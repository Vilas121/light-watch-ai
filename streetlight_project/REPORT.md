# Project Report — Broken Streetlight Detection System

**Course:** AI / Machine Learning Mini Project
**Tools:** Python, Streamlit, TensorFlow/Keras, OpenCV, MobileNetV2

---

## 1. Abstract

Street lighting is essential for road safety at night, yet faulty lamps often
stay unrepaired for weeks because faults are reported manually. This project
presents a simple AI based solution: a deep learning image classifier that
examines a nighttime photograph of a streetlight and predicts whether it is
**Working** or **Broken**. The system uses transfer learning on the pre-trained
**MobileNetV2** convolutional neural network and is wrapped in a lightweight
**Streamlit** web interface, so a user can upload an image and receive a
prediction with a confidence percentage in a few seconds.

---

## 2. Introduction

Cities operate thousands of streetlights. Maintenance teams rely on citizen
complaints or manual night patrols to find broken lamps, both of which are slow
and inconsistent. Modern image classification models can recognise visual
patterns with high accuracy, and a lit lamp looks visibly different from an
unlit one. By training a small classifier on top of a pre-trained network, we
can automate this inspection using ordinary photographs taken with a phone.

---

## 3. Problem Statement

To design and implement a system that automatically classifies a nighttime
streetlight image as **Working Streetlight** or **Broken Streetlight**, and
reports the prediction confidence through an easy-to-use web interface.

---

## 4. Objectives

1. Collect / organise a small dataset of nighttime streetlight images in two
   classes: *Working* and *Broken*.
2. Apply transfer learning using the pre-trained MobileNetV2 model.
3. Preprocess images consistently (resize to 224×224, scale pixel values).
4. Build a Streamlit interface with Home, Upload, Prediction and About pages.
5. Display the result with colour coding (green = Working, red = Broken) and a
   confidence percentage.
6. Handle errors gracefully, e.g. when no image is uploaded.

---

## 5. Methodology

**Step 1 — Data collection.** Images are placed in `dataset/Working/` and
`dataset/Broken/`. The folder names become the class labels automatically.

**Step 2 — Preprocessing.** Each image is converted to RGB, resized to
224×224 with OpenCV, and scaled using MobileNetV2's `preprocess_input`
(pixel values mapped to the range −1 to 1).

**Step 3 — Model building (transfer learning).** MobileNetV2 pre-trained on
ImageNet is loaded without its top layer and frozen. A small head is added:

```
MobileNetV2 (frozen)
   -> GlobalAveragePooling2D
   -> Dense(64, relu)
   -> Dense(2, softmax)      # Broken / Working
```

**Step 4 — Training.** The model is compiled with the Adam optimiser and
categorical cross-entropy loss, and trained for a few epochs with an 80/20
train–validation split and light augmentation (flip, small rotation).

**Step 5 — Prediction.** The saved model (`model/streetlight_model.h5`) is
loaded once. For a new image, `model.predict()` returns two probabilities; the
larger one gives the label and the confidence percentage.

**Step 6 — Interface.** Streamlit provides the sidebar navigation, file
uploader, loading spinner, success message and colour-coded result card.

**Flow diagram**

```text
Upload image -> Preprocess (resize + scale) -> MobileNetV2 classifier
             -> Softmax probabilities -> Label + Confidence -> Display
```

---

## 6. Technologies Used

| Technology | Role in the project |
|---|---|
| Python 3 | Core programming language |
| Streamlit | Web user interface (pages, upload, results) |
| TensorFlow / Keras | Building, training and loading the model |
| MobileNetV2 | Pre-trained CNN used for transfer learning |
| OpenCV | Image resizing and processing |
| NumPy | Numerical array operations |
| Pillow | Reading uploaded image files |

---

## 7. Expected Output

- The user uploads a nighttime streetlight image on the Upload page.
- A loading animation appears while the model runs.
- The Prediction page shows the image, a success message, and either:
  - 🟢 **Working Streetlight** — displayed in green, with confidence e.g. 94.2%
  - 🔴 **Broken Streetlight** — displayed in red, with confidence e.g. 91.7%
- If no image is uploaded, a clear error message is shown instead.

---

## 8. Conclusion

The project demonstrates that a common civic problem can be addressed with a
small, understandable deep learning pipeline. Using transfer learning, good
accuracy is achievable with only a few hundred images and a few minutes of
training on a normal laptop. The Streamlit interface makes the model usable by
someone with no programming background, which is the key requirement for a
practical maintenance tool.

---

## 9. Future Scope

- Detect several streetlights within one wide-angle photo using object detection.
- Build a mobile app so field staff can capture and classify on the spot.
- Identify partially faulty lights (dim or flickering), not just on/off.
- Automatically generate a maintenance report listing faulty lamps.
- Train on a larger, more varied dataset covering fog, rain and different
  camera qualities to improve robustness.