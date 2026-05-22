import streamlit as st
import cv2
import numpy as np
import pandas as pd
import joblib
import os
import time
from datetime import datetime
from typing import Tuple, Optional

# Import your completed modules
from src.preprocessing import preprocess_image
from src.feature_extraction import extract_all_features

# ============================================================================
# CONFIGURATION
# ============================================================================

CLASS_NAMES = {0: "🟢 NORMAL", 1: "🔴 DEFECTIVE"}
COLORS = {0: (0, 255, 0), 1: (0, 0, 255)}  # BGR format


@st.cache_resource
def load_models():
    """Load and cache all trained models."""
    models = {}
    model_paths = {
        "KNN": "models/knn.pkl",
        "SVM": "models/svm.pkl",
        "Random Forest": "models/rf.pkl"
    }
    
    for model_name, path in model_paths.items():
        if os.path.exists(path):
            models[model_name] = joblib.load(path)
        else:
            st.error(f"❌ Model not found: {path}")
    
    return models


@st.cache_resource
def load_scaler():
    """Load and cache the feature scaler."""
    path = "models/scaler.pkl"
    if os.path.exists(path):
        return joblib.load(path)
    else:
        st.error(f"❌ Scaler not found: {path}")
        return None


def predict_frame(frame_bgr: np.ndarray, model: object, scaler: object) -> Tuple[Optional[int], Optional[float], Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Run inference pipeline on a single frame.
    """
    try:
        # Convert BGR to grayscale
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        
        # Normalize and resize
        gray = gray.astype(np.float32) / 255.0
        gray = cv2.resize(gray, (128, 128))
        
        # Edge detection
        gray_uint8 = (gray * 255).astype(np.uint8)
        edges = cv2.Canny(gray_uint8, 50, 150)
        edge_map = edges.astype(np.float32) / 255.0
        
        # Extract 42D features
        features = extract_all_features(gray, edge_map)
        features_2d = features.reshape(1, -1)
        features_scaled = scaler.transform(features_2d)
        
        # Predict
        prediction = int(model.predict(features_scaled)[0])
        
        # Get confidence
        confidence = 0.85  # Default fallback
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features_scaled)[0]
            confidence = float(np.max(probabilities))
        
        return prediction, confidence, gray, edge_map
    
    except Exception as e:
        st.error(f"Error in prediction: {e}")
        return None, None, None, None


# ============================================================================
# MAIN UI
# ============================================================================

def show():
    """Main Live Demo page."""
    
    # Title
    st.markdown("""
    <div class="vi-page-title">🎥 Live <span>Demo</span></div>
    <div class="vi-page-subtitle">
        Real-time webcam detection with feature visualization
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Persistent Session States for holding historical data between reruns
    if "predictions_history" not in st.session_state:
        st.session_state.predictions_history = []
    if "last_gray" not in st.session_state:
        st.session_state.last_gray = None
    if "last_edge_map" not in st.session_state:
        st.session_state.last_edge_map = None

    # Load resources
    models = load_models()
    scaler = load_scaler()
    
    if not models or scaler is None:
        st.error("❌ Cannot load models or scaler. Check `models/` directory.")
        return
    
    # ─────────────────────────────────────────────────────────────────────
    # LAYOUT: 2 COLUMNS (Defined first to avoid NameError)
    # ─────────────────────────────────────────────────────────────────────
    col_video, col_controls = st.columns([3, 1], gap="medium")
    
    # ─────────────────────────────────────────────────────────────────────
    # RIGHT: CONTROLS (Rendered first logically to capture user selection)
    # ─────────────────────────────────────────────────────────────────────
    with col_controls:
        st.markdown('<div class="vi-section-label">⚙️ Controls</div>', unsafe_allow_html=True)
        
        # Model Selection
        model_name = st.selectbox("Active Model", options=["SVM", "KNN", "Random Forest"], index=0)
        st.session_state.selected_model = model_name
        model = models[model_name]
        
        # Action Buttons
        start_button = st.button("▶️ START", key="live_start", use_container_width=True)
        stop_button = st.button("⏹️ STOP", key="live_stop", use_container_width=True)
        
        if start_button:
            st.session_state.live_demo_running = True
            st.rerun()
            
        if stop_button:
            st.session_state.live_demo_running = False
            st.rerun()
            
        st.divider()
        
        # Placeholders for live running data
        status_placeholder = st.empty()
        fps_placeholder = st.empty()
        frames_placeholder = st.empty()
        
        if st.session_state.get("live_demo_running", False):
            status_placeholder.info("🟢 RUNNING")
        else:
            status_placeholder.warning("⏹️ STOPPED")

    # ─────────────────────────────────────────────────────────────────────
    # LEFT: VIDEO FEED & RESULTS PLACEHOLDERS
    # ─────────────────────────────────────────────────────────────────────
    with col_video:
        st.markdown('<div class="vi-section-label">📹 Camera Feed</div>', unsafe_allow_html=True)
        video_placeholder = st.empty()
        
        # Metrics container underneath the video box
        metrics_container = st.container()

    # ─────────────────────────────────────────────────────────────────────
    # LIVE DETECTION LOOP
    # ─────────────────────────────────────────────────────────────────────
    if st.session_state.get("live_demo_running", False):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Cannot access webcam. Check permissions.")
            st.session_state.live_demo_running = False
            st.rerun()
        
        frame_count = 0
        start_time = time.time()
        
        # Main Thread Loop
        while st.session_state.live_demo_running:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to read from webcam")
                break
                
            frame_count += 1
            frame_display = cv2.resize(frame, (640, 480))
            
            # Inference Execution
            prediction, confidence, gray, edge_map = predict_frame(frame_display, model, scaler)
            
            if prediction is None:
                break
                
            # Update cache states for visuals below
            st.session_state.last_gray = gray
            st.session_state.last_edge_map = edge_map
            
            # Performance metrics
            elapsed = time.time() - start_time
            fps = frame_count / (elapsed + 1e-6)
            
            # History logs calculation
            new_log = {
                "Frame": frame_count,
                "Prediction": CLASS_NAMES[prediction],
                "Confidence": f"{confidence*100:.1f}%",
                "Timestamp": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.predictions_history.append(new_log)
            if len(st.session_state.predictions_history) > 15:
                st.session_state.predictions_history = st.session_state.predictions_history[-15:]
                
            # OpenCV Frame Annotations
            label = CLASS_NAMES[prediction]
            color = COLORS[prediction]
            
            frame_display = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
            cv2.rectangle(frame_display, (10, 10), (320, 100), (255, 255, 255), -1)
            cv2.rectangle(frame_display, (10, 10), (320, 100), (0, 0, 0), 2)
            cv2.putText(frame_display, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
            cv2.putText(frame_display, f"Conf: {confidence*100:.1f}%", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            
            # Stream UI updates on the fly
            video_placeholder.image(frame_display, use_container_width=True)
            
            with metrics_container:
                mc1, mc2, mc3 = st.columns(3)
                mc1.metric("Frames", frame_count)
                mc2.metric("FPS", f"{fps:.1f}")
                mc3.metric("Time Running", f"{elapsed:.1f}s")
                
            fps_placeholder.metric("FPS", f"{fps:.1f}")
            frames_placeholder.metric("Frames", frame_count)
            
        cap.release()
        st.session_state.live_demo_running = False
        st.rerun()

    # ─────────────────────────────────────────────────────────────────────
    # SECTION: PREDICTION HISTORY TABLE
    # ─────────────────────────────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="vi-section-label">📊 Prediction History</div>', unsafe_allow_html=True)
    
    if st.session_state.predictions_history:
        history_df = pd.DataFrame(st.session_state.predictions_history)
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("Run detection to see prediction history")
    
    # ─────────────────────────────────────────────────────────────────────
    # SECTION: FEATURE VISUALIZATION
    # ─────────────────────────────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="vi-section-label">🔍 Feature Visualization</div>', unsafe_allow_html=True)
    
    if st.session_state.last_gray is not None and st.session_state.last_edge_map is not None:
        feat_col1, feat_col2 = st.columns(2)
        
        with feat_col1:
            st.image(st.session_state.last_gray, caption="Grayscale (128×128)", use_container_width=True, clamp=True)
        
        with feat_col2:
            st.image(st.session_state.last_edge_map, caption="Edge Map (Canny)", use_container_width=True, clamp=True)
        
        # Extraction pipeline for stats mapping
        features = extract_all_features(st.session_state.last_gray, st.session_state.last_edge_map)
        lbp_features = features[:26]
        edge_density = features[26:]
        
        tab1, tab2 = st.tabs(["📈 LBP Features (26)", "📊 Edge Density (4×4)"])
        
        with tab1:
            lbp_df = pd.DataFrame({
                "LBP Bin": range(26),
                "Value": lbp_features
            })
            st.bar_chart(lbp_df.set_index("LBP Bin")["Value"])
        
        with tab2:
            edge_grid = edge_density.reshape(4, 4)
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 5))
            im = ax.imshow(edge_grid, cmap='hot', interpolation='nearest')
            ax.set_xlabel('Column')
            ax.set_ylabel('Row')
            ax.set_title('Edge Density Grid (4×4)')
            
            for i in range(4):
                for j in range(4):
                    ax.text(j, i, f'{edge_grid[i, j]:.2f}', ha="center", va="center", color="w", fontsize=10)
            
            plt.colorbar(im, ax=ax, label='Density')
            st.pyplot(fig)
    else:
        st.info("Run detection to see feature visualizations")
    
    # ─────────────────────────────────────────────────────────────────────
    # SECTION: INFORMATION EXPANDABLES
    # ─────────────────────────────────────────────────────────────────────
    st.divider()
    with st.expander("ℹ️ What is LBP (Local Binary Patterns)?"):
        st.markdown("""
        **Local Binary Patterns (LBP)** is a texture descriptor that captures local patterns in images.
        #### How it works:
        1. For each pixel, compare it with its 8 neighbors.
        2. Create a binary code based on intensity differences.
        3. Count occurrences of different patterns (26 bins for uniform LBP).
        """)
    
    with st.expander("ℹ️ What is Edge Density?"):
        st.markdown("""
        **Edge Density** quantifies how many edges appear in different regions of the image grid.
        #### How it works:
        1. Apply Canny edge detection.
        2. Divide the image into a 4×4 grid (16 sub-cells).
        3. Calculate the fraction of edge pixels per cell.
        """)


if __name__ == "__main__":
    show()