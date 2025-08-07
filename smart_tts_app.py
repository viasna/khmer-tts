
import streamlit as st
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Smart TTS", layout="centered", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center;'>🗣️ Smart TTS</h1>", unsafe_allow_html=True)

langs = {"Khmer 🇰🇭": "km", "English 🇬🇧": "en", "Vietnamese 🇻🇳": "vi"}
selected_lang = st.selectbox("Choose a language", list(langs.keys()))
lang_code = langs[selected_lang]

st.markdown("### Enter your text below:")

if "text_input" not in st.session_state:
    st.session_state.text_input = ""

def clear_text():
    st.session_state.text_input = ""

def paste_text():
    st.session_state.text_input = st.experimental_get_query_params().get("paste", [""])[0]

st.text_area("Text to Convert", key="text_input", height=200)

col1, col2, col3 = st.columns(3)
with col1:
    st.button("🧹 Clear", on_click=clear_text)
with col2:
    st.button("📋 Paste", on_click=paste_text)
with col3:
    if st.button("🔊 Speak"):
        if st.session_state.text_input.strip():
            tts = gTTS(st.session_state.text_input, lang=lang_code)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                tts.save(tmpfile.name)
                st.audio(tmpfile.name, format="audio/mp3")
                st.download_button("💾 Download MP3", data=open(tmpfile.name, "rb").read(),
                                   file_name="tts_output.mp3", mime="audio/mp3")
        else:
            st.warning("Please enter some text to speak.")
