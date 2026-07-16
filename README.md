# 🎨 AI Image Studio

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
</p>

<p align="center">
  A polished, interactive AI image generator built with <b>Streamlit</b> and the <b>Pollinations AI</b> API.<br>
  Turn any text prompt into a custom AI-generated image — with full control over style, size, and enhancements.
</p>

<p align="center">
  Built during the <b>MirAI School of Technology Virtual Summer Internship 2026 — "AI Builder" Track"</b>
</p>

---

## 📋 Table of Contents

- [Demo](#-demo)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [What Was Fixed & Improved](#-what-was-fixed--improved)
- [Acknowledgements](#-acknowledgements)

---

## 🎥 Demo

**Watch the full walkthrough here:** [▶️ Demo Video](https://drive.google.com/file/d/1Yzp2ynq0WeOQWCS5knlOm9J_Y-zLzssq/view?usp=sharing)

*(The video shows live resizing via sliders, Magic Enhance, image generation, and downloading a working `.png` file.)*

---

## ✨ Features

| Category | Feature | Description |
|---|---|---|
| 🖼️ Core | Working sliders | Width & height sliders actually resize the generated image |
| 🖼️ Core | Correct file downloads | Downloads save as valid `.png` files, named by art style |
| 🖼️ Core | Magic Enhance | One click adds quality-boosting keywords to any prompt |
| 🖼️ Core | Surprise Me | Instantly generates an image from a random creative prompt |
| 🎨 Customization | Art styles | Realistic, Anime, Cyberpunk, Watercolor, Fantasy, and more |
| 🎨 Customization | Aspect ratio presets | Square, Portrait, Landscape, or fully custom dimensions |
| 🎨 Customization | Color mood control | Warm, cool, vibrant, monochrome palettes |
| 🎨 Customization | Negative prompts | Exclude unwanted elements from the output |
| ⚡ Productivity | Prompt presets | Ready-made templates (portrait, product shot, etc.) |
| ⚡ Productivity | Quick-add chips | One-click keyword boosters |
| ⚡ Productivity | Prompt history | Reuse your last 10 prompts |
| 📁 Gallery | Favorites | Mark and filter your favorite generations |
| 📁 Gallery | Bulk ZIP download | Download your entire gallery in one click |
| 📁 Gallery | Session stats | Track total images generated and favorited |

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Python web app framework for the UI
- **[Pollinations AI](https://pollinations.ai/)** — free text-to-image generation API
- **Python** standard libraries — `requests`, `random`, `zipfile`, `datetime`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/ai-image-studio.git
   cd ai-image-studio
   ```

2. **Create a virtual environment** *(recommended)*
   ```bash
   python -m venv venv
   source venv/bin/activate       # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open the local URL in your browser (usually `http://localhost:8501`).

---

## 📁 Project Structure

```
ai-image-studio/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Files/folders excluded from version control
└── README.md           # Project documentation (this file)
```

---

## 🐞 What Was Fixed & Improved

This project started as a working prototype with a few bugs, which were debugged and extended into a polished tool:

| Issue | Before | After |
|---|---|---|
| Sliders had no effect | Width/height values were never sent to the API | Values are appended as URL parameters, so images resize correctly |
| Broken downloads | Files saved without an extension (`my_ai_image`) | Files save as valid, dynamically-named `.png` files |
| No prompt enhancement | Users had to manually write quality keywords | "Magic Enhance" toggle auto-boosts any prompt |
| No inspiration option | Users faced writer's block with no fallback | "Surprise Me" button generates from a curated random list |

---

## 🙏 Acknowledgements

Built as part of the **MirAI School of Technology** Virtual Summer Internship 2026 — *AI Builder Track*.

Image generation powered by [Pollinations AI](https://pollinations.ai/).
