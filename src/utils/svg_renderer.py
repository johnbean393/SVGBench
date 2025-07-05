import os
import platform

# Class to render SVG code to a file
class SVGRenderer:

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
        Render SVG code using Wand and save to specified path as PNG.
        
        Args:
            code (str): SVG code as a string
            directory_path (str): Directory path where the file should be saved
            filename (str): Name of the file (without extension)
        """
        # Set up macOS environment variables first
        SVGRenderer.setup_macos_environment()
        # Check if ImageMagick is installed
        if not SVGRenderer.check_imagemagick():
            # Install ImageMagick if not installed
            SVGRenderer.install_imagemagick()
            # Set up environment again after installation
            SVGRenderer.setup_macos_environment()
        # Now import Wand after environment is set up
        from wand.image import Image
        from wand.color import Color
        # Ensure the directory exists
        os.makedirs(directory_path, exist_ok=True)
        # Create the full file path with extension
        file_path = os.path.join(directory_path, f"{filename}.png")
        # Convert SVG to PNG using Wand
        with Image(blob=code.encode('utf-8'), format='svg') as img:
            img.format = 'png'
            img.save(filename=file_path)

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