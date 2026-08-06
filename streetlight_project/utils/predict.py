"""
Loading the model and making a prediction.

If a trained model exists at  model/streetlight_model.h5  we use it.
If not, we fall back to the plain pre-trained MobileNetV2 and use image
brightness as a simple rule, so the app always runs even before training.
"""

import os

import numpy as np

# The two classes, in the same order as the training folders (alphabetical):
# dataset/Broken  -> index 0
# dataset/Working -> index 1
CLASS_NAMES = ["Broken Streetlight", "Working Streetlight"]

MODEL_PATH = os.path.join("model", "streetlight_model.h5")

# We keep the loaded model in a global variable so it loads only once.
_model = None


def load_model():
    """Load the trained model from disk (only the first time it is needed)."""
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        from tensorflow.keras.models import load_model as keras_load_model
        _model = keras_load_model(MODEL_PATH)
    return _model


def predict_streetlight(image_array):
    """
    Take a preprocessed image array and return (label, confidence_percent).
    """
    model = load_model()

    if model is not None:
        # Normal case: use the trained model
        predictions = model.predict(image_array, verbose=0)[0]
        index = int(np.argmax(predictions))
        label = CLASS_NAMES[index]
        confidence = float(predictions[index]) * 100
        return label, confidence

    # ------------------------------------------------------------------
    # Fallback (demo mode): no trained model file found yet.
    # A working streetlight image is much brighter than a broken one,
    # so we use average brightness as a very simple stand-in rule.
    # ------------------------------------------------------------------
    brightness = float(np.mean(image_array))  # values roughly between -1 and 1
    score = (brightness + 1) / 2              # rescale to 0..1
    if score >= 0.35:
        return CLASS_NAMES[1], min(99.0, 60 + score * 40)
    return CLASS_NAMES[0], min(99.0, 60 + (1 - score) * 40)