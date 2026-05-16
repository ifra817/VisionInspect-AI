"""
🔍 Predict Page - VisionInspect AI
"""

import streamlit as st
import cv2
import numpy as np
import pickle
import os
from PIL import Image


# ============================================================================
# MODEL / PIPELINE LOADING
# ============================================================================

@st.cache_resource
def load_models():
    models = {}
    paths = {"KNN": "models/knn.pkl", "SVM": "models/svm.pkl", "Random Forest": "models/rf.pkl"}
    for name, path in paths.items():
        if os.path.exists(path):
            with open(path, "rb") as f:
                models[name] = pickle.load(f)
    return models


@st.cache_resource
def load_scaler():
    path = "models/scaler.pkl"
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None


# ============================================================================
# IMAGE HELPERS
# ============================================================================

def file_to_bgr(uploaded_file):
    """Convert a Streamlit UploadedFile to a BGR numpy array."""
    try:
        img = Image.open(uploaded_file).convert("RGB")
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        st.error(f"Could not load image: {e}")
        return None


def preprocess(image_bgr):
    """Return (gray, blurred, edges) all at 128×128."""
    resized  = cv2.resize(image_bgr, (128, 128))
    gray     = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred  = cv2.GaussianBlur(gray, (5, 5), 0)
    edges    = cv2.Canny(blurred, 50, 150)
    return resized, gray, blurred, edges


def extract_features(gray, edges):
    """
    Placeholder feature extractor.
    ⚠️  Replace with the real logic from src/feature_extraction.py once ready.
    Output shape must match what the trained models expect.
    """
    feats = [
        np.mean(gray), np.std(gray), float(np.min(gray)), float(np.max(gray)),
        np.mean(edges), float(np.sum(edges > 0)),
    ]
    hist = cv2.calcHist([gray], [0], None, [16], [0, 256]).flatten()[:8]
    feats.extend(hist.tolist())
    return np.array(feats).reshape(1, -1)


def run_prediction(image_bgr, model, scaler):
    """Full pipeline → (label_str, confidence_float, resized, gray, blurred, edges)."""
    resized, gray, blurred, edges = preprocess(image_bgr)
    features = extract_features(gray, edges)

    if scaler is not None:
        try:
            features = scaler.transform(features)
        except Exception:
            pass

    prediction = model.predict(features)[0]

    try:
        confidence = float(np.max(model.predict_proba(features)))
    except Exception:
        confidence = 0.85

    label = "DEFECTIVE" if prediction == 1 else "NORMAL"
    return label, confidence, resized, gray, blurred, edges


# ============================================================================
# PAGE
# ============================================================================

def show():

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="vi-page-title">🔍 Predict <span>Defects</span></div>
    <div class="vi-page-subtitle">
        Upload or capture a smartphone image — the pipeline handles the rest.
    </div>
    """, unsafe_allow_html=True)

    # ── Load assets ───────────────────────────────────────────────────────────
    models = load_models()
    scaler = load_scaler()

    if not models:
        st.warning("No trained models found in `models/`. Train the models first.")
        return

    # Active model comes from the global sidebar selector (app.py)
    model_name = st.session_state.get("selected_model", "SVM")
    if model_name not in models:
        st.error(f"Model '{model_name}' not loaded. Check `models/{model_name.lower().replace(' ', '_')}.pkl`.")
        return

    model = models[model_name]

    # ── Confidence threshold (page-local setting only) ────────────────────────
    with st.expander("⚙️ Prediction settings", expanded=False):
        conf_threshold = st.slider(
            "Confidence threshold",
            min_value=0.50, max_value=1.0, value=0.70, step=0.05,
            help="Warn when model confidence falls below this value.",
        )

    st.divider()

    # ── Two-column layout ─────────────────────────────────────────────────────
    col_input, col_result = st.columns(2, gap="large")

    # LEFT: image input
    with col_input:
        st.markdown('<div class="vi-section-label">Input Image</div>', unsafe_allow_html=True)

        method = st.radio(
            "input_method",
            ["📁 Upload File", "📷 Camera Snapshot"],
            horizontal=True,
            label_visibility="collapsed",
        )

        image_bgr = None

        if method == "📁 Upload File":
            uploaded = st.file_uploader(
                "Drop image here",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
            )
            if uploaded:
                image_bgr = file_to_bgr(uploaded)

        else:  # Camera
            snap = st.camera_input("Take a photo", label_visibility="collapsed")
            if snap:
                image_bgr = file_to_bgr(snap)

        if image_bgr is not None:
            st.markdown('<div class="vi-section-label" style="margin-top:1rem;">Original</div>',
                        unsafe_allow_html=True)
            st.image(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), use_column_width=True)

    # RIGHT: prediction result
    with col_result:
        st.markdown('<div class="vi-section-label">Result</div>', unsafe_allow_html=True)

        if image_bgr is None:
            st.markdown("""
            <div class="vi-card" style="text-align:center; padding:2.5rem 1rem; color:var(--text-muted);">
                Upload or capture an image to see the prediction here.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Analysing…"):
                label, conf, resized, gray, blurred, edges = run_prediction(image_bgr, model, scaler)

            badge_cls = "normal" if label == "NORMAL" else "defective"
            icon      = "🟢" if label == "NORMAL" else "🔴"

            st.markdown(f"""
            <div class="vi-card" style="padding: 1.5rem;">
                <div style="margin-bottom: 0.75rem;">
                    <span class="vi-badge {badge_cls}">{icon} {label}</span>
                </div>
                <div style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.4rem;">
                    Confidence &nbsp;
                    <span style="font-family:var(--font-display);
                                 color:var(--accent); font-weight:700;">
                        {conf*100:.1f}%
                    </span>
                    &nbsp;·&nbsp; Model: <strong>{model_name}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(float(conf))

            if conf < conf_threshold:
                st.warning(
                    f"Confidence ({conf*100:.1f}%) is below your threshold "
                    f"({conf_threshold*100:.0f}%). Consider re-capturing the image."
                )
            else:
                st.success("Confidence above threshold ✓")

    # ── Preprocessing visualisation (full width) ──────────────────────────────
    if image_bgr is not None:
        st.divider()
        st.markdown('<div class="vi-section-label">Preprocessing Pipeline</div>',
                    unsafe_allow_html=True)

        _, gray, blurred, edges = preprocess(image_bgr)
        resized_rgb = cv2.cvtColor(cv2.resize(image_bgr, (128, 128)), cv2.COLOR_BGR2RGB)

        p1, p2, p3, p4 = st.columns(4, gap="small")
        with p1:
            st.image(resized_rgb,          caption="① Original 128×128", use_column_width=True)
        with p2:
            st.image(Image.fromarray(gray),    caption="② Grayscale",       use_column_width=True)
        with p3:
            st.image(Image.fromarray(blurred), caption="③ Gaussian Blur",   use_column_width=True)
        with p4:
            st.image(Image.fromarray(edges),   caption="④ Canny Edges",     use_column_width=True)

    # ── Batch prediction ──────────────────────────────────────────────────────
    st.divider()
    st.markdown('<div class="vi-section-label">Batch Prediction</div>', unsafe_allow_html=True)

    with st.expander("Predict multiple images at once"):
        batch_files = st.file_uploader(
            "Upload images",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="batch_uploader",
        )

        if batch_files and st.button("🚀 Run Batch", key="batch_run"):
            results = []
            bar = st.progress(0)

            for i, f in enumerate(batch_files):
                img = file_to_bgr(f)
                if img is not None:
                    lbl, c, *_ = run_prediction(img, model, scaler)
                    results.append({
                        "File":       f.name,
                        "Prediction": lbl,
                        "Confidence": f"{c*100:.1f}%",
                    })
                bar.progress((i + 1) / len(batch_files))

            bar.empty()

            if results:
                st.success(f"Processed {len(results)} image(s).")
                st.dataframe(results, use_container_width=True)
            else:
                st.error("No successful predictions.")


if __name__ == "__main__":
    show()