import streamlit as st
from PIL import Image
import numpy as np
import random
import io

st.set_page_config(page_title="AI Outfit Recommender", layout="wide")

st.title("🧥 AI Outfit Recommender")
st.caption("Upload your wardrobe and get outfit suggestions powered by basic color matching!")

# Initialize storage
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = {}

# Categories
categories = ["Topwear", "Bottomwear", "Outerwear", "Footwear"]

# Upload section (with multiple file support)
st.subheader("👕 Upload Your Wardrobe")
for category in categories:
    uploaded_files = st.file_uploader(
        f"Upload {category} Images", type=["jpg", "jpeg", "png"],
        accept_multiple_files=True, key=category
    )
    if uploaded_files:
        st.session_state.uploaded_images[category] = []
        for uploaded in uploaded_files[:10]:  # Limit to 10 images per category
            image = Image.open(uploaded).resize((160, 160))
            avg_color = np.mean(np.array(image.resize((40, 40))).reshape(-1, 3), axis=0)
            st.session_state.uploaded_images[category].append({
                "image": image,
                "avg_color": avg_color,
                "filename": uploaded.name
            })

# Color scoring function
def color_score(c1, c2):
    dist = np.linalg.norm(np.array(c1) - np.array(c2))
    score = 100 - min(dist / 4.5, 100)
    return score

# Outfit suggestion function
def generate_recommendation():
    uploaded_images = st.session_state.uploaded_images
    if "Topwear" in uploaded_images and "Bottomwear" in uploaded_images:
        top = random.choice(uploaded_images["Topwear"])
        bottom = random.choice(uploaded_images["Bottomwear"])
        score = int(color_score(top["avg_color"], bottom["avg_color"]))
        comment = "🔥 Perfectly Layered!" if score > 70 else "💡 Try Bolder Contrast"
        return top, bottom, score, comment
    return None, None, None, "Upload at least Topwear and Bottomwear."

# Suggest outfit
if st.button("👕 Suggest Outfit"):
    top, bottom, score, comment = generate_recommendation()

    if top and bottom:
        st.subheader("🎽 Your Suggested Outfit")
        cols = st.columns(4)

        cols[0].image(top["image"], caption="Topwear", use_column_width=True)
        cols[1].image(bottom["image"], caption="Bottomwear", use_column_width=True)

        if "Outerwear" in st.session_state.uploaded_images:
            outer_list = st.session_state.uploaded_images["Outerwear"]
            if outer_list:
                outer = random.choice(outer_list)
                cols[2].image(outer["image"], caption="Outerwear", use_column_width=True)

        if "Footwear" in st.session_state.uploaded_images:
            foot_list = st.session_state.uploaded_images["Footwear"]
            if foot_list:
                foot = random.choice(foot_list)
                cols[3].image(foot["image"], caption="Footwear", use_column_width=True)

        st.markdown(f"### 🎯 AI Match Score: **{score}%**")
        st.info(comment)
    else:
        st.warning("Upload both Topwear and Bottomwear to get an outfit suggestion.")

# Optional: Feedback
st.subheader("💬 Your Feedback")
feedback = st.text_area("What do you think of this outfit?", height=100)
if st.button("📤 Submit Feedback"):
    st.success("Thanks for your feedback!")
