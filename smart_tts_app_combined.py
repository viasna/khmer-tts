
import streamlit as st
import os
import tempfile

# Free TTS (gTTS)
from gtts import gTTS

# Pro TTS (Google Cloud)
from langdetect import detect
from google.cloud import texttospeech

# App UI
st.set_page_config(page_title="Smart TTS - Speak Any Language", layout="centered")

st.markdown("<h1 style='text-align:center;'>🗣️ Smart TTS – Speak Any Language</h1>", unsafe_allow_html=True)
st.caption("Supports Khmer, English, Vietnamese, Korean, Chinese – with voice speed, native voices, and MP3 download.")

# Mode selection
mode = st.radio("🎛 Select Mode", ["Free Mode (gTTS)", "Pro Mode (Google Cloud)"])

# Text input
text = st.text_area("✍️ Enter or paste your text:", height=150)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📋 Paste"):
        try:
            import pyperclip
            pasted_text = pyperclip.paste()
            st.session_state["pasted"] = pasted_text
        except:
            st.warning("Clipboard not supported in Streamlit Cloud.")
with col_btn2:
    if st.button("🧹 Clear"):
        text = ""
        st.session_state["pasted"] = ""

if "pasted" in st.session_state:
    text = st.session_state["pasted"]
    st.session_state["pasted"] = ""

# Language detection and manual selection
detected_lang = detect(text) if text.strip() else "unknown"
lang_display = {
    "km": "Khmer",
    "en": "English",
    "vi": "Vietnamese",
    "ko": "Korean",
    "zh-cn": "Chinese"
}
language = st.selectbox("🌐 Language (Auto-detected: {})".format(lang_display.get(detected_lang, "unknown")),
                        ["Auto", "Khmer", "English", "Vietnamese", "Korean", "Chinese"])

lang_code_map = {
    "Khmer": "km",
    "English": "en",
    "Vietnamese": "vi",
    "Korean": "ko",
    "Chinese": "zh-CN"
}
lang_code = lang_code_map.get(language, detected_lang if detected_lang in lang_code_map.values() else "en")

# Speed control
speed_option = st.selectbox("🎚 Voice Speed", ["Super Fast", "Fast", "Normal", "Slow"])
speed_factor = {
    "Super Fast": 1.4,
    "Fast": 1.2,
    "Normal": 1.0,
    "Slow": 0.85
}[speed_option]

# Pro Mode: upload JSON key and choose voice
if mode == "Pro Mode (Google Cloud)":
    st.sidebar.header("🔐 Google Cloud API Key")
    json_key = st.sidebar.file_uploader("Upload your JSON Key", type="json")

    voice_options = {
        "km": ["km-KH-Wavenet-A", "km-KH-Wavenet-B"],
        "en": ["en-US-Wavenet-D", "en-US-Wavenet-F"],
        "vi": ["vi-VN-Wavenet-A", "vi-VN-Wavenet-B"],
        "ko": ["ko-KR-Wavenet-A", "ko-KR-Wavenet-B"],
        "zh-CN": ["cmn-CN-Wavenet-A", "cmn-CN-Wavenet-B"]
    }

    voice_name = st.selectbox("👤 Choose Voice (Google Cloud)", voice_options.get(lang_code, ["en-US-Wavenet-D"]))

# Action buttons
col_a, col_b = st.columns(2)
speak = col_a.button("🔊 Speak")
save = col_b.button("💾 Download MP3")

# Helper: adjust MP3 speed
def change_speed(audio_path, rate=1.0):
    from pydub import AudioSegment
    sound = AudioSegment.from_file(audio_path, format="mp3")
    changed = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * rate)})
    changed = changed.set_frame_rate(44100)
    changed.export(audio_path, format="mp3")

# Processing
if speak or save:
    if text.strip():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name

        if mode == "Free Mode (gTTS)":
            tts = gTTS(text=text, lang=lang_code)
            tts.save(tmp_path)
            if speed_factor != 1.0:
                from pydub import AudioSegment
                change_speed(tmp_path, speed_factor)

        elif mode == "Pro Mode (Google Cloud)":
            if json_key is None:
                st.warning("⚠️ Please upload your Google Cloud JSON key.")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as keyfile:
                    keyfile.write(json_key.read())
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyfile.name

                client = texttospeech.TextToSpeechClient()
                synthesis_input = texttospeech.SynthesisInput(text=text)
                voice = texttospeech.VoiceSelectionParams(language_code=lang_code, name=voice_name)
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    speaking_rate=speed_factor
                )

                response = client.synthesize_speech(
                    input=synthesis_input, voice=voice, audio_config=audio_config
                )

                with open(tmp_path, "wb") as out:
                    out.write(response.audio_content)

        # Play and/or download
        if speak:
            st.audio(tmp_path, format="audio/mp3")
        if save:
            with open(tmp_path, "rb") as f:
                st.download_button("⬇️ Click to Download", f, "speech.mp3", mime="audio/mp3")

        os.remove(tmp_path)
    else:
        st.warning("⚠️ Please enter some text first.")
