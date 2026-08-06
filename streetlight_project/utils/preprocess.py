"""
Image preprocessing helpers.

Every image must be converted into the exact shape MobileNetV2 expects:
a 224 x 224 RGB image, scaled the same way the original model was trained.
"""

import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# MobileNetV2 always works with 224 x 224 images
IMAGE_SIZE = (224, 224)


def read_image(uploaded_file):
    """Turn a Streamlit uploaded file into a normal PIL image (RGB)."""
    image = Image.open(uploaded_file)
    return image.convert("RGB")


def preprocess_image(pil_image):
    """
    Convert a PIL image into a model-ready NumPy array.

    Steps:
    1. PIL image  ->  NumPy array
    2. Resize to 224 x 224 using OpenCV
    3. Scale pixel values the MobileNetV2 way (values between -1 and 1)
    4. Add a "batch" dimension, because Keras expects a list of images
    """
    array = np.array(pil_image)                       # step 1
    array = cv2.resize(array, IMAGE_SIZE)             # step 2
    array = preprocess_input(array.astype("float32")) # step 3
    array = np.expand_dims(array, axis=0)             # step 4 -> (1, 224, 224, 3)
    return array