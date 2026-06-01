"""
🔍 Predict/Analysis Page - VisionInspect AI
"""

import streamlit as st
import cv2
import numpy as np
import joblib
import os
import tempfile
from PIL import Image
from pathlib import Path
from typing import Any

# Bring in your exact pipeline from src
from src.predict import load_inference_pipeline
from src.preprocessing import preprocess_image
from src.feature_extraction import extract_all_features

# ============================================================================
# PIPELINE CONFIGURATION
# ============================================================================

CLASS_NAMES = {0: "NORMAL", 1: "DEFECTIVE"}

def run_prediction_pipeline(file_path: str, model_name: str, scaler: Any):
    """
    Leverages the exact logic used in the CLI by passing a real file path string.
    This completely prevents the pathlib crash inside src/preprocessing.py.
    """
    # 1. Run through your real src preprocessing (takes a file path string)
    preprocessed_img, edge_map = preprocess_image(file_path)
    
    # 2. Extract the true 42 features
    features = extract_all_features(preprocessed_img, edge_map)
    
    # 3. Scale and format for the model
    features_2d = features.reshape(1, -1)
    features_scaled = scaler.transform(features_2d)
    
    # 4. Load the active model from session state
    models_dict = load_cached_models()
    model = models_dict[model_name]
    
    prediction = int(model.predict(features_scaled)[0])
    label = CLASS_NAMES[prediction]
    
    confidence = 0.85 # Fallback
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features_scaled)[0]
        confidence = float(np.max(probabilities))
        
    return label, confidence, preprocessed_img, edge_map

@st.cache_resource
def load_cached_models():
    """Cache models in memory for smooth UI performance."""
    models = {}
    paths = {"KNN": "models/knn.pkl", "SVM": "models/svm.pkl", "Random Forest": "models/rf.pkl"}
    for name, path in paths.items():
        if os.path.exists(path):
            models[name] = joblib.load(path)
    return models

@st.cache_resource
def load_cached_scaler():
    """Cache scaler in memory."""
    path = "models/scaler.pkl"
    if os.path.exists(path):
        return joblib.load(path)
    return None

# ============================================================================
# UI RENDERING
# ============================================================================

def show():
    # 1. Inject CSS to push the entire content block down
    st.markdown("""
        <style>
            /* Targets the main content area */
            [data-testid="stMainBlockContainer"] {
                padding-top: 6rem !important;
            }
            /* Optional: ensure the title has a bit of extra space regardless of global padding */
            .vi-page-title {
                margin-top: 1rem !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. Page Header
    st.markdown("""
    <div class="vi-page-title">🔍 Predict <span>Defects</span></div>
    <div class="vi-page-subtitle">
        Upload or capture a smartphone image — the computer vision pipeline handles the rest.
    </div>
    """, unsafe_allow_html=True)

    models = load_cached_models()
    scaler = load_cached_scaler()

    if not models or scaler is None:
        st.warning("⚠️ Trained models or feature scalers are missing from the `models/` directory.")
        return

    model_name = st.session_state.get("selected_model", "Random Forest")
    if model_name == "rf": model_name = "Random Forest"
    elif model_name == "svm": model_name = "SVM"
    elif model_name == "knn": model_name = "KNN"

    with st.expander("⚙️ Prediction settings", expanded=False):
        conf_threshold = st.slider(
            "Confidence threshold",
            min_value=0.50, max_value=1.0, value=0.70, step=0.05,
            help="Flag alerts when model confidence falls below this threshold value."
        )

    st.divider()

    col_input, col_result = st.columns(2, gap="large")
    
    # Store uploaded raw bytes safely
    uploaded_file_buffer = None
    display_image = None

    # LEFT COLUMN: Handle Inputs safely
    with col_input:
        st.markdown('<div class="vi-section-label">Input Image Source</div>', unsafe_allow_html=True)
        
        method = st.radio(
            "input_method",
            ["📁 Upload File", "📷 Camera Snapshot"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if method == "📁 Upload File":
            uploaded = st.file_uploader(
                "Drop image here",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
            )
            if uploaded is not None:
                display_image = uploaded
                uploaded_file_buffer = uploaded.getvalue()
        else:
            snap = st.camera_input("Take a photo", label_visibility="collapsed")
            if snap is not None:
                display_image = snap
                uploaded_file_buffer = snap.getvalue()

        if display_image is not None:
            st.markdown('<div class="vi-section-label" style="margin-top:1rem;">Original View</div>', unsafe_allow_html=True)
            st.image(display_image, use_container_width=True)

    # RIGHT COLUMN: Show Prediction Engine Results
    with col_result:
        st.markdown('<div class="vi-section-label">Analysis Result</div>', unsafe_allow_html=True)

        if uploaded_file_buffer is None:
            st.markdown("""
            <div class="vi-card" style="text-align:center; padding:2.5rem 1rem; color:var(--text-muted);">
                Provide an image source on the left to activate processing.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Executing Feature Extraction & Inference..."):
                # Create a temporary file on disk to get a real string path
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    temp_file.write(uploaded_file_buffer)
                    temp_file_path = temp_file.name

                try:
                    # Pass the real path string down the stream
                    label, conf, preprocessed_img, edge_map = run_prediction_pipeline(
                        temp_file_path, model_name, scaler
                    )
                finally:
                    # Clean up the disk file safely after inference completes
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

            badge_cls = "normal" if label == "NORMAL" else "defective"
            icon = "🟢" if label == "NORMAL" else "🔴"

            st.markdown(f"""
            <div class="vi-card" style="padding: 1.5rem;">
                <div style="margin-bottom: 0.75rem;">
                    <span class="vi-badge {badge_cls}">{icon} {label}</span>
                </div>
                <div style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.4rem;">
                    Confidence &nbsp;
                    <span style="font-family:var(--font-display); color:var(--accent); font-weight:700;">
                        {conf*100:.1f}%
                    </span>
                    &nbsp;·&nbsp; Engine: <strong>{model_name}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(float(conf))

            if conf < conf_threshold:
                st.warning(f"⚠️ Low Confidence warning: Result ({conf*100:.1f}%) sits below your threshold specification.")
            else:
                st.success("Analysis confidence parameters met ✓")

    # LOWER SECTION: Pipeline Stage Visualization
    if uploaded_file_buffer is not None:
        st.divider()
        st.markdown('<div class="vi-section-label">Handcrafted Feature Preprocessing Stages</div>', unsafe_allow_html=True)

        p1, p2 = st.columns(2, gap="medium")
        with p1:
            st.image(preprocessed_img, caption="1. Normalized Grayscale (128x128)", use_container_width=True)
        with p2:
            st.image(edge_map, caption="2. Structural Canny Edge Map Extract", use_container_width=True)

    # BATCH EXTRACTIONS
    st.divider()
    st.markdown('<div class="vi-section-label">Batch Testing Utility</div>', unsafe_allow_html=True)
    with st.expander("Process bulk directory evaluations"):
        batch_files = st.file_uploader(
            "Upload multiple testing instances",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="batch_uploader"
        )
        if batch_files and st.button("🚀 Execute Batch Run", key="batch_run"):
            results = []
            bar = st.progress(0)
            for i, f in enumerate(batch_files):
                f_buffer = f.getvalue()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_file:
                    t_file.write(f_buffer)
                    t_path = t_file.name
                
                try:
                    lbl, c, *_ = run_prediction_pipeline(t_path, model_name, scaler)
                    results.append({
                        "File Target": f.name,
                        "Inference Label": lbl,
                        "Confidence Index": f"{c*100:.1f}%"
                    })
                finally:
                    if os.path.exists(t_path):
                        os.remove(t_path)
                        
                bar.progress((i + 1) / len(batch_files))
            bar.empty()
            st.dataframe(results, use_container_width=True)

if __name__ == "__main__":
    show()