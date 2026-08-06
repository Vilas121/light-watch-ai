# 💡 Broken Streetlight Detection System

A beginner-friendly AI mini project that predicts whether a streetlight in a
nighttime photo is **Working** or **Broken**, using a pre-trained
**MobileNetV2** image classification model and a **Streamlit** web interface.

---

## 1. Project Overview

Broken streetlights are usually found only when someone drives around and
notices them. This project automates that check: the user uploads a nighttime
streetlight image, the model classifies it, and the app shows the prediction
(green for Working, red for Broken) with a confidence percentage.

Pages in the app:

| Page | What it does |
|---|---|
| 🏠 Home | Project title, description, and a **Start Detection** button |
| 📤 Upload | Upload a JPG/JPEG/PNG image, preview it, press **Detect** |
| 📊 Prediction | Shows the image, the prediction, and the confidence % |
| ℹ️ About | Problem statement, objectives, advantages, future scope, tech used |

---

## 2. Installation Steps

```bash
# 1. Go into the project folder
cd streetlight_project

# 2. (Recommended) create a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

# 3. Install the required libraries
pip install -r requirements.txt
```

---

## 3. Required Libraries

| Library | Why it is used |
|---|---|
| streamlit | Builds the web interface |
| tensorflow / keras | Loads MobileNetV2 and trains the classifier |
| opencv-python | Resizes and processes the images |
| numpy | Array maths |
| Pillow | Reads the uploaded image file |

---

## 4. How to Run

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

### Using your own dataset

Put your images into these two folders (folder names must match exactly):

```
dataset/
├── Working/    <- photos where the streetlight is ON
└── Broken/     <- photos where the streetlight is OFF or damaged
```

Then train the model:

```bash
python model/train_model.py
```

This creates `model/streetlight_model.h5`, which the app loads automatically.

> If no trained model file exists yet, the app still runs in a simple **demo
> mode** that uses image brightness, so you can test the interface first.

---

## 5. Folder Structure

```
streetlight_project/
│
├── app.py                  # Main Streamlit application (all 4 pages)
├── requirements.txt        # Libraries to install
├── README.md               # This file
├── REPORT.md               # Project report for submission
│
├── model/
│   ├── train_model.py      # Transfer-learning training script
│   └── streetlight_model.h5  (created after training)
│
├── dataset/
│   ├── Working/            # Your "working streetlight" images
│   └── Broken/             # Your "broken streetlight" images
│
├── utils/
│   ├── preprocess.py       # Reads + resizes + scales images
│   └── predict.py          # Loads the model and returns the prediction
│
└── assets/                 # Images/icons used by the interface
```

---

## 6. Tips for the Viva

- **Why MobileNetV2?** It is small, fast, and already knows general image
  features, so it works well even with a small dataset (transfer learning).
- **Why freeze the base model?** With few images, retraining everything would
  overfit. We only train the last small layers.
- **What is confidence?** The softmax output of the predicted class, shown as
  a percentage.