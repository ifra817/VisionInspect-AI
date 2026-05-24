"""
Home — VisionInspect AI Landing Page
"""

import streamlit as st


def show():

    st.markdown("""
    <style>
        [data-testid="stMainBlockContainer"] {
            padding-top: 4rem !important;
        }

        .vi-hero-bg {
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(255,107,107,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,107,107,0.02) 1px, transparent 1px);
            background-size: 64px 64px;
            pointer-events: none;
            z-index: -1; /* Changed from 0 to -1 */
        }

        @keyframes pulse-glow {
            0%, 100% { opacity: 0.4; transform: scale(1);   }
            50%       { opacity: 0.7; transform: scale(1.08); }
        }

        .vi-glow-orb {
            position: fixed;
            width: 700px;
            height: 700px;
            border-radius: 50%;
            background: radial-gradient(circle,
                rgba(255,107,107,0.08) 0%,
                transparent 70%
            );
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: -2; /* Changed from 0 to -2 so it sits below hero-bg */
            animation: pulse-glow 5s ease-in-out infinite;
        }


        .vi-line {
            height: 1px;
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(255,107,107,0.4) 20%,
                rgba(255,107,107,0.4) 80%,
                transparent 100%
            );
            margin: 2rem auto;
            max-width: 600px;
        }

        .vi-feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-top: 3rem;
        }

        @media (max-width: 900px) {
            .vi-feature-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 600px) {
            .vi-feature-grid {
                grid-template-columns: 1fr;
            }
        }

        .vi-feature-item {
            background: rgba(26, 34, 53, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 1.75rem 1.5rem;
            text-align: center;
            transition: all 0.25s ease;
            backdrop-filter: blur(10px);
        }

        .vi-feature-item:hover {
            border-color: rgba(255, 107, 107, 0.3);
            background: rgba(26, 34, 53, 0.8);
            transform: translateY(-2px);
        }

        .vi-feature-icon {
            font-size: 2rem;
            margin-bottom: 0.75rem;
        }

        .vi-feature-title {
            font-family: 'Space Mono', monospace;
            font-size: 0.9rem;
            font-weight: 700;
            color: #E8EDF5;
            margin-bottom: 0.4rem;
            letter-spacing: -0.01em;
        }

        .vi-feature-desc {
            font-size: 0.82rem;
            color: #6B7A99;
            line-height: 1.6;
        }

        .vi-stat-item {
            text-align: center;
        }

        .vi-stat-number {
            font-family: 'Space Mono', monospace;
            font-size: 1.6rem;
            font-weight: 700;
            color: #FF6B6B;
            line-height: 1;
            margin-bottom: 0.35rem;
        }

        .vi-stat-label {
            font-size: 0.75rem;
            color: #6B7A99;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 500;
        }

        .vi-footer-section {
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: 2rem;
        }

        .vi-footer-text {
            font-size: 0.85rem;
            color: #6B7A99;
            margin-bottom: 1.5rem;
        }
    </style>

    <div class="vi-hero-bg"></div>
    <div class="vi-glow-orb"></div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.markdown("""
    <p style="
        text-align: center;
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #FF6B6B;
        margin: 0 0 1.5rem 0;
        opacity: 0.85;
    ">Intelligent Visual Inspection System</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="
        text-align: center;
        font-family: 'Space Mono', monospace;
        font-size: clamp(2.8rem, 6vw, 4.2rem);
        font-weight: 700;
        color: #E8EDF5;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin: 0 0 1rem 0;
    ">VisionInspect<span style="color:#FF6B6B;"> AI</span></h1>
    """, unsafe_allow_html=True)

    st.markdown('<div class="vi-line"></div>', unsafe_allow_html=True)

    st.markdown("""
    <p style="
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #6B7A99;
        max-width: 550px;
        margin: 0 auto 2rem;
        line-height: 1.8;
        font-weight: 400;
    ">
        Detect smartphone component defects in real-time using advanced
        machine learning and computer vision. Upload an image or use your camera.
    </p>
    """, unsafe_allow_html=True)

    col_left, col_cta, col_right = st.columns([1, 1.2, 1])
    with col_cta:
        if st.button("Start Analysis →", key="cta_start", use_container_width=True):
            st.session_state.current_page = "Analyse"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="vi-line"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    stats = [
        ("~90%", "Accuracy"),
        ("3", "ML Models"),
        ("<100ms", "Pred. Time"),
        ("1000+", "Training Data"),
    ]
    for col, (num, lbl) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(f"""
            <div class="vi-stat-item">
                <div class="vi-stat-number">{num}</div>
                <div class="vi-stat-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <p style="
        text-align: center;
        font-family: 'Space Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #3D4A5C;
        margin-bottom: 2rem;
    ">What You Can Do</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="vi-feature-grid">
        <div class="vi-feature-item">
            <div class="vi-feature-icon">📤</div>
            <div class="vi-feature-title">Upload Images</div>
            <div class="vi-feature-desc">Batch process or analyze single images with instant predictions.</div>
        </div>
        <div class="vi-feature-item">
            <div class="vi-feature-icon">📷</div>
            <div class="vi-feature-title">Live Camera</div>
            <div class="vi-feature-desc">Real-time defect detection directly from your webcam.</div>
        </div>
        <div class="vi-feature-item">
            <div class="vi-feature-icon">🤖</div>
            <div class="vi-feature-title">3 ML Models</div>
            <div class="vi-feature-desc">Choose between KNN, SVM, or Random Forest classifiers.</div>
        </div>
        <div class="vi-feature-item">
            <div class="vi-feature-icon">🔍</div>
            <div class="vi-feature-title">Detailed Analysis</div>
            <div class="vi-feature-desc">See confidence scores and preprocessing pipeline visualizations.</div>
        </div>
        <div class="vi-feature-item">
            <div class="vi-feature-icon">📊</div>
            <div class="vi-feature-title">Model Metrics</div>
            <div class="vi-feature-desc">Explore accuracy, precision, recall, and ROC-AUC comparisons.</div>
        </div>
        <div class="vi-feature-item">
            <div class="vi-feature-icon">⚡</div>
            <div class="vi-feature-title">Fast Processing</div>
            <div class="vi-feature-desc">Sub-100ms inference time for real-world quality control.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="vi-footer-section">
        <div class="vi-footer-text">
            Want to learn more? Explore the team and project architecture.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    footer_col1, footer_col2 = st.columns(2, gap="small")
    
    with footer_col1:
        st.link_button("👥 Meet the Team", url="?page=about", use_container_width=True)
    
    with footer_col2:
        st.link_button("🔍 Start Analysing", url="?page=analyse", use_container_width=True)


    st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    show()