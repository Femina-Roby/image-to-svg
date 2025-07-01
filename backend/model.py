from PIL import Image
import numpy as np
import cv2
import svgwrite
from io import BytesIO

def convert_image_to_svg(image_bytes: bytes) -> str:
    try:
        image = Image.open(BytesIO(image_bytes)).convert("L")  # Grayscale
        image = image.resize((256, 256))  # Resize for simplicity
        img_array = np.array(image)

        # Threshold the image to binary
        _, thresh = cv2.threshold(img_array, 128, 255, cv2.THRESH_BINARY_INV)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create SVG document
        dwg = svgwrite.Drawing(size=("256px", "256px"))

        for contour in contours:
            points = [(float(pt[0][0]), float(pt[0][1])) for pt in contour]
            if points:
                dwg.add(dwg.polygon(points=points, fill='black'))

        return dwg.tostring()

    except Exception as e:
        print("SVG conversion failed:", e)
        return f"<svg><text>Error: {str(e)}</text></svg>"