# Testing
from PIL import Image
import numpy as np
import subprocess

def preprocess_image(input_path, output_path):
    # Load PNG image using Pillow
    img = Image.open(input_path).convert('L')  # Convert to grayscale

    # Perform any additional preprocessing here if needed
    # For example, you can use filters, adjustments, etc.

    # Save the preprocessed image
    img.save(output_path)

def convert_png_to_svg(preprocessed_path, svg_output_path):
    # Use Potrace to convert preprocessed image to SVG
    subprocess.run(['potrace', preprocessed_path, '-o', svg_output_path])

# Example usage
input_png = 'web_dev/Approve_icon.svg.png'
preprocessed_png = 'preprocessed.png'
output_svg = 'output.svg'

preprocess_image(input_png, preprocessed_png)
convert_png_to_svg(preprocessed_png, output_svg)