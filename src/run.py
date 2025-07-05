import argparse
import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import from benchmark
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from benchmark.benchmark import Benchmark

# Main function to run the benchmark
def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='SVGBench: A challenging contamination-free LLM benchmark that tests knowledge, coding, physical reasoning capabilities of LLMs.')
    
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
        '--api-key',
        default=os.getenv('OPENROUTER_API_KEY'),
        help='Your API key for the endpoint'
    )
    
    parser.add_argument(
        '--open-router-api-key',
        default=os.getenv('OPENROUTER_API_KEY'),
        help='Your OpenRouter API key'
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
            open_router_api_key=open_router_api_key
        )
        # Run the benchmark
        benchmark.run(run_full_benchmark=True)

if __name__ == "__main__":
    main()
