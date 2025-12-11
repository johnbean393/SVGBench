# SVGBench

A challenging LLM benchmark that tests knowledge, coding, instruction following, and physical reasoning capabilities of Large Language Models through SVG generation tasks.

![WebUI](https://raw.githubusercontent.com/johnbean393/SVGBench/refs/heads/main/assets/webUI.png)

## Overview

SVGBench evaluates how well language models can code and reason with physical concepts by presenting them with complex SVG generation prompts and detailed requirements. The benchmark tests models' abilities to:

- Knowledge: Understand spatial relationships and positioning
- Coding: Generate syntactically correct SVG code
- Instruction Follwing: Follow detailed visual specifications
- Physical Reasoning: Reason about physical properties and realistic representations

## Features

- **Comprehensive Test Suite**: 100+ unique questions with detailed requirements
- **Multi-model Support**: Compatible with any OpenAI API-compatible endpoint
- **Detailed Scoring**: Requirement-based evaluation system
- **Web UI**: Built-in results visualization interface

## Leaderboard

| Model | Score |
| :--- | ---: |
| gpt-5.2 (xhigh) | 74.4% |
| claude-opus-4.5 (non-thinking) | 72.0% |
| claude-opus-4.5 (thinking) | 71.5% |
| gemini-3-pro-preview | 68.7% |
| gpt-5.1 (high) | 67.5% |
| gpt-5 (high) | 67.4% |
| gpt-5.1 (medium) | 64.7% |
| claude-sonnet-4.5 | 62.2% |
| gemini-2.5-pro | 61.4% |
| gpt-5.1-codex (medium) | 61.8% |
| gpt-5-codex (medium) | 61.0% |
| glm-4.6 | 60.5% |
| claude-3.7-sonnet | 60.4% |
| gpt-5-mini | 59.7% |
| claude-sonnet-4 | 59.4% |
| gpt-4.1 | 58.4% |
| minimax-m2 | 58.3% |
| glm-4.5 | 58.3% |
| claude haiku-4.5 | 57.2% |
| kimi-k2-thinking | 57.1% |
| o3 | 56.7% |
| grok-4 | 54.4% |
| gpt-5.1-codex-mini (medium) | 54.0% |
| gpt-4.1-mini | 53.4% |
| deepseek-v3.1 | 53.1% |
| gemini-2.5-flash-preview-09-2025 | 52.1% |
| gemini-2.5-flash | 51.4% |
| deepseek-v3.2-exp | 51.3% |
| grok-4-fast | 50.5% |
| gpt-5-chat | 50.4% |
| deepseek-v3.2 | 49.8% |
| qwen3-coder-plus-2509 | 49.8% |
| gpt-5-nano | 49.7% |
| glm-4.5-air | 48.9% |
| qwen3-coder-480b-a35b-instruct | 48.7% |
| qwen3-235b-a22b-instruct-2507 | 48.6% |
| kimi-k2-0905 | 48.5% |
| deepseek-v3.1-terminus (reasoning) | 48.2% |
| o4-mini | 48.0% |
| claude-3.5-sonnet | 47.9% |
| deepseek-v3.1 (reasoning) | 47.8% |
| qwen3-next-80b-a3b-instruct | 47.4% |
| glm-4.5v | 46.5% |
| gpt-5.1-chat | 46.3% |
| mistral-medium-3.1 | 46.1% |
| mistral-large-2512 | 46.0% |
| grok-3 | 45.8% |
| gpt-oss-120b | 45.6% |
| gemini-2.5-flash-lite | 43.7% |
| kimi-k2 | 43.6% |
| o3-mini | 42.7% |
| gemini-2.5-flash-lite-preview-09-2025 | 41.8% |
| gemini-2.0-flash-001 | 41.6% |
| step3 | 41.4% |
| qwen3-vl-235b-a22b-instruct | 41.0% |
| qwen3-30b-a3b-instruct-2507 | 40.9% |
| deepseek-r1-0528 | 40.4% |
| sonoma-sky-alpha | 40.5% |
| gemini-2.0-flash-lite-001 | 39.6% |
| sonoma-dusk-alpha | 39.4% |
| qwen3-next-80b-a3b-thinking | 39.2% |
| qwen3-coder-30b-a3b-instruct | 38.0% |
| codestral-2508 | 37.9% |
| llama-4-maverick | 36.0% |
| mistral-small-3.2-24b-instruct | 35.9% |
| gpt-4.1-nano | 35.5% |
| gpt-oss-20b | 34.7% |
| qwen3-235b-a22b | 33.9% |
| nova-2-lite-v1 (non-thinking) | 33.9% |
| claude-3.5-haiku | 33.3% |
| nova-2-lite-v1 (thinking) | 32.0% |
| gpt-4o | 31.8% |
| hermes-4-405b | 31.6% |
| gemma-3-27b-it | 29.6% |
| qwen3-32b | 29.4% |
| qwen3-30b-a3b-thinking-2507 | 28.4% |
| llama-4-scout | 26.9% |
| qwen3-30b-a3b | 26.1% |
| gemma-3-12b-it | 25.7% |
| gpt-4o-mini | 25.4% |
| hermes-4-70b | 21.6% |
| seed-oss-36b-instruct | 21.1% |
| gemma-3-4b-it | 14.7% |
| trinity-mini | 8.7% |
| llama-3.1-8b-instruct | 6.8% |

## Installation

**Note:** This benchmark has only been tested on macOS.

### Prerequisites

- Python 3
- Google Chrome browser
- ChromeDriver (for SVG rendering)

### 1. Clone the Repository

```bash
git clone https://github.com/johnbean393/SVGBench.git
cd SVGBench
```

### 2. Set Up Python Environment

#### Option A: Using Conda (Recommended)
```bash
# Create and activate conda environment
conda create -n svgbench python=3.13
conda activate svgbench
```

#### Option B: Using Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install ChromeDriver

ChromeDriver is required for rendering SVG files to PNG images.

1. **Check your Chrome version:**
   - Open Google Chrome
   - Go to `chrome://version/`
   - Note the version number

2. **Download ChromeDriver:**
   - Visit [ChromeDriver Downloads](https://googlechromelabs.github.io/chrome-for-testing/)
   - Download the version that matches your Chrome browser
   - Extract the downloaded file

3. **Add ChromeDriver to PATH:**

   **macOS/Linux:**
   ```bash
   # Move chromedriver to a directory in your PATH
   sudo mv chromedriver /usr/local/bin/
   
   # Make it executable
   sudo chmod +x /usr/local/bin/chromedriver
   ```

   **Windows:**
   ```bash
   # Add the chromedriver.exe location to your system PATH
   # Or place chromedriver.exe in a directory already in PATH
   ```

4. **Verify installation:**
   ```bash
   chromedriver --version
   ```

## Usage

#### Command Line Options

- `--model` (required): The model to test. Support for multiple models by separating with semicolons
- `--endpoint`: OpenAI compatible endpoint (default: https://openrouter.ai/api/v1)
- `--api-key`: Your API key for the endpoint
- `--open-router-api-key`: Your OpenRouter API key (if different from main API key)

#### Examples

**Single model on OpenRouter:**
```bash
python src/run.py --model "anthropic/claude-sonnet-4" --api-key "sk-..."
```

**Multiple models:**
```bash
python src/run.py --model "google/gemini-2.5-pro;anthropic/claude-sonnet-4;openai/gpt-4.1"
```

**Custom endpoint:**
```bash
python src/run.py --model "gpt-4.1" --endpoint "https://api.openai.com/v1" --api-key "sk-..." --open-router-api-key "sk-..."
```

**Using environment variables:**
```bash
# Set in .env file: OPENROUTER_API_KEY=your_key_here
python src/run.py --model "google/gemini-2.5-flash"
```

### Test Mode

For development and testing, you can run a smaller subset of questions:

```bash
# This will use test_questions.json instead of the full questions.json
# Modify the run() call in src/run.py to use run_full_benchmark=False
```

### Viewing Results

After running the benchmark:

1. **Results Files**: Individual model results are saved in `results/{model-name}/benchmark_results.json`
2. **Generated Images**: SVG renderings are saved as PNG files in `results/{model-name}/`
3. **Web UI**: The benchmark offers to start a local web server for viewing results:
   ```
   Run the webUI? (y/n): y
   ```
   Access at: [http://localhost:8000/webUI](http://localhost:8000/webUI)

## Project Structure

```
SVGBench/
├── src/
│   ├── run.py              # Main entry point
│   ├── benchmark/
│   │   └── benchmark.py    # Core benchmark logic
│   └── utils/
│       ├── llm.py          # LLM interface
│       └── svg_renderer.py # SVG to PNG conversion
├── questions/
│   ├── questions.json      # Full benchmark questions
│   └── test_questions.json # Subset for testing
├── results/               # Generated results and images
├── requirements.txt       # Python dependencies
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request