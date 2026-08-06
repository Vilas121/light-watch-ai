"""
Broken Streetlight Detection System
-----------------------------------
A beginner-friendly Streamlit app that classifies a nighttime streetlight
image as "Working Streetlight" or "Broken Streetlight".

Run it with:   streamlit run app.py
"""

import time

import streamlit as st
from PIL import Image

from utils.preprocess import read_image, preprocess_image
from utils.predict import predict_streetlight

# ----------------------------------------------------------------------
# 1. Basic page configuration (title, icon, layout)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Broken Streetlight Detection System",
    page_icon="💡",
    layout="wide",
)

# ----------------------------------------------------------------------
# 2. Simple blue & white theme using a little CSS
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
        .stApp { background-color: #f5f9ff; }
        h1, h2, h3 { color: #10406b; }
        .card {
            background: #ffffff;
            border: 1px solid #d8e6f5;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 4px 14px rgba(16, 64, 107, 0.08);
        }
        .result-ok  { color: #17803d; font-size: 30px; font-weight: 700; }
        .result-bad { color: #c1121f; font-size: 30px; font-weight: 700; }
        div.stButton > button {
            background-color: #1565c0;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
        }
        div.stButton > button:hover { background-color: #0d47a1; color: #ffffff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# 3. Session state: remembers which page we are on and the last result
# ----------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "result" not in st.session_state:
    st.session_state.result = None      # will hold (label, confidence)
if "image" not in st.session_state:
    st.session_state.image = None       # the uploaded PIL image


def go_to(page_name):
    """Small helper to switch pages."""
    st.session_state.page = page_name


# ----------------------------------------------------------------------
# 4. Sidebar navigation with icons
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 💡 Streetlight AI")
    st.caption("Beginner AI Mini Project")
    pages = ["🏠 Home", "📤 Upload", "📊 Prediction", "ℹ️ About"]
    # Keep the sidebar in sync with the current page
    current = {"Home": 0, "Upload": 1, "Prediction": 2, "About": 3}[st.session_state.page]
    choice = st.radio("Navigation", pages, index=current, label_visibility="collapsed")
    st.session_state.page = choice.split(" ", 1)[1]
    st.markdown("---")
    st.info("Model: MobileNetV2\nFramework: TensorFlow / Keras")

page = st.session_state.page

# ----------------------------------------------------------------------
# 5. HOME PAGE
# ----------------------------------------------------------------------
if page == "Home":
    st.title("💡 Broken Streetlight Detection System")
    st.subheader("Detect faulty street lamps from nighttime images using AI")

    st.markdown(
        """
        <div class="card">
        <p>Broken streetlights make roads unsafe at night, but city workers usually
        find them only by driving around and looking. This mini project uses a
        <b>pre-trained MobileNetV2 image classification model</b> to look at a
        nighttime photo of a streetlight and predict whether it is
        <b>Working</b> or <b>Broken</b>, along with a confidence score.</p>
        <p>Just upload a JPG, JPEG or PNG image and press <b>Detect</b>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    col1, col2, col3 = st.columns(3)
    col1.metric("Model", "MobileNetV2")
    col2.metric("Classes", "2")
    col3.metric("Input size", "224 x 224")

    st.write("")
    if st.button("🚀 Start Detection"):
        go_to("Upload")
        st.rerun()

# ----------------------------------------------------------------------
# 6. UPLOAD PAGE
# ----------------------------------------------------------------------
elif page == "Upload":
    st.title("📤 Upload Streetlight Image")
    st.write("Supported formats: **JPG, JPEG, PNG**")

    uploaded_file = st.file_uploader(
        "Choose a nighttime streetlight image",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is not None:
        # Convert the uploaded bytes into a PIL image and remember it
        image = read_image(uploaded_file)
        st.session_state.image = image
        st.image(image, caption="Uploaded image", width=420)

    if st.button("🔍 Detect"):
        # Error handling: user pressed Detect without uploading anything
        if st.session_state.image is None:
            st.error("⚠️ Please upload an image first before clicking Detect.")
        else:
            # Loading animation while the model runs
            with st.spinner("Analyzing the image, please wait..."):
                progress = st.progress(0)
                for percent in range(0, 100, 20):
                    time.sleep(0.1)
                    progress.progress(percent + 20)
                try:
                    array = preprocess_image(st.session_state.image)
                    label, confidence = predict_streetlight(array)
                    st.session_state.result = (label, confidence)
                    go_to("Prediction")
                    st.rerun()
                except Exception as error:  # simple, readable error handling
                    st.error(f"Something went wrong during prediction: {error}")

# ----------------------------------------------------------------------
# 7. PREDICTION PAGE
# ----------------------------------------------------------------------
elif page == "Prediction":
    st.title("📊 Prediction Result")

    if st.session_state.result is None or st.session_state.image is None:
        st.warning("No prediction yet. Please upload an image and click Detect.")
        if st.button("Go to Upload page"):
            go_to("Upload")
            st.rerun()
    else:
        label, confidence = st.session_state.result
        st.success("✅ Prediction completed successfully!")

        left, right = st.columns(2)
        with left:
            st.image(st.session_state.image, caption="Uploaded image", width=380)

        with right:
            css_class = "result-ok" if label == "Working Streetlight" else "result-bad"
            icon = "🟢" if label == "Working Streetlight" else "🔴"
            st.markdown(
                f"""
                <div class="card">
                    <p style="color:#5b7c9d;margin-bottom:4px;">Prediction</p>
                    <p class="{css_class}">{icon} {label}</p>
                    <p style="color:#5b7c9d;margin-bottom:4px;">Confidence</p>
                    <p style="font-size:26px;font-weight:700;color:#10406b;">
                        {confidence:.2f}%
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(int(confidence))

        st.write("")
        if st.button("🔁 Test another image"):
            st.session_state.image = None
            st.session_state.result = None
            go_to("Upload")
            st.rerun()

# ----------------------------------------------------------------------
# 8. ABOUT PAGE
# ----------------------------------------------------------------------
elif page == "About":
    st.title("ℹ️ About the Project")

    st.header("Problem Statement")
    st.write(
        "Municipal bodies have thousands of streetlights. Broken lamps are usually "
        "reported manually, which is slow and often incomplete, leaving roads dark "
        "and unsafe. An automatic image based checker can speed this up."
    )

    st.header("Objectives")
    st.markdown(
        """
        - Classify a nighttime streetlight image as **Working** or **Broken**.
        - Use transfer learning with the pre-trained **MobileNetV2** model.
        - Provide a simple web interface where anyone can upload an image.
        - Show the prediction along with a confidence percentage.
        """
    )

    st.header("Advantages")
    st.markdown(
        """
        - Fast and automatic – no manual inspection needed.
        - Low cost – works with ordinary phone photos.
        - Lightweight model that runs on a normal laptop.
        - Very simple interface, usable by non technical staff.
        """
    )

    st.header("Future Scope")
    st.markdown(
        """
        - Detect multiple streetlights in a single wide photo.
        - Add a mobile app for field workers.
        - Automatically generate maintenance reports.
        - Extend the model to detect dim or flickering lights, not just on/off.
        """
    )

    st.header("Technologies Used")
    st.markdown(
        """
        | Technology | Purpose |
        |---|---|
        | Python | Programming language |
        | Streamlit | Web interface |
        | TensorFlow / Keras | Deep learning model |
        | OpenCV | Image processing |
        | MobileNetV2 | Pre-trained CNN used for transfer learning |
        | NumPy | Numerical operations |
        """
    )