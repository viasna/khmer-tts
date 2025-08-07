
import streamlit as st
from gtts import gTTS
import base64
import os
import tempfile
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

st.set_page_config(page_title="Smart TTS", layout="centered", initial_sidebar_state="auto")
st.markdown("<h1 style='text-align: center;'>💡 Smart TTS</h1>", unsafe_allow_html=True)

lang_options = {
    "Khmer 🇰🇭": "km",
    "English 🇬🇧": "en",
    "Vietnamese 🇻🇳": "vi"
}

lang = st.selectbox("Choose a language", options=list(lang_options.keys()))
lang_code = lang_options[lang]

text = st.text_area("Enter your text below:", height=200, key="text_input")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🧹 Clear"):
        st.session_state["text_input"] = ""
with col2:
    if st.button("📋 Paste"):
        st.warning("Please paste manually on mobile. Clipboard access is restricted.")
with col3:
    speak = st.button("🔊 Speak")

# Playback speed
speed = st.slider("🔁 Playback Speed", min_value=0.5, max_value=2.0, step=0.1, value=1.0)

def convert_and_play(text, lang_code, speed):
    tts = gTTS(text=text, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        sound = AudioSegment.from_mp3(fp.name)
        if speed != 1.0:
            sound = sound._spawn(sound.raw_data, overrides={
                "frame_rate": int(sound.frame_rate * speed)
            }).set_frame_rate(sound.frame_rate)
        st.audio(fp.name, format="audio/mp3")
        b64 = base64.b64encode(open(fp.name, "rb").read()).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="tts_output.mp3">📥 Download MP3</a>'
        st.markdown(href, unsafe_allow_html=True)
        os.unlink(fp.name)

if speak and text.strip() != "":
    convert_and_play(text, lang_code, speed)
