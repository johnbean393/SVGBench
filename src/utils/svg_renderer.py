import os
import platform
import re
import xml.etree.ElementTree as ET

# Class to render SVG code to a file
class SVGRenderer:

    # Function to extract SVG dimensions
    @staticmethod
    def extract_svg_dimensions(svg_code):
        """
        Extract width and height from SVG code.
        
        Args:
            svg_code (str): SVG code as a string
            
        Returns:
            tuple: (width, height) in pixels, or (800, 600) as default
        """
        try:
            # Parse the SVG code
            root = ET.fromstring(svg_code.strip())
            
            # Get width and height attributes
            width = root.get('width')
            height = root.get('height')
            
            # If width/height are present, parse them
            if width and height:
                # Remove units and convert to int
                width_val = SVGRenderer._parse_dimension(width)
                height_val = SVGRenderer._parse_dimension(height)
                
                if width_val and height_val:
                    return (width_val, height_val)
            
            # If no width/height, try to extract from viewBox
            viewbox = root.get('viewBox')
            if viewbox:
                # viewBox format: "min-x min-y width height"
                parts = viewbox.split()
                if len(parts) >= 4:
                    try:
                        vb_width = float(parts[2])
                        vb_height = float(parts[3])
                        # Use viewBox dimensions, but ensure reasonable size
                        return (max(int(vb_width), 200), max(int(vb_height), 200))
                    except (ValueError, IndexError):
                        pass
            
        except ET.ParseError:
            # If XML parsing fails, try regex approach
            try:
                # Try to find width and height with regex
                width_match = re.search(r'width\s*=\s*["\']?(\d+(?:\.\d+)?)["\']?', svg_code, re.IGNORECASE)
                height_match = re.search(r'height\s*=\s*["\']?(\d+(?:\.\d+)?)["\']?', svg_code, re.IGNORECASE)
                
                if width_match and height_match:
                    width_val = float(width_match.group(1))
                    height_val = float(height_match.group(1))
                    return (int(width_val), int(height_val))
                
                # Try viewBox with regex
                viewbox_match = re.search(r'viewBox\s*=\s*["\']([^"\']+)["\']', svg_code, re.IGNORECASE)
                if viewbox_match:
                    parts = viewbox_match.group(1).split()
                    if len(parts) >= 4:
                        try:
                            vb_width = float(parts[2])
                            vb_height = float(parts[3])
                            return (max(int(vb_width), 200), max(int(vb_height), 200))
                        except (ValueError, IndexError):
                            pass
            except Exception:
                pass
        
        # Default fallback with better proportions
        return (800, 600)

    @staticmethod
    def _parse_dimension(dim_str):
        """
        Parse dimension string and convert to pixels.
        
        Args:
            dim_str (str): Dimension string like "100px", "50%", "2in", etc.
            
        Returns:
            int: Dimension in pixels, or None if cannot parse
        """
        if not dim_str:
            return None
        
        # Remove whitespace
        dim_str = dim_str.strip()
        
        # Handle percentage (assume 800px as base for percentage)
        if dim_str.endswith('%'):
            try:
                percentage = float(dim_str[:-1])
                # Use a more generous base for percentage calculations
                return int(1000 * percentage / 100)
            except ValueError:
                return None
        
        # Handle units
        unit_multipliers = {
            'px': 1,
            'pt': 1.33,  # 1 pt = 1.33 px
            'pc': 16,    # 1 pc = 16 px
            'mm': 3.78,  # 1 mm = 3.78 px
            'cm': 37.8,  # 1 cm = 37.8 px
            'in': 96,    # 1 in = 96 px
        }
        
        # Try to extract number and unit
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([a-z%]*)$', dim_str.lower())
        if match:
            value = float(match.group(1))
            unit = match.group(2) or 'px'
            
            multiplier = unit_multipliers.get(unit, 1)
            return int(value * multiplier)
        
        # If no unit, assume pixels
        try:
            return int(float(dim_str))
        except ValueError:
            return None

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
    def svg_to_png_selenium(svg_code, output_path, width=None, height=None):
        """
        Convert SVG code to PNG using Selenium with headless browser.
        
        Args:
            svg_code (str): The SVG code as a string
            output_path (str): Path where the PNG should be saved
            width (int, optional): Browser width. If None, will be extracted from SVG
            height (int, optional): Browser height. If None, will be extracted from SVG
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            import base64
            import tempfile
            import os
        except ImportError:
            raise ImportError("Please install selenium: pip install selenium")
        
        # Calculate dynamic dimensions from SVG if not provided
        if width is None or height is None:
            calculated_width, calculated_height = SVGRenderer.calculate_svg_bounds(svg_code)
            width = width or calculated_width
            height = height or calculated_height
        
        # Create HTML with embedded SVG - force exact dimensions
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ 
                    margin: 0; 
                    padding: 0; 
                    box-sizing: border-box;
                }}
                body {{ 
                    background: white;
                    width: {width}px;
                    height: {height}px;
                    overflow: hidden;
                }}
                svg {{ 
                    display: block;
                    width: {width}px !important;
                    height: {height}px !important;
                }}
            </style>
        </head>
        <body>
            {svg_code}
        </body>
        </html>
        """
        
        # Setup Chrome options with device emulation for exact dimensions
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument(f'--window-size={width},{height}')
        chrome_options.add_argument(f'--force-device-scale-factor=1')
        
        # Create temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        try:
            # Launch browser and take screenshot
            driver = webdriver.Chrome(options=chrome_options)
            
            # Set window size explicitly after driver creation
            driver.set_window_size(width, height + 139)
            
            driver.get(f'file://{os.path.abspath(temp_html_path)}')
            
            # Get the body element and take a screenshot of just that
            body = driver.find_element("tag name", "body")
            body.screenshot(output_path)
            
            driver.quit()
            
        finally:
            # Clean up
            os.unlink(temp_html_path)

    @staticmethod
    def calculate_svg_bounds(svg_code):
        """
        Calculate the actual bounds of SVG elements to determine optimal rendering size.
        
        Args:
            svg_code (str): SVG code as a string
            
        Returns:
            tuple: (width, height) based on actual content bounds
        """
        try:
            # Parse the SVG code
            root = ET.fromstring(svg_code.strip())
            # First try to get explicit dimensions
            width = root.get('width')
            height = root.get('height')
            viewbox = root.get('viewBox')
            # If we have explicit width/height, use them
            if width and height:
                width_val = SVGRenderer._parse_dimension(width)
                height_val = SVGRenderer._parse_dimension(height)
                if width_val and height_val:
                    return (width_val, height_val)
            # If we have viewBox, use it as the base
            if viewbox:
                parts = viewbox.split()
                if len(parts) >= 4:
                    try:
                        vb_x = float(parts[0])
                        vb_y = float(parts[1])
                        vb_width = float(parts[2])
                        vb_height = float(parts[3])
                        
                        # Calculate actual bounds by analyzing elements
                        min_x, min_y, max_x, max_y = SVGRenderer._analyze_svg_elements(root)
                        
                        if min_x is not None and max_x is not None:
                            # Use the larger of viewBox or actual content bounds
                            content_width = max_x - min_x
                            content_height = max_y - min_y
                            
                            # Use viewBox as minimum, but expand if content is larger
                            final_width = max(vb_width, content_width + abs(min_x) * 2)
                            final_height = max(vb_height, content_height + abs(min_y) * 2)
                            
                            return (int(final_width), int(final_height))
                        else:
                            # Fallback to viewBox dimensions
                            return (int(vb_width), int(vb_height))
                    except (ValueError, IndexError):
                        pass
            # If no viewBox, analyze elements directly
            min_x, min_y, max_x, max_y = SVGRenderer._analyze_svg_elements(root)
            if min_x is not None and max_x is not None:
                # Add some margin around the content
                margin = 20
                width = max_x - min_x + margin * 2
                height = max_y - min_y + margin * 2
                return (max(int(width), 200), max(int(height), 200))
            
        except ET.ParseError:
            # If XML parsing fails, try regex approach for basic dimensions
            try:
                width_match = re.search(r'width\s*=\s*["\']?(\d+(?:\.\d+)?)["\']?', svg_code, re.IGNORECASE)
                height_match = re.search(r'height\s*=\s*["\']?(\d+(?:\.\d+)?)["\']?', svg_code, re.IGNORECASE) 
                if width_match and height_match:
                    width_val = float(width_match.group(1))
                    height_val = float(height_match.group(1))
                    return (int(width_val), int(height_val))
                # Try viewBox with regex
                viewbox_match = re.search(r'viewBox\s*=\s*["\']([^"\']+)["\']', svg_code, re.IGNORECASE)
                if viewbox_match:
                    parts = viewbox_match.group(1).split()
                    if len(parts) >= 4:
                        try:
                            vb_width = float(parts[2])
                            vb_height = float(parts[3])
                            return (int(vb_width), int(vb_height))
                        except (ValueError, IndexError):
                            pass
            except Exception:
                pass
        # Final fallback
        return (800, 600)

    @staticmethod
    def _analyze_svg_elements(root):
        """
        Analyze SVG elements to find their bounds.
        
        Args:
            root: XML root element of the SVG
            
        Returns:
            tuple: (min_x, min_y, max_x, max_y) or (None, None, None, None) if no elements found
        """
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        found_elements = False
        
        # Recursively analyze all elements
        for elem in root.iter():
            bounds = SVGRenderer._get_element_bounds(elem)
            if bounds:
                found_elements = True
                elem_min_x, elem_min_y, elem_max_x, elem_max_y = bounds
                min_x = min(min_x, elem_min_x)
                min_y = min(min_y, elem_min_y)
                max_x = max(max_x, elem_max_x)
                max_y = max(max_y, elem_max_y)
        
        if not found_elements:
            return (None, None, None, None)
        
        return (min_x, min_y, max_x, max_y)

    @staticmethod
    def _get_element_bounds(elem):
        """
        Get bounds for a specific SVG element.
        
        Args:
            elem: XML element
            
        Returns:
            tuple: (min_x, min_y, max_x, max_y) or None if no bounds found
        """
        tag = elem.tag.lower()
        if tag.endswith('rect'):
            return SVGRenderer._get_rect_bounds(elem)
        elif tag.endswith('circle'):
            return SVGRenderer._get_circle_bounds(elem)
        elif tag.endswith('ellipse'):
            return SVGRenderer._get_ellipse_bounds(elem)
        elif tag.endswith('line'):
            return SVGRenderer._get_line_bounds(elem)
        elif tag.endswith('polyline') or tag.endswith('polygon'):
            return SVGRenderer._get_poly_bounds(elem)
        elif tag.endswith('path'):
            return SVGRenderer._get_path_bounds(elem)
        elif tag.endswith('text'):
            return SVGRenderer._get_text_bounds(elem)
        
        return None

    @staticmethod
    def _get_rect_bounds(elem):
        """Get bounds for rectangle element."""
        try:
            x = float(elem.get('x', 0))
            y = float(elem.get('y', 0))
            width = float(elem.get('width', 0))
            height = float(elem.get('height', 0))
            return (x, y, x + width, y + height)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _get_circle_bounds(elem):
        """Get bounds for circle element."""
        try:
            cx = float(elem.get('cx', 0))
            cy = float(elem.get('cy', 0))
            r = float(elem.get('r', 0))
            return (cx - r, cy - r, cx + r, cy + r)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _get_ellipse_bounds(elem):
        """Get bounds for ellipse element."""
        try:
            cx = float(elem.get('cx', 0))
            cy = float(elem.get('cy', 0))
            rx = float(elem.get('rx', 0))
            ry = float(elem.get('ry', 0))
            return (cx - rx, cy - ry, cx + rx, cy + ry)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _get_line_bounds(elem):
        """Get bounds for line element."""
        try:
            x1 = float(elem.get('x1', 0))
            y1 = float(elem.get('y1', 0))
            x2 = float(elem.get('x2', 0))
            y2 = float(elem.get('y2', 0))
            return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _get_poly_bounds(elem):
        """Get bounds for polyline/polygon element."""
        try:
            points = elem.get('points', '')
            if not points:
                return None
            
            # Parse points string
            coords = []
            for point in points.replace(',', ' ').split():
                try:
                    coords.append(float(point))
                except ValueError:
                    continue
            
            if len(coords) < 4:  # Need at least 2 points (4 coordinates)
                return None
            x_coords = coords[0::2]
            y_coords = coords[1::2]
            return (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _get_path_bounds(elem):
        """Get approximate bounds for path element (simplified)."""
        try:
            d = elem.get('d', '')
            if not d:
                return None
            # Simple regex to extract numbers from path
            numbers = re.findall(r'-?\d+(?:\.\d+)?', d)
            if len(numbers) < 2:
                return None
            coords = [float(n) for n in numbers]
            x_coords = coords[0::2]
            y_coords = coords[1::2]
            return (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _get_text_bounds(elem):
        """Get approximate bounds for text element."""
        try:
            x = float(elem.get('x', 0))
            y = float(elem.get('y', 0))
            # Estimate text size (rough approximation)
            text_content = elem.text or ''
            font_size = elem.get('font-size', '12')
            try:
                font_size = float(re.search(r'\d+', str(font_size)).group())
            except:
                font_size = 12
            # Rough estimation: width = length * 0.6 * font_size, height = font_size
            width = len(text_content) * 0.6 * font_size
            height = font_size
            return (x, y - height, x + width, y)
        except (ValueError, TypeError):
            return None

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