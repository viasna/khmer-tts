import streamlit as st
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Smart TTS", layout="centered", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center;'>🎙️ Smart TTS</h1>", unsafe_allow_html=True)

st.markdown("### Choose a language")
language = st.selectbox("Choose a language", ["Khmer 🇰🇭", "English 🇬🇧", "Vietnamese 🇻🇳"], label_visibility="collapsed")

lang_code = {"Khmer 🇰🇭": "km", "English 🇬🇧": "en", "Vietnamese 🇻🇳": "vi"}.get(language, "km")

st.markdown("### Enter your text below:")
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
text_input = st.text_area("Text to Convert", value=st.session_state.text_input, height=150, label_visibility="collapsed", key="text_input")

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🧹 Clear"):
        st.session_state.text_input = ""
with col2:
    if st.button("📋 Paste"):
        st.session_state.text_input = st.experimental_get_query_params().get("paste", [""])[0]
with col3:
    speak = st.button("🗣️ Speak")

playback_speed = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.1)

if speak and st.session_state.text_input.strip():
    tts = gTTS(text=st.session_state.text_input, lang=lang_code)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    audio_path = tmp_file.name

    st.success("✅ Speech generated!")
    st.audio(audio_path)

    with open(audio_path, "rb") as audio_file:
        st.download_button("⬇️ Download MP3", data=audio_file, file_name="tts_output.mp3", mime="audio/mpeg")

    st.markdown(
        '<a href="https://www.facebook.com/sharer/sharer.php?u=https://yourdomain.com/tts_output.mp3" target="_blank">🔗 Share the downloaded MP3 file manually to social media</a>',
        unsafe_allow_html=True)