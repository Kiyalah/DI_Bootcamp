# ============================================
# Daily Challenge: Hands-On Image Transformation
# and Visualization
# ============================================

# Install libraries (Google Colab)
# Uncomment if needed

# !pip install tensorflow
# !pip install keras
# !pip install pillow

# ============================================
# Import Libraries
# ============================================

from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from scipy.ndimage import rotate
import tensorflow as tf
from tensorflow import keras

# ============================================
# Load and Display Original Image
# ============================================

# Path of image
image_path = 'flowers/flowers/19_010.png'

# Load image using PIL
original_image = Image.open(image_path)

# Display original image
plt.figure(figsize=(5,5))
plt.imshow(original_image)
plt.title("Original Image")
plt.axis("off")
plt.show()

# ============================================
# Rotate Image by 30 Degrees
# ============================================

def rotate_image_30_degrees(image):
    return rotate(image, 30, reshape=False)

# Rotate image
rotated_image = rotate_image_30_degrees(original_image)

# Display rotated image
plt.figure(figsize=(5,5))
plt.imshow(rotated_image)
plt.title("Rotated Image (30 Degrees)")
plt.axis("off")
plt.show()

# ============================================
# Flip Image Horizontally
# ============================================

horizontal_flip = ImageOps.mirror(original_image)

plt.figure(figsize=(5,5))
plt.imshow(horizontal_flip)
plt.title("Horizontal Flip")
plt.axis("off")
plt.show()

# ============================================
# Flip Image Vertically
# ============================================

vertical_flip = ImageOps.flip(original_image)

plt.figure(figsize=(5,5))
plt.imshow(vertical_flip)
plt.title("Vertical Flip")
plt.axis("off")
plt.show()

# ============================================
# Zoom In Image (1.2x)
# ============================================

# Get original size
width, height = original_image.size

# Resize image
zoomed_image = original_image.resize(
    (int(width * 1.2), int(height * 1.2))
)

# Display zoomed image
plt.figure(figsize=(5,5))
plt.imshow(zoomed_image)
plt.title("Zoomed Image (1.2x)")
plt.axis("off")
plt.show()

print("\n===== END OF IMAGE TRANSFORMATIONS =====")