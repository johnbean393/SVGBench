import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.llm import LLM
from utils.svg_renderer import SVGRenderer

# Class to run a benchmark
class Benchmark:

    # Function to initialize the benchmark class
    def __init__(
            self, 
            model: str, 
            endpoint: str, 
            api_key: str
    ):
        self.llm = LLM(model=model, endpoint=endpoint, api_key=api_key)

    # Function to run a benchmark
    def run(
            self,
            run_full_benchmark: bool = True,
            max_workers: int = 10
    ):
        # Load questions JSON
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(script_dir, '..', '..')
        json_filename = "questions.json" if run_full_benchmark else "test_questions.json"
        json_path = os.path.join(project_root, "questions", json_filename)
        with open(json_path, "r") as file:
            questions = json.load(file)
        # Create results directory
        results_dir = f"results/{self.llm.model.replace('/', '-')}"
        os.makedirs(results_dir, exist_ok=True)
        # Initialize results tracking
        results = {
            "model": self.llm.model,
            "timestamp": datetime.now().isoformat(),
            "total_questions": len(questions),
            "question_scores": [],
            "average_score": 0.0
        }
        # Run questions in parallel with max 10 workers
        with ThreadPoolExecutor(
            max_workers=max_workers
        ) as executor:
            # Submit all questions to the executor
            future_to_question = {
                executor.submit(self._run_question_with_retry, question, index): (question, index)
                for index, question in enumerate(questions)
            }
            # Process completed futures
            for future in as_completed(future_to_question):
                question, index = future_to_question[future]
                try:
                    score = future.result()
                    results["question_scores"].append({
                        "question_index": index,
                        "prompt": question["prompt"],
                        "requirements": question["requirements"],
                        "score": score
                    })
                    print(f"Completed question {index} with score: {score}")
                except Exception as e:
                    print(f"Failed to complete question {index} after retries: {e}")
                    results["question_scores"].append({
                        "question_index": index,
                        "prompt": question["prompt"],
                        "requirements": question["requirements"],
                        "score": 0.0,
                        "error": str(e)
                    })
        
        # Sort results by question index to maintain order
        results["question_scores"].sort(key=lambda x: x["question_index"])
        
        # Calculate average score
        total_score = sum(item["score"] for item in results["question_scores"])
        results["average_score"] = total_score / len(results["question_scores"]) if results["question_scores"] else 0.0
        
        # Save results to JSON file
        results_file_path = os.path.join(results_dir, "benchmark_results.json")
        with open(results_file_path, "w") as file:
            json.dump(results, file, indent=2)
        
        print(f"\nBenchmark completed!")
        print(f"Average score: {results['average_score']:.3f}")
        print(f"Results saved to: {results_file_path}")
        
        return results

    # Function to run a single question with retry logic
    def _run_question_with_retry(
            self, 
            question: dict, 
            index: int
    ) -> float:
        # Retry 3 times if failed
        for attempt in range(3):
            try:
                return self.run_question(question, index)
            except Exception as e:
                print(f"Error running question {index} (attempt {attempt + 1}): {e}")
                if attempt == 2:  # Last attempt
                    # Return score of 0 if failed
                    return 0.0
                continue

    # Function to run a single question
    def run_question(
            self, 
            question: dict, 
            index: int
    ) -> float:
        # Formulate requirements
        requirements = "\n".join([f"{i+1}. {req}" for i, req in enumerate(question["requirements"])])
        requirements_num = len(question["requirements"])
        # Generate the SVG code
        self.generate_svg_code(question["prompt"], requirements, index)
        # Evaluate the generated SVG
        score = self.evaluate_svg(question, index, requirements, requirements_num)
        # Return the score
        return score
    
    # Function to generate the SVG code
    def generate_svg_code(
            self, 
            prompt: str, 
            requirements: str, 
            index: int
    ):
        generate_prompt = f"""
{prompt} Wrap the SVG code in an SVG code block following the example below.

Example:
```svg
<svg viewBox="0 0 100 100" width="100" height="100">
    <circle cx="50" cy="50" r="40" fill="red" />
</svg>
```

Requirements:
{requirements}
"""
        # Generate text from the image
        text = self.llm.generate_text(generate_prompt)
        # Extract the SVG code from the text
        svg_code = text.split("```svg")[1].split("```")[0]
        # Create the results directory if it doesn't exist
        results_dir = f"results/{self.llm.model.replace('/', '-')}"
        os.makedirs(results_dir, exist_ok=True)
        # Render the SVG code to an image
        SVGRenderer.render_svg(svg_code, results_dir, f"question_{index}")
        print(f"Generated SVG for question {index}")
        # Save the SVG code to a file
        with open(f"{results_dir}/question_{index}.svg", "w") as file:
            file.write(svg_code)

    # Function to evaluate the generated SVG
    def evaluate_svg(
            self, 
            question: dict, 
            index: int, 
            requirements: str, 
            requirements_num: int
    ) -> float:
        # Get the SVG path
        svg_path = f"results/{self.llm.model.replace('/', '-')}/question_{index}.svg"
        # Formulate prompt
        evaluate_prompt = f"""
How many of the following {requirements_num} requirements were fulfilled? Respond with a number ONLY in the following JSON schema.

{{
    "number_of_fulfilled_requirements": 3
}}

Requirements:
{requirements}
"""
        # Init evaluator LLM
        evaluator_llm = LLM(
            model="gemini/gemini-2.5-pro",
            endpoint="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        # Evaluate the SVG
        json_response = self.llm.generate_text(
            evaluate_prompt, 
            json_schema={
                "type": "object",
                "properties": {
                    "number_of_fulfilled_requirements": {
                        "type": "number"
                        }
                    }
            }
        )
        # Parse the JSON response
        parsed_json = json.loads(json_response)
        # Calculate the score
        score = parsed_json["number_of_fulfilled_requirements"] / requirements_num
        # Return the score
        return score

# Example usage
if __name__ == "__main__":
    # Get the directory two levels up from the current file
    parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Load environment variable from .env file in that directory
    from dotenv import load_dotenv
    load_dotenv(os.path.join(parent_dir, '.env'))
    # Get the API key from the environment variable
    api_key = os.getenv("OPENROUTER_API_KEY")
    # Create an instance of the Benchmark class
    benchmark = Benchmark(
        model="google/gemini-2.5-pro",
        endpoint="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    # Run the benchmark
    benchmark.run(run_full_benchmark=False)