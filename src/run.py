import argparse
import os
import sys
import shutil
import subprocess
from dotenv import load_dotenv

# Add the src directory to the path so we can import from benchmark
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from benchmark.benchmark import Benchmark

# Main function to run the benchmark
def main():
    # Load environment variables from .env file
    load_dotenv()
    # Create argument parser
    parser = argparse.ArgumentParser(description='SVGBench: A challenging LLM benchmark that tests knowledge, coding, physical reasoning capabilities of LLMs.')
    # Add command line arguments
    parser.add_argument(
        '--model', 
        required=True,
        help='The model to test. Test multiple models by separating them with a semicolon. (e.g. "google/gemini-2.5-flash;qwen/qwen3-30b-a3b")'
    )
    parser.add_argument(
        '--endpoint', 
        default='https://openrouter.ai/api/v1',
        help='The OpenAI compatible endpoint to test with (default: https://openrouter.ai/api/v1)'
    )
    parser.add_argument(
        '--open-router-endpoint',
        default='https://openrouter.ai/api/v1',
        help='The OpenRouter endpoint to use (default: https://openrouter.ai/api/v1)'
    )
    parser.add_argument(
        '--api-key',
        default=os.getenv('OPENROUTER_API_KEY'),
        help='Your API key for the endpoint'
    )
    parser.add_argument(
        '--open-router-api-key',
        default=os.getenv('OPENROUTER_API_KEY'),
        help='Your OpenRouter API key'
    )
    parser.add_argument(
        '--reasoning-effort',
        choices=['xhigh', 'high', 'medium', 'low'],
        help='Reasoning effort level for models that support it (high, medium, low)'
    )
    parser.add_argument(
        '--reasoning-max-tokens',
        type=int,
        help='Maximum number of tokens to use for reasoning (Anthropic-style models)'
    )
    parser.add_argument(
        '--max-output-tokens',
        type=int,
        help='Maximum number of output tokens for the response'
    )
    # Parse arguments
    args = parser.parse_args()
    # Get API key from argument or environment variable
    api_key = args.api_key or os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Error: API key must be provided via --api-key argument or OPENROUTER_API_KEY environment variable")
        sys.exit(1)
    # Get OpenRouter API key from argument or use the main API key as fallback
    open_router_api_key = args.open_router_api_key or api_key
    # Create benchmark instance for each model
    models = args.model.split(";")
    for model in models:
        benchmark = Benchmark(
            model=model,
            endpoint=args.endpoint,
            api_key=api_key,
            open_router_api_key=open_router_api_key,
            open_router_endpoint=args.open_router_endpoint,
            reasoning_effort=args.reasoning_effort,
            reasoning_max_tokens=args.reasoning_max_tokens,
            max_output_tokens=args.max_output_tokens
        )
        # Run the benchmark
        benchmark.run(run_full_benchmark=True)
    
    # Update the models list for the webUI
    try:
        print("Updating models list for webUI...")
        webui_module_path = os.path.join("results", "webUI")
        if os.path.exists(os.path.join(webui_module_path, "generate_models_list.py")):
            # Add the webUI directory to the path temporarily
            sys.path.insert(0, webui_module_path)
            try:
                from generate_models_list import generate_models_list
                # Call the function with the results directory and webUI output directory
                results_dir = "results"
                output_dir = webui_module_path
                generate_models_list(results_dir=results_dir, output_dir=output_dir, verbose=True)
                print("Models list updated successfully!")
            finally:
                # Remove the path we added
                sys.path.pop(0)
        else:
            print(f"Warning: generate_models_list.py not found in {webui_module_path}. Skipping models list update.")
    except ImportError as e:
        print(f"Warning: Failed to import generate_models_list: {e}")
    except Exception as e:
        print(f"Warning: Error updating models list: {e}")
    
    # Run the webUI with user confirmation
    if input("Run the webUI? (y/n): ").lower() == "y":
        # Start the server from the results directory
        if shutil.which("python"):
            # Notify the user that the server is running
            print("WebUI started at http://localhost:8000/webUI")
            subprocess.run(["python", "-m", "http.server", "8000"], cwd="results/")
        elif shutil.which("python3"):
            # Notify the user that the server is running
            print("WebUI started at http://localhost:8000/webUI")
            subprocess.run(["python3", "-m", "http.server", "8000"], cwd="results/")
        else:
            print("Error: Neither 'python' nor 'python3' command found")
            sys.exit(1)

if __name__ == "__main__":
    main()