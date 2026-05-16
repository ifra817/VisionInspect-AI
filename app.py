"""
VisionInspect AI — Main Application Entry Point
"""

import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="VisionInspect AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL THEME
# Defined once here. views/ files are plain Python modules (not in pages/),
# so this CSS is always injected before any view renders.
# CSS custom properties (vars) work because every view runs inside this process.
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Tokens ──────────────────────────────────────────────────────────────── */
:root {
    /* Colours */
    --c-accent:          #FF6B6B;
    --c-accent-dim:      #E85555;
    --c-accent-glow:     rgba(255, 107, 107, 0.15);
    --c-success:         #00D4AA;
    --c-success-dim:     rgba(0, 212, 170, 0.12);
    --c-info:            #4A9EFF;
    --c-warning:         #FFD43B;

    /* Backgrounds */
    --c-bg:              #0A0E1A;
    --c-surface:         #111827;
    --c-elevated:        #1A2235;
    --c-hover:           #1F2A40;

    /* Borders */
    --c-border:          rgba(255, 255, 255, 0.06);
    --c-border-mid:      rgba(255, 255, 255, 0.12);
    --c-border-accent:   rgba(255, 107, 107, 0.35);

    /* Text */
    --c-text:            #E8EDF5;
    --c-text-dim:        #6B7A99;
    --c-text-muted:      #3D4A5C;

    /* Typography */
    --f-display:         'Space Mono', monospace;
    --f-body:            'Inter', sans-serif;

    /* Radii */
    --r-sm:              6px;
    --r-md:              10px;
    --r-lg:              16px;

    /* Shadows */
    --s-card:            0 4px 20px rgba(0, 0, 0, 0.4);
    --s-accent:          0 6px 28px rgba(255, 107, 107, 0.18);
}

/* ── Streamlit base reset ─────────────────────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"] {
    background-color: var(--c-bg) !important;
    font-family: var(--f-body) !important;
    color: var(--c-text) !important;
}

[data-testid="stMainBlockContainer"] {
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1100px !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--c-surface) !important;
    border-right: 1px solid var(--c-border-mid) !important;
}

[data-testid="stSidebar"] > div {
    padding: 1.5rem 1.25rem !important;
}

/* Radio items */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-family: var(--f-body) !important;
    font-size: 0.875rem !important;
    color: var(--c-text-dim) !important;
    padding: 0.3rem 0 !important;
    transition: color 0.15s;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    color: var(--c-text) !important;
}

/* Selectbox in sidebar */
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: var(--c-elevated) !important;
    border: 1px solid var(--c-border-mid) !important;
    border-radius: var(--r-sm) !important;
    color: var(--c-text) !important;
    font-size: 0.875rem !important;
}

/* Metric chips */
[data-testid="stMetric"] {
    background: var(--c-elevated) !important;
    border: 1px solid var(--c-border) !important;
    border-radius: var(--r-sm) !important;
    padding: 0.6rem 0.75rem !important;
}

[data-testid="stMetricLabel"] p {
    font-size: 0.72rem !important;
    color: var(--c-text-dim) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stMetricValue"] {
    color: var(--c-accent) !important;
    font-family: var(--f-display) !important;
    font-size: 1rem !important;
}

[data-testid="stMetricDelta"] {
    font-size: 0.72rem !important;
}

/* ── Buttons ──────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #FF6B6B 0%, #E85555 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--r-sm) !important;
    font-family: var(--f-body) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.01em !important;
    padding: 0.55rem 1.5rem !important;
    transition: opacity 0.18s, transform 0.15s, box-shadow 0.18s !important;
    box-shadow: var(--s-accent) !important;
}

.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(255, 107, 107, 0.28) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Dividers ─────────────────────────────────────────────────────────────── */
hr, [data-testid="stDivider"] {
    border-color: var(--c-border) !important;
    margin: 1.25rem 0 !important;
}

/* ── Alerts ───────────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    background: var(--c-elevated) !important;
    border-radius: var(--r-sm) !important;
    border-left-width: 3px !important;
    font-size: 0.875rem !important;
}

/* ── Progress bar ─────────────────────────────────────────────────────────── */
[data-testid="stProgressBar"] > div {
    background: rgba(255, 107, 107, 0.15) !important;
    border-radius: 99px !important;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #FF6B6B, #E85555) !important;
    border-radius: 99px !important;
}

/* ── File uploader ────────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--c-elevated) !important;
    border: 1.5px dashed var(--c-border-accent) !important;
    border-radius: var(--r-md) !important;
}

/* ── Code blocks ──────────────────────────────────────────────────────────── */
code, pre {
    font-family: var(--f-display) !important;
    font-size: 0.82em !important;
    background: var(--c-elevated) !important;
    border-radius: var(--r-sm) !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   SHARED COMPONENT CLASSES
   Used across all views — defined once here so views stay CSS-free.
   ══════════════════════════════════════════════════════════════════════════ */

/* Page header */
.vi-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    color: #E8EDF5;
    letter-spacing: -0.03em;
    line-height: 1.2;
    margin: 0 0 0.3rem 0;
}

.vi-title-accent { color: #FF6B6B; }

.vi-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.925rem;
    color: #6B7A99;
    margin: 0 0 2rem 0;
    font-weight: 400;
    line-height: 1.5;
}

/* Section eyebrow */
.vi-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #FF6B6B;
    margin: 0 0 0.6rem 0;
}

/* Cards */
.vi-card {
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin: 0.5rem 0;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.vi-card:hover {
    border-color: rgba(255, 107, 107, 0.3);
    box-shadow: 0 6px 28px rgba(255, 107, 107, 0.12);
}

.vi-card-raised {
    background: #1A2235;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 0.5rem 0;
}

/* Left-accent line card */
.vi-card-line {
    border-left: 2px solid #FF6B6B;
    border-radius: 0 10px 10px 0;
    background: #111827;
    border-top: 1px solid rgba(255,255,255,0.06);
    border-right: 1px solid rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 0.85rem 1.25rem;
    margin: 0.35rem 0;
}

/* Result badges */
.vi-badge {
    display: inline-block;
    padding: 0.4rem 1rem;
    border-radius: 99px;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}

.vi-badge-ok {
    background: rgba(0, 212, 170, 0.1);
    color: #00D4AA;
    border: 1px solid rgba(0, 212, 170, 0.28);
}

.vi-badge-bad {
    background: rgba(255, 107, 107, 0.1);
    color: #FF6B6B;
    border: 1px solid rgba(255, 107, 107, 0.3);
}

/* Stat tiles */
.vi-stat {
    background: #1A2235;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 1.1rem 1rem;
    text-align: center;
}

.vi-stat-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #FF6B6B;
    line-height: 1;
    margin-bottom: 0.35rem;
}

.vi-stat-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: #6B7A99;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}

/* Feature cards */
.vi-feat {
    background: #111827;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 1.4rem 1.25rem;
    text-align: center;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    height: 100%;
}

.vi-feat:hover {
    border-color: rgba(255, 107, 107, 0.3);
    box-shadow: 0 8px 30px rgba(255, 107, 107, 0.1);
    transform: translateY(-3px);
}

.vi-feat-icon  { font-size: 1.9rem; margin-bottom: 0.7rem; }

.vi-feat-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    font-weight: 700;
    color: #E8EDF5;
    margin-bottom: 0.4rem;
    letter-spacing: -0.01em;
}

.vi-feat-desc {
    font-size: 0.82rem;
    color: #6B7A99;
    line-height: 1.6;
}

/* Tech pills */
.vi-pill {
    display: inline-block;
    background: #1A2235;
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #6B7A99;
    padding: 0.28rem 0.8rem;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.18rem;
    font-family: 'Inter', sans-serif;
}

/* Sidebar section label */
.vi-nav-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3D4A5C;
    margin: 0 0 0.5rem 0;
    padding: 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "current_page"   not in st.session_state:
    st.session_state.current_page   = "Home"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "SVM"

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Wordmark
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

    # Navigation
    st.markdown('<p class="vi-nav-label">Navigation</p>', unsafe_allow_html=True)

    PAGES = ["Home", "Analyse", "Results", "About"]

    selected = st.radio(
        label="nav",
        options=PAGES,
        index=PAGES.index(st.session_state.current_page),
        label_visibility="collapsed",
        key="nav_radio",
    )
    st.session_state.current_page = selected

    st.divider()

    # Active model — single definition; pages read st.session_state.selected_model
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

    # Quick stats (placeholder until models are trained)
    st.markdown('<p class="vi-nav-label">Model Stats</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="Accuracy",  value="85.7%", delta="+2.4%")
    with col_b:
        st.metric(label="Precision", value="88.5%", delta="-1.2%")

    st.divider()

    # Build info
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


# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTER
# Views live in views/ (not pages/) so Streamlit does not auto-discover them.
# ══════════════════════════════════════════════════════════════════════════════
def _load(name: str) -> None:
    try:
        if name == "Home":
            from views import home;     home.show()
        elif name == "Analyse":
            from views import analyse;  analyse.show()
        elif name == "Results":
            from views import results;  results.show()
        elif name == "About":
            from views import about;    about.show()
    except ModuleNotFoundError as exc:
        st.error(f"View not found — {exc}")
        st.caption("Make sure the module exists inside the `views/` folder.")
    except Exception as exc:
        st.error(f"Failed to load view — {exc}")
        raise  # surfaces full traceback in terminal during development


_load(st.session_state.current_page)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
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