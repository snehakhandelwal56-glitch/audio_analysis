import streamlit as st
from audio_analyzer import run_pipeline
import tempfile
import os

st.set_page_config(page_title="Meeting Intelligence Platform", layout="wide")

if "outputs" not in st.session_state:
    st.session_state["outputs"] = None

# -----------------------------
# 🎨 Styling
# -----------------------------
st.markdown("""
<style>
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 🧠 Header
# -----------------------------
st.title("Meeting Intelligence Platform")
st.caption("Automatically transform meeting recordings into structured, actionable insights — eliminating manual note-taking and improving execution clarity.")

# -----------------------------
# 📂 Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Audio File",
    type=["mp3", "wav", "m4a"]
)

# -----------------------------
# 🌍 Language  (Translation)
# -----------------------------
languages = [
    "Hindi",
    "English",
    "Spanish",
    "German",
    "Chinese",
    "Japanese",
    "Arabic"
]

selected_language = st.selectbox(
    "🌍 Select Translation Language",
    languages
)

target_language = selected_language  
# -----------------------------
# 🚀 Run
# -----------------------------
if st.button("Run Analysis"):
    if not uploaded_file:
        st.warning("Please upload an audio file first.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        try:
            with st.spinner("Running AI Agents..."):
                st.session_state["outputs"] = run_pipeline(temp_path, target_language)
            st.success("Analysis Complete!")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

outputs = st.session_state["outputs"]

if outputs:
    # -----------------------------
    # 🧾 Tabs (SEPARATE)
    # -----------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Final Report",
        "💡 Insights",
        "😊 Sentiment",
        "🌍 Translation",
        "📄 Transcript"
    ])

    # -----------------------------
    # 📊 Final Report
    # -----------------------------
    with tab1:
        st.subheader("Final Combined Report")
        st.write(outputs["final_report.txt"])

        st.download_button(
            "⬇ Download Report",
            outputs["final_report.txt"],
            file_name="final_report.txt",
            key="download_final_report"
        )

    # -----------------------------
    # 💡 Insights
    # -----------------------------
    with tab2:
        st.subheader("Key Insights")
        st.write(outputs["insights.txt"])

    # -----------------------------
    # 😊 Sentiment
    # -----------------------------
    with tab3:
        st.subheader("Sentiment Analysis")
        st.write(outputs["sentiment.txt"])

    # -----------------------------
    # 🌍 Translation
    # -----------------------------
    with tab4:
        st.subheader("Translation")
        st.write(outputs["translation.txt"])

        st.download_button(
            "⬇ Download Translation",
            outputs["translation.txt"],
            file_name="translation.txt",
            key="download_translation"
        )

    # -----------------------------
    # 📄 Transcript
    # -----------------------------
    with tab5:
        st.subheader("Transcript")
        st.write(outputs["transcript.txt"])

        st.download_button(
            "⬇ Download Transcript",
            outputs["transcript.txt"],
            file_name="transcript.txt",
            key="download_transcript"
        )