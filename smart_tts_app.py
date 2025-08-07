
import streamlit as st
import tempfile
from gtts import gTTS
import base64
import os

# App title and layout
st.set_page_config(page_title="Smart TTS with Native Voices", layout="centered", initial_sidebar_state="auto")
st.markdown("<h1 style='text-align: center;'>🔊 Smart TTS with Native Voices</h1>", unsafe_allow_html=True)

# Language and voice options
languages = {
    "Khmer 🇰🇭": "km",
    "English 🇬🇧": "en",
    "Vietnamese 🇻🇳": "vi"
}
voice_types = ["Man", "Woman", "Child"]

# Sidebar selections
selected_lang = st.selectbox("Select Language", list(languages.keys()))
selected_voice = st.selectbox("Select Voice Type", voice_types)

# Text input with persistent session state
if "text_input" not in st.session_state:
    st.session_state["text_input"] = ""

# Action buttons
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("🧹 Clear"):
        st.session_state["text_input"] = ""
with col2:
    if st.button("📋 Paste"):
        st.info("📋 Please use Ctrl+V (or long press on mobile) to paste text manually.")
with col3:
    speak_now = st.button("🗣️ Speak")

# Main text area
text_input = st.text_area("Enter your text below:", value=st.session_state["text_input"], height=150, key="text_input")

# Playback speed slider
speed = st.slider("Playback Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# Processing
if speak_now and text_input.strip():
    lang_code = languages[selected_lang]
    tts = gTTS(text=text_input, lang=lang_code, slow=False)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        audio_path = f.name

    st.success("✅ Speech generated!")
    st.audio(audio_path)

    # MP3 download
    with open(audio_path, "rb") as f:
        mp3 = f.read()
    b64 = base64.b64encode(mp3).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="tts_output.mp3">📥 Download MP3</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Share instruction
    st.info("🔗 Share the downloaded MP3 file manually to social media.")
