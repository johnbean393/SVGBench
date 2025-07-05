#!/usr/bin/env python3

import os
import json
from pathlib import Path
import sys

# Function to generate the model list for the webUI
def generate_models_list(results_dir=None, output_dir=None, verbose=True):
    """
    Generate a list of available models from the results directory.
    
    Args:
        results_dir (str or Path, optional): Path to the results directory. 
                                           If None, uses the parent directory of this file.
        output_dir (str or Path, optional): Directory to write models.json to.
                                          If None, uses the directory of this file.
        verbose (bool): Whether to print progress messages.
    
    Returns:
        list: List of available model names.
    """
    if results_dir is None:
        results_dir = Path(__file__).parent.parent  # Go up one level from webUI to results
    else:
        results_dir = Path(results_dir)
    
    if output_dir is None:
        output_dir = Path(__file__).parent
    else:
        output_dir = Path(output_dir)
    
    models = []
    
    # Scan all directories in results
    for item in results_dir.iterdir():
        if item.is_dir() and item.name != 'webUI':  # Skip the webUI directory
            # Check if the directory contains benchmark_results.json
            benchmark_file = item / 'benchmark_results.json'
            if benchmark_file.exists():
                models.append(item.name)
    
    # Sort models alphabetically
    models.sort()
    
    # Write to models.json
    models_file = output_dir / 'models.json'
    with open(models_file, 'w') as f:
        json.dump({'models': models}, f, indent=2)
    
    if verbose:
        print(f"Generated models list with {len(models)} models:")
        for model in models:
            print(f"  - {model}")
    
    return models

if __name__ == '__main__':
    generate_models_list() 