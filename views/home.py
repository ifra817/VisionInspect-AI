"""
Home — VisionInspect AI
"""

import streamlit as st


def show():

    st.markdown("""
    <style>
        [data-testid="stMainBlockContainer"] {
            padding-top: 0 !important;
        }

        /* Animated scan line across hero */
        @keyframes scanline {
            0%   { top: 0%; opacity: 0; }
            10%  { opacity: 1; }
            90%  { opacity: 1; }
            100% { top: 100%; opacity: 0; }
        }

        /* Subtle grid background */
        .vi-hero-bg {
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(255,107,107,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,107,107,0.03) 1px, transparent 1px);
            background-size: 48px 48px;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes pulse-glow {
            0%, 100% { opacity: 0.5; transform: scale(1);   }
            50%       { opacity: 0.8; transform: scale(1.05); }
        }

        .vi-glow-orb {
            position: fixed;
            width: 600px;
            height: 600px;
            border-radius: 50%;
            background: radial-gradient(circle,
                rgba(255,107,107,0.07) 0%,
                transparent 65%
            );
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 0;
            animation: pulse-glow 4s ease-in-out infinite;
        }

        /* Nav cards */
        .vi-nav-card {
            background: rgba(26, 34, 53, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            padding: 1.4rem 1rem;
            text-align: center;
            cursor: pointer;
            transition: border-color 0.25s, box-shadow 0.25s, transform 0.2s;
            backdrop-filter: blur(8px);
        }

        .vi-nav-card:hover {
            border-color: rgba(255, 107, 107, 0.5);
            box-shadow: 0 0 24px rgba(255, 107, 107, 0.12);
            transform: translateY(-3px);
        }

        .vi-nav-card-icon {
            font-size: 1.6rem;
            margin-bottom: 0.5rem;
        }

        .vi-nav-card-title {
            font-family: 'Space Mono', monospace;
            font-size: 0.8rem;
            font-weight: 700;
            color: #E8EDF5;
            margin-bottom: 0.3rem;
            letter-spacing: -0.01em;
        }

        .vi-nav-card-desc {
            font-family: 'Inter', sans-serif;
            font-size: 0.75rem;
            color: #6B7A99;
            line-height: 1.5;
        }

        /* Stat row */
        .vi-stat-inline {
            text-align: center;
            padding: 0.5rem;
        }

        .vi-stat-inline-num {
            font-family: 'Space Mono', monospace;
            font-size: 1.4rem;
            font-weight: 700;
            color: #FF6B6B;
            line-height: 1;
        }

        .vi-stat-inline-lbl {
            font-family: 'Inter', sans-serif;
            font-size: 0.7rem;
            color: #3D4A5C;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.25rem;
        }

        /* Tag pills in description */
        .vi-tag {
            display: inline-block;
            background: rgba(255, 107, 107, 0.08);
            border: 1px solid rgba(255, 107, 107, 0.2);
            color: #FF6B6B;
            padding: 0.15rem 0.6rem;
            border-radius: 99px;
            font-size: 0.72rem;
            font-family: 'Space Mono', monospace;
            margin: 0.15rem;
        }

        /* Divider line with glow */
        .vi-line {
            height: 1px;
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(255,107,107,0.3) 30%,
                rgba(255,107,107,0.3) 70%,
                transparent 100%
            );
            margin: 0.5rem auto;
            max-width: 600px;
        }
    </style>

    <div class="vi-hero-bg"></div>
    <div class="vi-glow-orb"></div>
    """, unsafe_allow_html=True)

    # ── Top spacer ────────────────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── Eyebrow ───────────────────────────────────────────────────────────────
    st.markdown("""
    <p style="
        text-align: center;
        font-family: 'Space Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #FF6B6B;
        margin: 0 0 1.1rem 0;
        opacity: 0.8;
    ">Visual Quality Inspection System</p>
    """, unsafe_allow_html=True)

    # ── Title ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <h1 style="
        text-align: center;
        font-family: 'Space Mono', monospace;
        font-size: clamp(2.6rem, 5vw, 4rem);
        font-weight: 700;
        color: #E8EDF5;
        letter-spacing: -0.04em;
        line-height: 1.08;
        margin: 0 0 1.25rem 0;
    ">VisionInspect<span style="color:#FF6B6B;"> AI</span></h1>
    """, unsafe_allow_html=True)

    # ── Divider glow ──────────────────────────────────────────────────────────
    st.markdown('<div class="vi-line"></div>', unsafe_allow_html=True)

    # ── Description ───────────────────────────────────────────────────────────
    st.markdown("""
    <p style="
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.975rem;
        color: #6B7A99;
        max-width: 480px;
        margin: 1.1rem auto 0.75rem;
        line-height: 1.8;
    ">
        An intelligent defect detection system built for smartphone
        component quality control. Upload an image or stream live from
        your camera — the ML pipeline classifies it in real time.
    </p>
    """, unsafe_allow_html=True)

    # ── Tags ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; margin: 0.75rem 0 1.75rem;">
        <span class="vi-tag">KNN</span>
        <span class="vi-tag">SVM</span>
        <span class="vi-tag">Random Forest</span>
        <span class="vi-tag">OpenCV</span>
        <span class="vi-tag">scikit-learn</span>
    </div>
    """, unsafe_allow_html=True)

    # ── CTA button ────────────────────────────────────────────────────────────
    _, btn, _ = st.columns([2.6, 1, 2.6])
    with btn:
        if st.button("Check it out →", key="home_cta", use_container_width=True):
            st.session_state.current_page = "Analyse"
            st.rerun()

    # ── Stats strip ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="vi-line"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    for col, num, lbl in zip(
        [s1, s2, s3, s4],
        ["~90%",   "3",       "<100ms",  "1000+"],
        ["Accuracy", "Models", "Pred. Time", "Train Images"],
    ):
        with col:
            st.markdown(f"""
            <div class="vi-stat-inline">
                <div class="vi-stat-inline-num">{num}</div>
                <div class="vi-stat-inline-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Navigation cards ──────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <p style="
        text-align: center;
        font-family: 'Space Mono', monospace;
        font-size: 0.62rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #3D4A5C;
        margin-bottom: 1rem;
    ">Where do you want to go?</p>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    nav_items = [
        ("c1", "🔬", "Analyse",  "Analyse",  "Upload an image or use live camera to detect defects."),
        ("c2", "📊", "Results",  "Results",  "View model metrics, comparisons and evaluation stats."),
        ("c3", "ℹ️", "About",    "About",    "Meet the team, explore the dataset and architecture."),
        ("c4", "📖", "Docs",     None,       "How the preprocessing and feature pipeline works."),
    ]

    for col, (_, icon, label, page, desc) in zip([c1, c2, c3, c4], nav_items):
        with col:
            st.markdown(f"""
            <div class="vi-nav-card">
                <div class="vi-nav-card-icon">{icon}</div>
                <div class="vi-nav-card-title">{label}</div>
                <div class="vi-nav-card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            # Real button underneath (invisible label, just for routing)
            if page and st.button(f"Go to {label}", key=f"nav_{label}",
                                  use_container_width=True):
                st.session_state.current_page = page
                st.rerun()


if __name__ == "__main__":
    show()