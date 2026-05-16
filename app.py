"""
VisionInspect AI — Main Application Entry Point
"""

import streamlit as st

def load_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 1. Page Configuration (Must be the very first Streamlit command)
st.set_page_config(
    page_title="VisionInspect AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Initialize Session States Safely
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "SVM"

# 3. Handle URL query parameters for navigation
query_params = st.query_params
if "page" in query_params:
    page = query_params["page"]
    if page.lower() == "about":
        st.session_state.current_page = "About"
    elif page.lower() == "analyse":
        st.session_state.current_page = "Analyse"
    elif page.lower() == "home":
        st.session_state.current_page = "Home"

load_css()

# 4. Navigation Callback to sync widget states flawlessly
def on_nav_change():
    st.session_state.current_page = st.session_state.nav_radio

# ============================================================================
# SIDEBAR NAVIGATION & CONTROLS
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <div style="
            font-family: 'Space Mono', monospace;
            font-size: 1rem;
            font-weight: 700;
            color: #E8EDF5;
            letter-spacing: -0.02em;
            line-height: 1;
        ">🔍 VisionInspect <span style="color:#FF6B6B;">AI</span></div>
        <div style="
            font-size: 0.7rem;
            color: #3D4A5C;
            margin-top: 0.35rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-family: 'Inter', sans-serif;
        ">Quality Inspection System</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<p class="vi-nav-label">Navigation</p>', unsafe_allow_html=True)

    PAGES = ["Home", "Analyse", "About"]

    # Safe index lookup for smooth rendering
    if st.session_state.current_page not in PAGES:
        st.session_state.current_page = "Home"
    current_index = PAGES.index(st.session_state.current_page)

    # Using an on_change callback prevents the widget sync-lag
    st.radio(
        label="nav",
        options=PAGES,
        index=current_index,
        label_visibility="collapsed",
        key="nav_radio",
        on_change=on_nav_change
    )

    st.divider()
    st.markdown('<p class="vi-nav-label">Active Model</p>', unsafe_allow_html=True)

    MODEL_OPTIONS = ["KNN", "SVM", "Random Forest"]
    st.session_state.selected_model = st.selectbox(
        label="model",
        options=MODEL_OPTIONS,
        index=MODEL_OPTIONS.index(st.session_state.selected_model),
        label_visibility="collapsed",
        key="model_select",
        help="This model is used for all predictions across the app.",
    )

    st.divider()
    st.markdown('<p class="vi-nav-label">Model Stats</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Accuracy", value="85.7%", delta="+2.4%")
    with col_b:
        st.metric(label="Precision", value="88.5%", delta="-1.2%")

    st.divider()
    st.markdown("""
    <div style="
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        color: #3D4A5C;
        line-height: 1.7;
    ">
        Ifra &nbsp;·&nbsp; Faiqa &nbsp;·&nbsp; Ayesha &nbsp;·&nbsp; Wajiha<br>
        Last updated: 2026-05-16
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# DYNAMIC VIEW LOADER ENGINE
# ============================================================================
def _load(name: str) -> None:
    try:
        if name == "Home":
            from views import home
            home.show()
        elif name == "Analyse":
            # Directing this safely to views/predict.py where your CV pipeline is fixed
            from views import predict
            predict.show()
        elif name == "About":
            from views import about
            about.show()
    except ModuleNotFoundError as exc:
        st.error(f"View not found — {exc}")
        st.caption("Make sure the file exists inside your `views/` folder.")
    except Exception as exc:
        st.error(f"Failed to load view — {exc}")
        raise

# Render active page view
_load(st.session_state.current_page)

st.divider()
st.markdown("""
<div style="
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #3D4A5C;
    padding-bottom: 0.5rem;
">
    © 2026 VisionInspect AI &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; OpenCV &nbsp;·&nbsp; Scikit-Learn
</div>
""", unsafe_allow_html=True)