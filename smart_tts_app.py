
import streamlit as st
from langdetect import detect, LangDetectException
from gtts import gTTS
import tempfile
import os

def safe_detect_language(text, fallback="km"):
    try:
        return detect(text) if text.strip() else fallback
    except LangDetectException:
        return fallback

def generate_tts(text, lang, speed):
    tts = gTTS(text=text, lang=lang, slow=(speed == "Slow"))
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

st.set_page_config(page_title="Smart TTS – Speak Any Language", layout="centered", page_icon="🗣️")

st.title("🗣️ Smart TTS – Speak Any Language")
st.markdown("Supports Khmer, English, Vietnamese, Korean, Chinese – with voice speed, native voices, and MP3 download.")

text_input = st.text_area("Enter or paste your text:")
st.button("Paste", on_click=lambda: None)
if st.button("Clear"):
    text_input = ""

language = safe_detect_language(text_input)
st.markdown(f"**Detected Language**: `{language}`")

speed = st.selectbox("Voice Speed", ["Normal", "Slow"])

if st.button("Speak"):
    if text_input.strip():
        mp3_path = generate_tts(text_input, language, speed)
        st.audio(mp3_path)
        with open(mp3_path, "rb") as f:
            st.download_button("Download MP3", data=f, file_name="tts_output.mp3", mime="audio/mpeg")
        os.remove(mp3_path)
    else:
        st.warning("Please enter some text to generate speech.")
