import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# ------------------------------
# Load Model (FIXED - no crash)
# ------------------------------

@st.cache_resource
def load_my_model():
    return load_model("model.keras")  # or model.h5 if you didn't change

model = load_my_model()

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="Digit Recognizer", page_icon="🧠", layout="centered")

# ------------------------------
# UI Styling
# ------------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00c3ff;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Title
# ------------------------------
st.title("🧠 Handwritten Digit Recognizer")
st.markdown("### Upload or Draw a digit (0–9)")

# ------------------------------
# Model Info
# ------------------------------
st.subheader("📈 Model Performance")
st.write("Accuracy: ~99.5% on MNIST dataset")

# ------------------------------
# Preprocessing (FIXED)
# ------------------------------
def preprocess_image(img):
    img = cv2.resize(img, (28, 28))

    # Normalize
    img = img / 255.0

    # Invert ONLY if needed
    if np.mean(img) > 0.5:
        img = 1 - img

    img = img.reshape(1, 28, 28, 1)
    return img

# ------------------------------
# Upload Section
# ------------------------------
st.subheader("📤 Upload Image")

uploaded_file = st.file_uploader("Upload a digit image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('L')
    st.image(image, caption="Uploaded Image", width=150)

    img = np.array(image)
    processed_img = preprocess_image(img)

    prediction = model.predict(processed_img, verbose=0)
    digit = np.argmax(prediction)
    confidence = np.max(prediction)

    st.success(f"🎯 Predicted Digit: {digit}")
    st.info(f"Confidence: {confidence:.2f}")
    st.bar_chart(prediction[0])

# ------------------------------
# Draw Section (FIXED)
# ------------------------------
st.subheader("✍️ Draw Digit")

canvas_result = st_canvas(
    fill_color="black",
    stroke_width=20,
    stroke_color="white",
    background_color="black",
    height=200,
    width=200,
    drawing_mode="freedraw",
    key="canvas",
)

if canvas_result.image_data is not None:
    img = canvas_result.image_data[:, :, 0]

    processed_img = preprocess_image(img)

    prediction = model.predict(processed_img, verbose=0)
    digit = np.argmax(prediction)
    confidence = np.max(prediction)

    st.success(f"🎯 Drawn Digit: {digit}")
    st.info(f"Confidence: {confidence:.2f}")
    st.bar_chart(prediction[0])
