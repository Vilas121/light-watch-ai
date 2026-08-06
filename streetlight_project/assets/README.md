# Assets folder

Put any images or icons used by the interface here, for example:

- `banner.png` — a header image for the Home page
- `sample_working.jpg` / `sample_broken.jpg` — demo images for the viva

Load one inside `app.py` like this:

```python
st.image("assets/banner.png", use_column_width=True)
```