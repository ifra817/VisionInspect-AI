"""
ℹ️ About Page - VisionInspect AI
"""

import streamlit as st


def show():

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="vi-page-title">ℹ️ About <span>VisionInspect AI</span></div>
    <div class="vi-page-subtitle">
        Intelligent Visual Quality Inspection using Machine Learning and OpenCV
    </div>
    """, unsafe_allow_html=True)

    # ── Project overview ──────────────────────────────────────────────────────
    st.markdown('<div class="vi-section-label">Project Overview</div>', unsafe_allow_html=True)

    ov1, ov2 = st.columns(2, gap="large")

    with ov1:
        st.markdown("""
        <div class="vi-card">
            <div style="font-size:0.9rem; color:var(--text-secondary); line-height:1.8;">
                <strong style="color:var(--text-primary);">VisionInspect AI</strong> detects defects in
                smartphone components using classical ML and computer vision.<br><br>
                The pipeline combines OpenCV-based preprocessing (grayscale, blur, Canny edges)
                with LBP texture features fed into KNN, SVM, and Random Forest classifiers.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ov2:
        capabilities = [
            ("📤", "Image upload & instant analysis"),
            ("📹", "Live webcam defect detection"),
            ("🎨", "Defect region visualisation"),
            ("⚖️", "Side-by-side model comparison"),
            ("📊", "Accuracy / Precision / Recall metrics"),
            ("🔍", "Preprocessing pipeline viewer"),
        ]
        items = "".join(
            f'<div style="padding:0.35rem 0; font-size:0.88rem; color:var(--text-secondary);">'
            f'{icon}&nbsp; {text}</div>'
            for icon, text in capabilities
        )
        st.markdown(f'<div class="vi-card">{items}</div>', unsafe_allow_html=True)

    st.divider()

    # ── Architecture cards ────────────────────────────────────────────────────
    st.markdown('<div class="vi-section-label">Technical Architecture</div>', unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3, gap="medium")

    arch = [
        ("📊 Data Pipeline",
         ["Kaggle Smartphone Defects dataset",
          "80 / 20 train–test split",
          "Resize → Grayscale → Blur → Canny",
          "LBP + edge density features"]),
        ("🤖 ML Models",
         ["KNN — K-Nearest Neighbours",
          "SVM — Support Vector Machine",
          "Random Forest ensemble",
          "GridSearchCV hyperparameter tuning"]),
        ("🎨 Frontend",
         ["Streamlit multi-page app",
          "Custom CSS design system",
          "Plotly + Matplotlib charts",
          "OpenCV live webcam stream"]),
    ]

    for col, (title, points) in zip([a1, a2, a3], arch):
        items = "".join(
            f'<div style="padding:0.3rem 0; font-size:0.85rem; color:var(--text-secondary);">'
            f'· {p}</div>'
            for p in points
        )
        col.markdown(f"""
        <div class="vi-card" style="height:100%;">
            <div style="font-family:var(--font-display); font-size:0.85rem;
                        color:var(--accent); margin-bottom:0.75rem;">{title}</div>
            {items}
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Tech stack ────────────────────────────────────────────────────────────
    st.markdown('<div class="vi-section-label">Technology Stack</div>', unsafe_allow_html=True)

    t1, t2 = st.columns(2, gap="large")
    with t1:
        st.markdown("**Backend & ML**")
        for t in ["Python 3.10+", "OpenCV", "Scikit-Learn", "NumPy", "Pandas", "Jupyter"]:
            st.markdown(f'<span class="vi-tech-pill">{t}</span>', unsafe_allow_html=True)

    with t2:
        st.markdown("**Frontend & Visualisation**")
        for t in ["Streamlit", "Plotly", "Matplotlib", "Pillow", "Custom CSS", "GitHub"]:
            st.markdown(f'<span class="vi-tech-pill">{t}</span>', unsafe_allow_html=True)

    st.divider()

    # ── Team ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="vi-section-label">Team</div>', unsafe_allow_html=True)

    members = [
        ("🎨", "Ifra",   "Project Lead · Frontend",
         "Streamlit UI/UX, page layout, custom design system, project coordination."),
        ("🤖", "Ayesha", "ML Engineer",
         "Model training, GridSearchCV tuning, evaluation metrics, KNN/SVM/RF."),
        ("⚙️", "Faiqa",  "Backend · Integration",
         "Prediction pipeline, live detection, model ↔ Streamlit wiring."),
        ("📊", "Wajiha", "Data & Metrics",
         "EDA, preprocessing pipeline, evaluation notebook, metrics page."),
    ]

    m1, m2, m3, m4 = st.columns(4, gap="medium")

    for col, (emoji, name, role, desc) in zip([m1, m2, m3, m4], members):
        col.markdown(f"""
        <div class="vi-card" style="text-align:center; padding:1.5rem 1rem;">
            <div style="font-size:2.2rem; margin-bottom:0.5rem;">{emoji}</div>
            <div style="font-family:var(--font-display); font-size:0.95rem;
                        color:var(--accent); font-weight:700; margin-bottom:0.2rem;">{name}</div>
            <div style="font-size:0.78rem; color:var(--info);
                        margin-bottom:0.6rem; font-weight:600;">{role}</div>
            <div style="font-size:0.82rem; color:var(--text-secondary);
                        line-height:1.55;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Dataset ───────────────────────────────────────────────────────────────
    st.markdown('<div class="vi-section-label">Dataset</div>', unsafe_allow_html=True)

    d1, d2 = st.columns([3, 1], gap="large")

    dataset_rows = [
        ("Source",       "Kaggle — Smartphone Defect Detection Dataset"),
        ("Total images", "1 000+ smartphone component images"),
        ("Classes",      "Normal · Defective"),
        ("Resolution",   "128 × 128 pixels (normalised)"),
        ("Split",        "80% training — 20% testing"),
        ("Preprocessing","Grayscale → Normalisation → Canny edge detection"),
    ]

    with d1:
        for label, value in dataset_rows:
            st.markdown(f"""
            <div class="vi-card accent-left" style="padding: 0.75rem 1rem; margin: 0.4rem 0;">
                <span style="font-size:0.75rem; color:var(--accent);
                             text-transform:uppercase; letter-spacing:0.08em;
                             font-family:var(--font-display);">{label}</span><br>
                <span style="font-size:0.9rem; color:var(--text-secondary);">{value}</span>
            </div>
            """, unsafe_allow_html=True)

    with d2:
        for num, lbl in [("1 000+", "Images"), ("128×128", "Resolution"), ("80:20", "Train : Test")]:
            st.markdown(f"""
            <div class="vi-stat" style="margin-bottom:0.75rem;">
                <div class="vi-stat-number" style="font-size:1.4rem;">{num}</div>
                <div class="vi-stat-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── Project timeline ──────────────────────────────────────────────────────
    st.markdown('<div class="vi-section-label">Project Timeline</div>', unsafe_allow_html=True)

    phases = [
        ("Phase 1", "Setup & Planning",          "Repo, folder structure, team roles, tech stack."),
        ("Phase 2", "Data Preparation",          "Dataset download, train/test split, preprocessing pipeline."),
        ("Phase 3", "Model Training",            "KNN, SVM, RF training + GridSearchCV."),
        ("Phase 4", "Frontend Development",      "Streamlit pages, custom CSS, responsive layout."),
        ("Phase 5", "Integration & Testing",     "Model loading, prediction pipeline, live detection."),
        ("Phase 6", "Refinement & Deployment",   "Optimisation, bug fixes, documentation."),
    ]

    for phase, title, desc in phases:
        st.markdown(f"""
        <div class="vi-card accent-left" style="margin: 0.5rem 0;">
            <div style="display:flex; gap:1rem; align-items:baseline;">
                <span style="font-family:var(--font-display); font-size:0.72rem;
                             color:var(--accent); white-space:nowrap;">{phase}</span>
                <span style="font-weight:600; color:var(--text-primary);
                             font-size:0.9rem;">{title}</span>
            </div>
            <div style="font-size:0.85rem; color:var(--text-secondary);
                        margin-top:0.25rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Model performance placeholder ─────────────────────────────────────────
    st.markdown('<div class="vi-section-label">Model Performance</div>', unsafe_allow_html=True)
    st.info(
        "Training not yet complete. Once `results/eval_results.pkl` is available, "
        "this section will show Accuracy, Precision, Recall, F1-Score, ROC-AUC, "
        "and Confusion Matrix comparisons for all three models."
    )

    st.divider()

    # ── Repository ────────────────────────────────────────────────────────────
    st.markdown('<div class="vi-section-label">Repository</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="vi-card accent-left">
        <div style="font-size:0.88rem; color:var(--text-secondary); line-height:1.9;">
            <strong style="color:var(--text-primary);">GitHub:</strong>
            <a href="https://github.com/ifra817/VisionInspect-AI" target="_blank"
               style="color:var(--accent); text-decoration:none;">
               ifra817/VisionInspect-AI
            </a><br>
            <strong style="color:var(--text-primary);">Branch:</strong> main<br>
            <strong style="color:var(--text-primary);">Status:</strong>
            <span style="color:var(--success);">● Active Development</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()