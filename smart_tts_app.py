import streamlit as st
from gtts import gTTS
from langdetect import detect
from google.cloud import texttospeech
import os
from io import BytesIO

st.set_page_config(page_title="Smart TTS", layout="centered", page_icon="🗣️")

st.markdown("## 🗣️ Smart Text-to-Speech")
st.markdown("Easily convert your text into natural-sounding speech in Khmer, English, or Vietnamese.")

text_input = st.text_area("✏️ Enter text here", height=200)
voice_speed = st.selectbox("🎛️ Speed", ["Slow", "Normal", "Fast", "Super Fast"])
language_option = st.selectbox("🌐 Language", ["Auto Detect", "Khmer", "English", "Vietnamese"])
voice_type = st.selectbox("🎤 Voice Type", ["Female", "Male", "Child"])

# Convert button
if st.button("🔊 Generate Voice"):
    if not text_input.strip():
        st.warning("Please enter some text.")
    else:
        # Auto language detection
        lang_code = "km-KH"
        if language_option == "Auto Detect":
            detected_lang = detect(text_input)
            lang_code = "en-US" if detected_lang == "en" else "vi-VN" if detected_lang == "vi" else "km-KH"
        elif language_option == "English":
            lang_code = "en-US"
        elif language_option == "Vietnamese":
            lang_code = "vi-VN"
        elif language_option == "Khmer":
            lang_code = "km-KH"

        speed_mapping = {"Slow": 0.75, "Normal": 1.0, "Fast": 1.25, "Super Fast": 1.5}
        pitch_mapping = {"Female": 0.0, "Male": -2.0, "Child": 5.0}

        # Google TTS client
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text_input)
        voice = texttospeech.VoiceSelectionParams(language_code=lang_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=speed_mapping[voice_speed], pitch=pitch_mapping[voice_type])
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        # Playback and download
        st.audio(response.audio_content, format="audio/mp3")
        st.download_button("💾 Download MP3", response.audio_content, file_name="tts_output.mp3", mime="audio/mp3")