# ui/app.py
import streamlit as st
import pandas as pd
import requests
import time
import warnings

# Suppress Streamlit future warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# ===================== CONFIG =====================
st.set_page_config(
    page_title="Agenti-AI Financial Insight Analyzer",
    page_icon="🤖",
    layout="wide",
)

# ------------------- DARK MATERIAL STYLE -------------------
st.markdown("""
    <style>
        body, .stApp {
            background-color: #0e1117;
            color: #f5f5f5;
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3, h4 {
            color: #fafafa;
            font-weight: 600;
        }
        .stButton>button {
            background: linear-gradient(135deg, #1f77b4, #0072ff);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-size: 1rem;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.02);
            background: linear-gradient(135deg, #0072ff, #1f77b4);
        }
        .metric-card {
            background: #1b1f27;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.4);
            margin-bottom: 1rem;
        }
        .processing-card {
            background: #1b1f27;
            padding: 1rem;
            border-radius: 10px;
            margin-top: 1rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
            text-align: center;
        }
        .progress-bar {
            width: 100%;
            height: 12px;
            background-color: #222831;
            border-radius: 6px;
            overflow: hidden;
            margin-top: 0.8rem;
        }
        .progress-inner {
            height: 12px;
            background: linear-gradient(90deg, #1f77b4, #0072ff);
            transition: width 0.3s ease;
        }
    </style>
""", unsafe_allow_html=True)

# =============================================================
# 🔹 BACKEND CONFIGURATION
# =============================================================
BACKEND_URL = "http://127.0.0.1:8000/analyze/"

# =============================================================
# 🔹 HEADER
# =============================================================
st.title("🤖 Agenti-AI Financial Insight Analyzer")
st.caption("AI-powered document and dataset intelligence • Gemini + FastAPI + Streamlit")

# =============================================================
# 🔹 SESSION STATE
# =============================================================
if "results" not in st.session_state:
    st.session_state.results = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# =============================================================
# 🔹 FILE UPLOAD + RESET BUTTON
# =============================================================
col1, col2 = st.columns([4, 1])
with col1:
    uploaded_files = st.file_uploader(
        "📂 Upload Financial Files (PDF, Images, CSV, Excel)",
        type=["pdf", "jpg", "jpeg", "png", "csv", "xlsx"],
        accept_multiple_files=True
    )
with col2:
    if st.button("🔁 Reset / Re-upload"):
        st.session_state.results = []
        st.session_state.processing = False
        st.rerun()

# =============================================================
# 🔹 PROCESS FILES
# =============================================================
if uploaded_files and not st.session_state.processing:
    st.session_state.processing = True
    st.session_state.results = []

    total_files = len(uploaded_files)
    progress_placeholder = st.empty()

    for idx, file in enumerate(uploaded_files, start=1):
        progress_percent = int((idx - 1) / total_files * 100)
        progress_placeholder.markdown(f"""
            <div class='processing-card'>
                <h3>🔄 Processing Files ({idx - 1}/{total_files})</h3>
                <p>Currently analyzing: <b>{file.name}</b></p>
                <div class='progress-bar'>
                    <div class='progress-inner' style='width:{progress_percent}%;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        try:
            files = {"file": (file.name, file.getvalue(), file.type)}
            response = requests.post(BACKEND_URL, files=files, timeout=120)

            if response.status_code == 200:
                data = response.json()
                data.setdefault("Latency (s)", 0)
                data.setdefault("CPU Usage (%)", 0)
                st.session_state.results.append(data)
            else:
                st.session_state.results.append({"Filename": file.name, "Error": response.text})
        except Exception as e:
            st.session_state.results.append({"Filename": file.name, "Error": str(e)})

        time.sleep(0.3)  # simulate smooth animation

    progress_placeholder.markdown(f"""
        <div class='processing-card'>
            <h3>✅ Processing Complete!</h3>
            <p>All {total_files} files analyzed successfully.</p>
            <div class='progress-bar'>
                <div class='progress-inner' style='width:100%;'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.processing = False

# =============================================================
# 🔹 DISPLAY RESULTS
# =============================================================
if st.session_state.results:
    st.subheader("📊 Analysis Results")

    df = pd.DataFrame(st.session_state.results)
    for col in df.columns:
        df[col] = df[col].astype(str)

    # --- Metrics ---
    def safe_mean(column):
        try:
            return df[column].astype(float).mean()
        except Exception:
            return 0.0

    avg_latency = safe_mean("Latency (s)")
    avg_cpu = safe_mean("CPU Usage (%)")

    st.markdown("### ⚙️ System Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h3>Processed Files</h3><p>{len(df)}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h3>Average Latency</h3><p>{avg_latency:.2f}s</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h3>Avg CPU Usage</h3><p>{avg_cpu:.1f}%</p></div>", unsafe_allow_html=True)

    # --- Dynamic Table (auto height per uploaded file) ---
    st.markdown("### 🧠 Gemini AI Insights")
    st.dataframe(df, width="stretch", height=min(120 + len(df) * 70, 600))

    # --- Download ---
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Full Results (CSV)",
        data=csv,
        file_name="gemini_financial_analysis.csv",
        mime="text/csv",
    )
else:
    st.info("📤 Upload one or more financial documents or datasets to begin analysis.")
