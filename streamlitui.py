import streamlit as st
import os
import sys
import time

# Page configuration
st.set_page_config(
    page_title="Hate Speech Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main title styling */
    .main-title {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }

    .main-title h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
        margin-bottom: 0.3rem;
    }

    .main-title p {
        color: #8892b0;
        font-size: 1.05rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* Shield icon */
    .shield-icon {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: -0.5rem;
        filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.4));
    }

    /* Card styling */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .glass-card h3 {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 1.15rem;
        margin-bottom: 1rem;
    }

    /* Text area styling */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
    }

    .stTextArea textarea::placeholder {
        color: #4a5568 !important;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Result cards */
    .result-safe {
        background: linear-gradient(135deg, rgba(72, 187, 120, 0.1) 0%, rgba(56, 178, 172, 0.08) 100%);
        border: 1px solid rgba(72, 187, 120, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
        text-align: center;
        animation: fadeIn 0.5s ease-out;
    }

    .result-safe .result-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .result-safe .result-label {
        color: #48bb78;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .result-safe .result-desc {
        color: #68d391;
        font-size: 0.9rem;
        font-weight: 300;
    }

    .result-hate {
        background: linear-gradient(135deg, rgba(245, 101, 101, 0.1) 0%, rgba(237, 100, 166, 0.08) 100%);
        border: 1px solid rgba(245, 101, 101, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
        text-align: center;
        animation: fadeIn 0.5s ease-out;
    }

    .result-hate .result-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .result-hate .result-label {
        color: #f56565;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .result-hate .result-desc {
        color: #fc8181;
        font-size: 0.9rem;
        font-weight: 300;
    }

    /* Status cards */
    .status-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .status-dot-green {
        width: 8px;
        height: 8px;
        background: #48bb78;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(72, 187, 120, 0.5);
        display: inline-block;
    }

    .status-dot-red {
        width: 8px;
        height: 8px;
        background: #f56565;
        border-radius: 50%;
        box-shadow: 0 0 8px rgba(245, 101, 101, 0.5);
        display: inline-block;
    }

    .status-text {
        color: #a0aec0;
        font-size: 0.85rem;
    }

    /* Info section */
    .info-section {
        background: rgba(102, 126, 234, 0.06);
        border: 1px solid rgba(102, 126, 234, 0.15);
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1.5rem;
    }

    .info-section h4 {
        color: #667eea;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .info-section p {
        color: #718096;
        font-size: 0.82rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
        margin: 1.5rem 0;
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #4a5568;
        font-size: 0.78rem;
        letter-spacing: 0.5px;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Tabs / expander */
    .stExpander {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
    }

    /* Success / Error messages */
    .stSuccess {
        background: rgba(72, 187, 120, 0.1) !important;
        border: 1px solid rgba(72, 187, 120, 0.2) !important;
        border-radius: 12px !important;
    }

    .stError {
        background: rgba(245, 101, 101, 0.1) !important;
        border: 1px solid rgba(245, 101, 101, 0.2) !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)


def check_model_exists():
    """Check if a trained model is available."""
    model_name = "model.h5"
    paths_to_check = [
        os.path.join("artifacts", "PredictModel", model_name),
        os.path.join("artifacts", "best_model", model_name),
    ]
    for path in paths_to_check:
        if os.path.exists(path):
            return True

    # Check timestamped artifact directories
    artifacts_base = os.path.join(os.getcwd(), "artifacts")
    if os.path.exists(artifacts_base):
        for dir_name in sorted(os.listdir(artifacts_base), reverse=True):
            candidate = os.path.join(artifacts_base, dir_name, "ModelTrainerArtifacts", model_name)
            if os.path.exists(candidate):
                return True
    return False


# ── Header ──────────────────────────────────────────────
st.markdown('<div class="shield-icon">🛡️</div>', unsafe_allow_html=True)
st.markdown("""
<div class="main-title">
    <h1>Hate Speech Detector</h1>
    
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ── Model Status ────────────────────────────────────────
model_ready = check_model_exists()

if model_ready:
    st.markdown("""
    <div class="status-card">
        <span class="status-dot-green"></span>
        <span class="status-text">Model loaded and ready for predictions</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="status-card">
        <span class="status-dot-red"></span>
        <span class="status-text">No trained model found — train one below</span>
    </div>
    """, unsafe_allow_html=True)


# ── Prediction Section ──────────────────────────────────
st.markdown("""
<div class="glass-card">
    <h3>🔍 Analyze Text</h3>
</div>
""", unsafe_allow_html=True)

user_text = st.text_area(
    label="Enter text to analyze",
    placeholder="Type or paste any text here to check for hate speech...",
    height=130,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_clicked = st.button("⚡ Analyze Text", use_container_width=True)

if predict_clicked:
    if not user_text.strip():
        st.warning("Please enter some text to analyze.")
    elif not model_ready:
        st.error("No trained model available. Please train the model first using the section below.")
    else:
        with st.spinner("Analyzing..."):
            try:
                from hate.pipeline.prediction_pipeline import PredictionPipeline
                pipeline = PredictionPipeline()
                result = pipeline.run_pipeline(user_text)

                if "no hate" in result.lower():
                    st.markdown("""
                    <div class="result-safe">
                        <div class="result-icon"></div>
                        <div class="result-label">Safe Content</div>
                        <div class="result-desc">No hate speech or abusive language detected</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result-hate">
                        <div class="result-icon"></div>
                        <div class="result-label">Hate & Abusive Content Detected</div>
                        <div class="result-desc">This text contains potentially harmful language</div>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Prediction failed: {str(e)}")


st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ── Training Section ────────────────────────────────────
with st.expander("Train Model", expanded=not model_ready):
    st.markdown("""
    <div style="color: #a0aec0; font-size: 0.9rem; margin-bottom: 1rem; line-height: 1.6;">
        Train the hate speech classification model using your local dataset.
        This may take several minutes depending on your hardware.
    </div>
    """, unsafe_allow_html=True)

    train_col1, train_col2, train_col3 = st.columns([1, 2, 1])
    with train_col2:
        train_clicked = st.button("Start Training", use_container_width=True)

    if train_clicked:
        progress_bar = st.progress(0, text="Initializing training pipeline...")
        status_text = st.empty()

        try:
            from hate.pipeline.train_pipeline import TrainPipeline

            status_text.info("Starting data ingestion...")
            progress_bar.progress(10, text="Data ingestion in progress...")

            train_pipeline = TrainPipeline()
            train_pipeline.run_pipeline()

            progress_bar.progress(100, text="Training complete!")
            status_text.empty()

            st.success("Model trained successfully! You can now analyze text above.")
            st.balloons()

            # Force recheck
            time.sleep(1)
            st.rerun()

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Training failed: {str(e)}")


# ── Info Section ────────────────────────────────────────
# st.markdown("""
# <div class="info-section">
#     <h4>ℹ️ About this App</h4>
#     <p>
#         This application uses a deep learning LSTM model to classify text as 
#         <strong>safe</strong> or <strong>hate/abusive</strong>. The model is trained on 
#         labeled tweet data and uses NLP techniques including tokenization, 
#         sequence padding, and text preprocessing to make predictions.
#     </p>
# </div>
# """, unsafe_allow_html=True)

# ── Footer ──────────────────────────────────────────────
# st.markdown("""
# <div class="custom-footer">
#     Built with Streamlit • Powered by TensorFlow & Keras
# </div>
# """, unsafe_allow_html=True)
