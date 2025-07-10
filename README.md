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

## Leaderboard (Updated 10/07/2025)

| Model | Score |
| :--- | ---: |
| gemini-2.5-pro | 61.4% |
| claude-3.7-sonnet | 60.4% |
| claude-sonnet-4 | 59.4% |
| gpt-4.1 | 58.4% |
| grok-4 | 54.4% |
| gpt-4.1-mini | 53.4% |
| gemini-2.5-flash | 51.4% |
| o4-mini | 48.0% |
| claude-3.5-sonnet | 47.9% |
| grok-3 | 45.8% |
| o3-mini | 42.7% |
| gemini-2.0-flash-001 | 41.6% |
| deepseek-r1-0528 | 40.4% |
| gemini-2.0-flash-lite-001 | 39.6% |
| llama-4-maverick | 36.0% |
| mistral-small-3.2-24b-instruct | 35.9% |
| gpt-4.1-nano | 35.5% |
| qwen3-235b-a22b | 33.9% |
| claude-3.5-haiku | 33.3% |
| gpt-4o | 31.8% |
| qwen3-32b | 29.4% |
| llama-4-scout | 26.9% |
| qwen3-30b-a3b | 26.1% |
| gpt-4o-mini | 25.4% |
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