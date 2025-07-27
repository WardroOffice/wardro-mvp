# stylesage_app.py - AI Enhanced Fashion Stylist with Modern UI

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import random
import numpy as np
from datetime import datetime

class StyleSageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StyleSage - AI Fashion Stylist")
        self.root.geometry("1020x780")
        self.root.configure(bg="#1f1f1f")

        self.categories = {
            "Topwear": [],
            "Bottomwear": [],
            "Outerwear": [],
            "Footwear": []
        }

        self.images = []
        self.outfit_paths = []

        self.build_ui()

    def build_ui(self):
        title = tk.Label(self.root, text="StyleSage - AI Fashion Stylist",
                         font=("Helvetica", 22, "bold"), bg="#1f1f1f", fg="#00e6e6")
        title.pack(pady=15)

        button_frame = tk.Frame(self.root, bg="#1f1f1f")
        button_frame.pack()

        for category in self.categories:
            btn = tk.Button(button_frame, text=f"Upload {category}", bg="#333", fg="white",
                            font=("Arial", 11), relief=tk.FLAT, command=lambda c=category: self.upload_image(c))
            btn.pack(side=tk.LEFT, padx=12, pady=10)

        suggest_btn = tk.Button(self.root, text="Suggest Outfit", font=("Arial", 14, "bold"),
                                bg="#00cc66", fg="white", relief=tk.FLAT, command=self.suggest_outfit)
        suggest_btn.pack(pady=10)

        save_btn = tk.Button(self.root, text="Save Outfit", font=("Arial", 12),
                             bg="#6600cc", fg="white", relief=tk.FLAT, command=self.save_outfit)
        save_btn.pack(pady=5)

        self.feedback = tk.Label(self.root, text="Upload clothes to begin!", font=("Arial", 13),
                                 bg="#1f1f1f", fg="#cccccc")
        self.feedback.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=950, height=420, bg="#ffffff", bd=2, relief=tk.RIDGE)
        self.canvas.pack(pady=15)

    def upload_image(self, category):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            try:
                img = Image.open(file_path).resize((160, 160))
                img_tk = ImageTk.PhotoImage(img)
                avg_color = self.get_average_color(img)
                self.categories[category].append((img_tk, file_path, avg_color))
                self.images.append(img_tk)
                self.feedback.config(text=f"{category} uploaded successfully.")
            except Exception as e:
                self.feedback.config(text=f"Error loading image: {str(e)}")

    def get_average_color(self, img):
        img = img.resize((40, 40))
        np_img = np.array(img)
        if len(np_img.shape) == 3:
            avg = np.mean(np_img.reshape(-1, 3), axis=0)
        else:
            avg = [np.mean(np_img)] * 3
        return tuple(avg.astype(int))

    def color_score(self, color1, color2):
        diff = np.linalg.norm(np.array(color1) - np.array(color2))
        return 100 - min(diff, 100)

    def ai_recommendation(self):
        # You can replace this with a real ML model later
        categories = [k for k in self.categories if self.categories[k]]
        outfit = [random.choice(self.categories[k]) if self.categories[k] else None for k in self.categories]
        return outfit

    def suggest_outfit(self):
        self.canvas.delete("all")
        self.outfit_paths = []

        if not self.categories["Topwear"] or not self.categories["Bottomwear"]:
            self.feedback.config(text="Upload at least Topwear and Bottomwear!")
            return

        outfit = self.ai_recommendation()
        self.outfit_paths = [item[1] for item in outfit if item]

        x = 60
        for item in outfit:
            if item:
                self.canvas.create_image(x, 110, anchor='nw', image=item[0])
                x += 220

        if outfit[0] and outfit[1]:
            score = self.color_score(outfit[0][2], outfit[1][2])
            comment = f"AI Match Score: {int(score)}% - {'🔥 Perfectly Layered!' if score > 70 else '💡 Try Bolder Contrast'}"
        else:
            comment = "Outfit suggested!"
        self.feedback.config(text=comment)

    def save_outfit(self):
        if not self.outfit_paths:
            self.feedback.config(text="No outfit to save!")
            return

        os.makedirs("saved_outfits", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outfit_{timestamp}.txt"
        path = os.path.join("saved_outfits", filename)

        with open(path, "w") as f:
            for p in self.outfit_paths:
                f.write(p + "\n")

        self.feedback.config(text=f"Outfit saved to {path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StyleSageApp(root)
    root.mainloop()

    import streamlit as st

    st.title("StyleSage: AI Style Recommender")

    user_input = st.text_input("Describe your vibe, event, or fashion interest:")

    if st.button("Get Recommendation"):
        if user_input:
            recommendation = get_style_recommendation(user_input)
            st.success(recommendation)
        else:
            st.warning("Please enter something to analyze.")



