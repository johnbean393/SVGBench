import os
import platform

# Class to render SVG code to a file
class SVGRenderer:

    # Function to set up general environment variables to suppress warnings
    @staticmethod
    def setup_environment():
        """
        Set up general environment variables to suppress Inkscape warnings.
        """
        # Suppress Inkscape warnings and output
        os.environ['INKSCAPE_PROFILE_DIR'] = '/dev/null'
        os.environ['G_MESSAGES_DEBUG'] = 'none'
        # Suppress GTK warnings
        os.environ['G_SLICE'] = 'always-malloc'
        os.environ['G_DEBUG'] = 'gc-friendly'

    # Function to set up macOS environment variables for ImageMagick
    @staticmethod
    def setup_macos_environment():
        """
        Set up ImageMagick environment variables for macOS.
        """
        if platform.system().lower() == "darwin":
            # Set ImageMagick environment variables for macOS
            os.environ['MAGICK_HOME'] = '/opt/homebrew/opt/imagemagick'
            current_dyld_path = os.environ.get('DYLD_LIBRARY_PATH', '')
            if current_dyld_path:
                os.environ['DYLD_LIBRARY_PATH'] = f'/opt/homebrew/opt/imagemagick/lib:{current_dyld_path}'
            else:
                os.environ['DYLD_LIBRARY_PATH'] = '/opt/homebrew/opt/imagemagick/lib'
            
            # Set ImageMagick configuration path
            os.environ['MAGICK_CONFIGURE_PATH'] = '/opt/homebrew/etc/ImageMagick-7'
        
        # Set up general environment variables
        SVGRenderer.setup_environment()

    # Function to check if ImageMagick is installed
    @staticmethod
    def check_imagemagick():
        """
        Check if ImageMagick is installed on macOS, Linux, and Windows.
        """
        system = platform.system().lower()
        if system == "windows":
            # On Windows, check for magick.exe (ImageMagick 7+) or convert.exe (ImageMagick 6)
            return (os.system("magick -version >nul 2>&1") == 0 or 
                    os.system("convert -version >nul 2>&1") == 0)
        elif system == "darwin":
            # On macOS, check for convert command
            return os.system("convert -version > /dev/null 2>&1") == 0
        else:
            # On Linux, check for convert command
            return os.system("convert -version > /dev/null 2>&1") == 0
    
    # Function to install ImageMagick if not installed using script
    @staticmethod
    def install_imagemagick():
        """
        Install ImageMagick on macOS, Linux, and Windows.
        """
        # Run the setup script
        os.system("bash setup_imagemagick.sh")

    # Function to render SVG code to an image file
    @staticmethod
    def render_svg(code: str, directory_path: str, filename: str):
        """
        Render SVG code using Selenium and save to specified path as PNG.
        
        Args:
            code (str): SVG code as a string
            directory_path (str): Directory path where the file should be saved
            filename (str): Name of the file (without extension)
        """
        # Ensure the directory exists
        os.makedirs(directory_path, exist_ok=True)
        
        # Create the full file path with extension
        file_path = os.path.join(directory_path, f"{filename}.png")
        
        # Use the Selenium implementation
        SVGRenderer.svg_to_png_selenium(code, file_path)

    @staticmethod
    def svg_to_png_selenium(svg_code, output_path, width=800, height=600):
        """
        Convert SVG code to PNG using Selenium with headless browser.
        
        Args:
            svg_code (str): The SVG code as a string
            output_path (str): Path where the PNG should be saved
            width (int): Browser width
            height (int): Browser height
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            import base64
            import tempfile
            import os
        except ImportError:
            raise ImportError("Please install selenium: pip install selenium")
        
        # Create HTML with embedded SVG
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ margin: 0; padding: 0; }}
                svg {{ display: block; }}
            </style>
        </head>
        <body>
            {svg_code}
        </body>
        </html>
        """
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(f'--window-size={width},{height}')
        
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        try:
            # Launch browser and take screenshot
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f'file://{os.path.abspath(temp_html_path)}')
            driver.save_screenshot(output_path)
            driver.quit()
            
        finally:
            # Clean up
            os.unlink(temp_html_path)

# Example usage
if __name__ == "__main__":
    # Define the SVG code
    svg_code = """
<svg viewBox="0 0 100 65" width="200" height="130">
  <g fill="#F2F9FF" stroke="#CDE4F5" stroke-width="2" stroke-linejoin="round">
    <!-- The flat bottom of the cloud -->
    <rect x="20" y="40" width="60" height="20" rx="10"></rect>
    <!-- The puffy top parts of the cloud -->
    <circle cx="35" cy="35" r="18"></circle>
    <circle cx="60" cy="30" r="25"></circle>
    <circle cx="80" cy="42" r="12"></circle>
  </g>
</svg>
"""
    # Render the SVG code to a PNG file
    SVGRenderer.render_svg(svg_code, "assets", "test_image")