
import streamlit as st
from gtts import gTTS
import os
import tempfile

st.set_page_config(page_title="Khmer Text-to-Speech", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>កម្មវិធីនិយាយអត្ថបទខ្មែរ</h1>",
    unsafe_allow_html=True
)

text = st.text_area("សូមវាយអត្ថបទខ្មែរ៖", height=150)

col1, col2 = st.columns([1, 1])
with col1:
    speed = st.selectbox("ល្បឿនសម្លេង", ["ធម្មតា", "យឺត"])
with col2:
    pitch = st.selectbox("ជម្រើសសំឡេង", ["ធម្មតា", "ខ្ពស់", "ទាប"])

speak_button = st.button("🔊 និយាយ")
save_button = st.button("💾 រក្សាទុកជា MP3")

def adjust_pitch(audio_path, pitch_level):
    from pydub import AudioSegment
    sound = AudioSegment.from_file(audio_path, format="mp3")
    if pitch_level == "ខ្ពស់":
        factor = 1.15
    elif pitch_level == "ទាប":
        factor = 0.85
    else:
        factor = 1.0
    changed = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * factor)
    }).set_frame_rate(44100)
    changed.export(audio_path, format="mp3")

if speak_button or save_button:
    if text.strip():
        slow = True if speed == "យឺត" else False
        tts = gTTS(text=text, lang='km', slow=slow)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            adjust_pitch(tmp.name, pitch)

            if speak_button:
                st.audio(tmp.name, format="audio/mp3")
            elif save_button:
                with open(tmp.name, "rb") as f:
                    st.download_button(
                        label="⬇️ ចុចដើម្បីទាញយក",
                        data=f,
                        file_name="khmer_speech.mp3",
                        mime="audio/mp3"
                    )
            os.unlink(tmp.name)
    else:
        st.warning("⚠️ សូមបញ្ចូលអត្ថបទមុននឹងចាប់ផ្តើម!")
