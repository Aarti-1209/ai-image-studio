import streamlit as st
import random
import requests
import io
import zipfile
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="wide")

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6C63FF, #FF6B9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎨 AI Image Studio</p>', unsafe_allow_html=True)
st.caption("Turn your imagination into images ✨")

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {url, prompt, favorite, timestamp}

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []  # last used text prompts

if "total_generated" not in st.session_state:
    st.session_state.total_generated = 0

if "reuse_prompt" not in st.session_state:
    st.session_state.reuse_prompt = ""

# ---------------- SIDEBAR SETTINGS ----------------
st.sidebar.header("⚙️ Settings")

art_style = st.sidebar.selectbox(
    "Art Style",
    ["Realistic", "Anime", "Cyberpunk", "Watercolor", "Fantasy", "Oil Painting", "3D Render"]
)

# --- Aspect Ratio Presets ---
aspect = st.sidebar.radio("Aspect Ratio", ["Square (1:1)", "Portrait (9:16)", "Landscape (16:9)", "Custom"])
aspect_map = {
    "Square (1:1)": (512, 512),
    "Portrait (9:16)": (576, 1024),
    "Landscape (16:9)": (1024, 576)
}

if aspect == "Custom":
    width = st.sidebar.slider("Width", 256, 1024, 512)
    height = st.sidebar.slider("Height", 256, 1024, 512)
else:
    width, height = aspect_map[aspect]
    st.sidebar.caption(f"Size: {width} x {height}")

# --- Color Mood ---
color_mood = st.sidebar.select_slider(
    "Color Mood",
    options=["Warm", "Neutral", "Cool", "Vibrant", "Monochrome"],
    value="Neutral"
)

# --- Number of Variations ---
num_images = st.sidebar.slider("Number of Variations", 1, 4, 1)

# --- Magic Enhance ---
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# --- Negative Prompt ---
negative_prompt = st.sidebar.text_input("🚫 Negative Prompt (avoid these)", placeholder="blurry, low quality, extra limbs")

st.sidebar.divider()
st.sidebar.caption("Made with ❤️ using Streamlit + Pollinations AI")

# ---------------- SURPRISE PROMPTS ----------------
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon made of glass flying over a city",
    "A robot painting a self-portrait in Paris",
    "An underwater library guarded by jellyfish"
]

# ---------------- PROMPT PRESETS ----------------
preset = st.selectbox(
    "🎯 Quick Presets (optional)",
    ["Custom", "Portrait", "Landscape", "Product Shot", "Fantasy Character"]
)

presets = {
    "Portrait": "professional headshot portrait, studio lighting",
    "Landscape": "wide scenic landscape, golden hour",
    "Product Shot": "product photography, white background, studio lighting",
    "Fantasy Character": "fantasy character concept art, detailed armor"
}

default_prompt = presets[preset] if preset != "Custom" else ""
starting_value = st.session_state.reuse_prompt or default_prompt
prompt = st.text_input("Enter your prompt:", value=starting_value)
st.session_state.reuse_prompt = ""  # consume it after use

# --- Prompt length warning ---
if prompt:
    st.caption(f"Prompt length: {len(prompt)} characters")
    if len(prompt) > 500:
        st.warning("Bahut lamba prompt hai, chhota karo behtar results ke liye.")

# --- Quick word suggestion chips ---
st.caption("💡 Quick add:")
chip_words = ["cinematic lighting", "dramatic sky", "hyper-realistic", "pastel colors", "intricate details", "soft glow"]
chip_cols = st.columns(len(chip_words))
for i, word in enumerate(chip_words):
    if chip_cols[i].button(word, key=f"chip_{word}"):
        st.session_state.reuse_prompt = f"{prompt}, {word}" if prompt else word
        st.rerun()

# --- Reuse a past prompt ---
if st.session_state.prompt_history:
    with st.expander("🕒 Reuse a previous prompt"):
        past = st.selectbox(
            "Pick from your recent prompts",
            options=list(reversed(st.session_state.prompt_history)),
            key="past_prompt_select"
        )
        if st.button("Use this prompt"):
            st.session_state.reuse_prompt = past
            st.rerun()

# --- Random style shuffle ---
if st.button("🔀 Shuffle Art Style"):
    style_options = ["Realistic", "Anime", "Cyberpunk", "Watercolor", "Fantasy", "Oil Painting", "3D Render"]
    st.toast(f"Shuffled to a random style! Try generating again.")
    art_style = random.choice(style_options)


# ---------------- HELPER FUNCTIONS ----------------
def build_full_prompt(user_prompt):
    full_prompt = f"{user_prompt}, {art_style} style, {color_mood.lower()} color palette"

    if negative_prompt:
        full_prompt += f", avoid {negative_prompt}"

    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    return full_prompt


def fetch_image_bytes(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.content


def generate_image(user_prompt, count=1):
    full_prompt = build_full_prompt(user_prompt)

    st.code(full_prompt, language=None)
    st.caption("👆 Copy this prompt")

    # Track prompt history (keep last 10, no immediate duplicates)
    if user_prompt and (not st.session_state.prompt_history or st.session_state.prompt_history[-1] != user_prompt):
        st.session_state.prompt_history.append(user_prompt)
        st.session_state.prompt_history = st.session_state.prompt_history[-10:]

    with st.spinner("🎨 Creating your masterpiece..."):
        cols = st.columns(count)
        for i in range(count):
            seed = random.randint(1, 100000)
            url = f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}&seed={seed}"

            try:
                img_bytes = fetch_image_bytes(url)
                cols[i].image(img_bytes, caption=f"Variation {i + 1}")
                cols[i].download_button(
                    label="Download",
                    data=img_bytes,
                    file_name=f"{art_style}_image_{seed}.png",
                    mime="image/png",
                    key=f"download_{seed}_{i}"
                )
                st.session_state.history.append({
                    "url": url,
                    "prompt": full_prompt,
                    "favorite": False,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "seed": seed
                })
                st.session_state.total_generated += 1
            except Exception as e:
                cols[i].error(f"Could not generate image: {e}")


# ---------------- GENERATE / SURPRISE BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Generate", use_container_width=True):
        if prompt:
            generate_image(prompt, count=num_images)
        else:
            st.warning("Pehle prompt likho!")

with col2:
    if st.button("🎲 Surprise Me!", use_container_width=True):
        random_prompt = random.choice(surprise_prompts)
        st.write(f"**Surprise Prompt:** {random_prompt}")
        generate_image(random_prompt, count=num_images)

# ---------------- GALLERY / HISTORY ----------------
if st.session_state.history:
    st.divider()

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    stat_col1.metric("🖼️ Total Generated", st.session_state.total_generated)
    stat_col2.metric("❤️ Favorites", sum(1 for item in st.session_state.history if item["favorite"]))
    stat_col3.metric("📁 In Gallery", len(st.session_state.history))

    show_favorites_only = st.checkbox("⭐ Show favorites only")

    top_col1, top_col2 = st.columns(2)
    with top_col1:
        if st.button("🗑️ Clear Gallery"):
            st.session_state.history = []
            st.rerun()

    with top_col2:
        # Build a ZIP of all images in memory for one-click download
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for item in st.session_state.history:
                try:
                    img_bytes = fetch_image_bytes(item["url"])
                    zip_file.writestr(f"image_{item['seed']}.png", img_bytes)
                except Exception:
                    pass
        st.download_button(
            "📦 Download All as ZIP",
            data=zip_buffer.getvalue(),
            file_name="ai_image_studio_gallery.zip",
            mime="application/zip"
        )

    st.subheader("🖼️ Your Gallery")

    items_to_show = [item for item in st.session_state.history if item["favorite"]] if show_favorites_only else st.session_state.history

    gallery_cols = st.columns(4)
    for idx, item in enumerate(reversed(items_to_show)):
        col = gallery_cols[idx % 4]
        col.image(item["url"], width=150)
        col.caption(f"🕒 {item['timestamp']}")
        fav_label = "💔 Unfavorite" if item["favorite"] else "❤️ Favorite"
        if col.button(fav_label, key=f"fav_{item['seed']}_{idx}"):
            item["favorite"] = not item["favorite"]
            st.rerun()

# ---------------- FOOTER ----------------
st.divider()
st.caption("Built with Streamlit + Pollinations AI · MirAI School of Technology Internship Project")