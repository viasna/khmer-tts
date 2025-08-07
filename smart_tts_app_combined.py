import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
import os
import uuid
from langdetect import detect, LangDetectException
from google.cloud import texttospeech

st.set_page_config(page_title="Smart TTS", layout="centered", page_icon="🗣️")
st.title("🗣️ Smart TTS – Speak Any Language")
st.markdown("Supports Khmer, English, Vietnamese, Korean, Chinese – with voice speed, native voices, and MP3 download.")

st.radio("Select Mode", ["Free Mode (gTTS)", "Pro Mode (Google Cloud)"], key="mode")

text = st.text_area("📝 Enter or paste your text:")

col1, col2 = st.columns(2)
with col1:
    if st.button("📋 Paste"):
        st.session_state['paste'] = True
    if st.button("🧹 Clear"):
        st.experimental_rerun()

language = "auto"
if text.strip():
    try:
        detected_lang = detect(text)
    except LangDetectException:
        detected_lang = "auto"
    language = st.selectbox("🌐 Language (Auto-detected: " + detected_lang + ")", ["auto", "km", "en", "vi", "zh", "ko"])
else:
    st.info("Enter text above to detect language.")

voice_speed = st.selectbox("📄 Voice Speed", ["Slow", "Normal", "Fast", "Super Fast"])
voice_map = {"Slow": 0.75, "Normal": 1.0, "Fast": 1.25, "Super Fast": 1.5}

client = None
google_voice_id = st.selectbox("🧑‍🎤 Choose Voice (Google Cloud)", [
    "en-US-Wavenet-D", "en-US-Wavenet-F", "km-KH-Standard-A", "vi-VN-Standard-A",
    "zh-CN-Standard-A", "ko-KR-Standard-A"
])

if st.button("🗣️ Speak"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        if st.session_state.mode == "Free Mode (gTTS)":
            tts = gTTS(text, lang=detected_lang if language == "auto" else language)
            file_path = f"{uuid.uuid4().hex}.mp3"
            tts.save(file_path)
        else:
            try:
                client = texttospeech.TextToSpeechClient()
                synthesis_input = texttospeech.SynthesisInput(text=text)
                voice = texttospeech.VoiceSelectionParams(
                    language_code=language if language != "auto" else detected_lang,
                    name=google_voice_id
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=voice_map.get(voice_speed, 1.0)
                )
                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )
                file_path = f"{uuid.uuid4().hex}.mp3"
                with open(file_path, "wb") as out:
                    out.write(response.audio_content)
            except Exception as e:
                st.error("Google Cloud TTS Error: " + str(e))
                file_path = None

        if file_path and os.path.exists(file_path):
            st.audio(file_path, format="audio/mp3")
            st.download_button("💾 Download MP3", data=open(file_path, "rb"), file_name="tts_output.mp3", mime="audio/mp3")
