# stylesage_web.py - Streamlit version (no Tkinter)
import streamlit as st
from PIL import Image
import numpy as np
import os
import random
from datetime import datetime

st.set_page_config(page_title="StyleSage", layout="centered")
st.title("👗 StyleSage - AI Fashion Stylist")

# --- Setup
categories = ["Topwear", "Bottomwear", "Outerwear", "Footwear"]
uploaded_images = {}

# --- Upload section
st.subheader("📤 Upload Your Outfit Items")

for category in categories:
    uploaded = st.file_uploader(f"Upload {category} Image", type=["jpg", "jpeg", "png"], key=category)
    if uploaded:
        image = Image.open(uploaded).resize((160, 160))
        uploaded_images[category] = {
            "image": image,
            "avg_color": np.mean(np.array(image.resize((40, 40))).reshape(-1, 3), axis=0),
            "filename": uploaded.name
        }

# --- AI Matching Logic
def color_score(color1, color2):
    diff = np.linalg.norm(np.array(color1) - np.array(color2))
    return 100 - min(diff, 100)

def generate_recommendation():
    score = None
    comment = ""
    
    if "Topwear" in uploaded_images and "Bottomwear" in uploaded_images:
        c1 = uploaded_images["Topwear"]["avg_color"]
        c2 = uploaded_images["Bottomwear"]["avg_color"]
        score = int(color_score(c1, c2))
        comment = "🔥 Perfectly Layered!" if score > 70 else "💡 Try Bolder Contrast"
    return score, comment

# --- Suggest Outfit
if st.button("👕 Suggest Outfit"):
    if "Topwear" in uploaded_images and "Bottomwear" in uploaded_images:
        st.subheader("🧠 AI Suggested Outfit")
        cols = st.columns(len(uploaded_images))
        for i, (cat, data) in enumerate(uploaded_images.items()):
            with cols[i]:
                st.image(data["image"], caption=cat, use_column_width=True)

        score, comment = generate_recommendation()
        st.markdown(f"### 🎯 AI Match Score: **{score}%**")
        st.info(comment)
    else:
        st.warning("Please upload at least **Topwear and Bottomwear** to get a suggestion.")

# --- Save Outfit
if st.button("💾 Save Outfit Info"):
    if uploaded_images:
        os.makedirs("saved_outfits", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outfit_{timestamp}.txt"
        with open(os.path.join("saved_outfits", filename), "w") as f:
            for cat, data in uploaded_images.items():
                f.write(f"{cat}: {data['filename']}\n")
        st.success(f"Outfit info saved as `{filename}`")
    else:
        st.warning("No outfit uploaded to save!")

# --- Feedback Section
st.markdown("---")
st.subheader("📝 Give Feedback")
feedback = st.text_area("Tell us how this AI stylist feels or what you'd like to see improved:")

if st.button("📬 Submit Feedback"):
    os.makedirs("feedback", exist_ok=True)
    with open("feedback/user_feedback.txt", "a") as f:
        f.write(f"{datetime.now()} - {feedback}\n")
    st.success("Thanks for your feedback!")

