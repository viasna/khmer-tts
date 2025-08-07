
import streamlit as st
from google.cloud import texttospeech
import base64

# App title and layout
st.set_page_config(page_title="Smart TTS", layout="centered")
st.markdown("<h1 style='text-align: center;'>Smart Text-to-Speech (TTS)</h1>", unsafe_allow_html=True)

# Text input area
text_input = st.text_area("Enter your text:", height=200, placeholder="Type your text here...")

# Manual language selection (no auto-detection)
language = st.selectbox("Choose language:", ["Khmer 🇰🇭", "English 🇬🇧", "Vietnamese 🇻🇳"])

# Gender and speed
gender = st.selectbox("Voice type:", ["Male", "Female", "Child"])
speed = st.select_slider("Speech Speed", options=["Slow", "Normal", "Fast", "Super Fast"], value="Normal")
pitch = st.slider("Voice Pitch", min_value=-20.0, max_value=20.0, value=0.0)

# Paste & clear buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Paste"):
        st.warning("Paste manually using your device's keyboard (Ctrl+V or long-press).")
with col2:
    if st.button("Clear"):
        text_input = ""

# Voice config mapping
language_codes = {
    "Khmer 🇰🇭": "km-KH",
    "English 🇬🇧": "en-US",
    "Vietnamese 🇻🇳": "vi-VN"
}

voice_profiles = {
    ("en-US", "Male"): "en-US-Wavenet-D",
    ("en-US", "Female"): "en-US-Wavenet-F",
    ("en-US", "Child"): "en-US-Wavenet-E",
    ("km-KH", "Male"): "km-KH-Wavenet-B",
    ("km-KH", "Female"): "km-KH-Wavenet-A",
    ("km-KH", "Child"): "km-KH-Wavenet-A",
    ("vi-VN", "Male"): "vi-VN-Wavenet-B",
    ("vi-VN", "Female"): "vi-VN-Wavenet-A",
    ("vi-VN", "Child"): "vi-VN-Wavenet-C"
}

speed_map = {
    "Slow": 0.75,
    "Normal": 1.0,
    "Fast": 1.25,
    "Super Fast": 1.5
}

# Google TTS client setup
client = texttospeech.TextToSpeechClient()

if st.button("🔊 Generate Speech") and text_input.strip() != "":
    with st.spinner("Generating voice..."):
        input_text = texttospeech.SynthesisInput(text=text_input)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_codes[language],
            name=voice_profiles[(language_codes[language], gender)]
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed_map[speed],
            pitch=pitch
        )
        response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
        st.audio(response.audio_content, format="audio/mp3")

        # Save MP3 for download
        mp3_path = Path("tts_output.mp3")
        mp3_path.write_bytes(response.audio_content)
        with open(mp3_path, "rb") as file:
            b64 = base64.b64encode(file.read()).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="tts_output.mp3">📥 Download MP3</a>'
            st.markdown(href, unsafe_allow_html=True)

        st.success("✅ Speech ready!")
