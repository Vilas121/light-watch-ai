# Dataset folder

Replace the sample folders with your own images. Keep the exact folder names:

```
dataset/
├── Working/   <- images where the streetlight is ON (glowing)
└── Broken/    <- images where the streetlight is OFF / damaged
```

Tips:
- 100–300 images per class is enough for a mini project.
- Use nighttime photos, JPG or PNG.
- Keep the two classes roughly balanced.

After adding images, train from the project root:

```bash
python model/train_model.py
```