"""
Train the streetlight classifier using transfer learning (MobileNetV2).

How to use:
1. Put your images inside:
       dataset/Working/   -> photos of streetlights that are ON
       dataset/Broken/    -> photos of streetlights that are OFF / damaged
2. From the project root run:
       python model/train_model.py
3. The trained model is saved as model/streetlight_model.h5
   The app picks it up automatically the next time you run it.
"""

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 5              # small number keeps training fast for a mini project
DATASET_DIR = "dataset"
OUTPUT_PATH = "model/streetlight_model.h5"

# ----------------------------------------------------------------------
# 1. Load the images from the dataset folders (80% train, 20% validation)
# ----------------------------------------------------------------------
datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    horizontal_flip=True,
    rotation_range=10,
)

train_data = datagen.flow_from_directory(
    DATASET_DIR, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE,
    class_mode="categorical", subset="training",
)
val_data = datagen.flow_from_directory(
    DATASET_DIR, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE,
    class_mode="categorical", subset="validation",
)

print("Classes found:", train_data.class_indices)  # {'Broken': 0, 'Working': 1}

# ----------------------------------------------------------------------
# 2. Build the model: pre-trained MobileNetV2 + a small new head
# ----------------------------------------------------------------------
base_model = MobileNetV2(
    weights="imagenet", include_top=False, input_shape=(224, 224, 3)
)
base_model.trainable = False  # keep the pre-trained knowledge frozen

x = GlobalAveragePooling2D()(base_model.output)
x = Dense(64, activation="relu")(x)
output = Dense(2, activation="softmax")(x)  # 2 classes: Broken / Working

model = Model(inputs=base_model.input, outputs=output)
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.summary()

# ----------------------------------------------------------------------
# 3. Train and save
# ----------------------------------------------------------------------
model.fit(train_data, validation_data=val_data, epochs=EPOCHS)
model.save(OUTPUT_PATH)
print(f"Model saved to {OUTPUT_PATH}")