
import streamlit as st
from gtts import gTTS
import os
import tempfile

st.set_page_config(page_title="TTS: Khmer, English, Vietnamese, Korean, Chinese", layout="centered")

# Toggle theme
theme = st.radio("Theme", ["Light", "Dark"], horizontal=True)

if theme == "Dark":
    st.markdown(
        "<style>body, .stApp { background-color: #1e1e1e; color: white; }"
        "textarea, select, .stButton>button { background-color: #2a2a2a; color: white; }</style>",
        unsafe_allow_html=True,
    )

# Logo / Title
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🌍 Multi-Language Text-to-Speech</h1>"
    "<h4 style='text-align: center;'>Khmer | English | Vietnamese | Korean | Chinese</h4>",
    unsafe_allow_html=True
)

# Text input
text = st.text_area("✍️ Enter text / បញ្ចូលអត្ថបទ / Nhập văn bản / 텍스트 입력 / 输入文本：", height=150)

# Language and speed
col1, col2 = st.columns(2)

with col1:
    language = st.selectbox("🌐 Language", ["Khmer", "English", "Vietnamese", "Korean", "Chinese"])
    lang_map = {
        "Khmer": "km",
        "English": "en",
        "Vietnamese": "vi",
        "Korean": "ko",
        "Chinese": "zh-CN"
    }
    lang_code = lang_map[language]

with col2:
    speed = st.selectbox("🎚 Voice Speed", ["Normal", "Slow"])
    slow = True if speed == "Slow" else False

# Buttons
speak_button = st.button("🔊 Speak")
save_button = st.button("💾 Save MP3")

if speak_button or save_button:
    if text.strip():
        tts = gTTS(text=text, lang=lang_code, slow=slow)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)

            if speak_button:
                st.audio(tmp.name, format="audio/mp3")
            elif save_button:
                with open(tmp.name, "rb") as f:
                    st.download_button(
                        label="⬇️ Download MP3",
                        data=f,
                        file_name="tts_output.mp3",
                        mime="audio/mp3"
                    )
            os.remove(tmp.name)
    else:
        st.warning("⚠️ Please enter text first!")
