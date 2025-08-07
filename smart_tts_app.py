
import streamlit as st
from gtts import gTTS
import tempfile
import os

# App Title
st.set_page_config(page_title="Smart TTS", layout="centered", page_icon="🔊")
st.markdown("<h1 style='text-align: center;'>🔊 Smart TTS</h1>", unsafe_allow_html=True)

# Language Selection
lang = st.selectbox("Choose a language", ["Khmer 🇰🇭", "English 🇺🇸", "Vietnamese 🇻🇳"])
lang_code = {"Khmer 🇰🇭": "km", "English 🇺🇸": "en", "Vietnamese 🇻🇳": "vi"}[lang]

# Text Input Area
st.write("Enter your text below:")
text_input = st.text_area("Text to Convert", height=200, label_visibility="collapsed")

# Control Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🧹 Clear"):
        st.experimental_rerun()

with col2:
    if st.button("📋 Paste"):
        st.warning("Please paste manually using your keyboard (Ctrl+V or ⌘+V).")

with col3:
    speak = st.button("🔈 Speak")

# Playback Speed Selection
speed = st.slider("Playback Speed", min_value=0.5, max_value=2.0, step=0.1, value=1.0)

if speak and text_input.strip():
    with st.spinner("Generating speech..."):
        tts = gTTS(text=text_input, lang=lang_code)
        tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_path.name)
        st.success("✅ Speech generated!")

        # Audio Player
        st.audio(tmp_path.name, format="audio/mp3", start_time=0)

        # MP3 Download Button
        with open(tmp_path.name, "rb") as audio_file:
            st.download_button("⬇️ Download MP3", audio_file, file_name="tts_output.mp3")

        # Social Share Placeholder (non-functional on Streamlit)
        st.info("ℹ️ Share the downloaded MP3 file manually to social media.")

    # Clean up
    tmp_path.close()
