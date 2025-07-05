#!/bin/bash

# Setup script for ImageMagick environment variables
# Source this file before running SVG rendering: source setup_imagemagick.sh

# For macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Install ImageMagick using Homebrew
    brew install imagemagick
    echo "ImageMagick installed successfully!"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # For Linux
    # Check if we're on Debian/Ubuntu
    if command -v apt-get &> /dev/null; then
        echo "Installing ImageMagick development libraries on Debian/Ubuntu..."
        sudo apt-get install libmagickwand-dev
        echo "ImageMagick development libraries installed successfully!"
    # Check if we're on Fedora/CentOS
    elif command -v yum &> /dev/null; then
        echo "Installing ImageMagick development libraries on Fedora/CentOS..."
        sudo yum install ImageMagick-devel
        echo "ImageMagick development libraries installed successfully!"
    else
        echo "Skipping ImageMagick setup for unsupported Linux distribution."
    fi
# For Windows
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "Windows detected. Manual installation required for ImageMagick."
    echo "Please download and install ImageMagick binary from:"
    echo "https://imagemagick.org/script/download.php#windows"
else
    echo "Skipping ImageMagick setup for unsupported systems."
fi