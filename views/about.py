"""
ℹ️ About Page - VisionInspect AI
"""

import streamlit as st

def show():
    # ── Page Header ──────────────────────────────────────────────────────────
    st.title("ℹ️ About VisionInspect AI")
    st.markdown("##### Intelligent Visual Quality Inspection using Machine Learning and OpenCV")
    st.divider()

    # ── Project Overview ─────────────────────────────────────────────────────
    st.header("What is VisionInspect AI?")
    st.info(
        "**VisionInspect AI** is an intelligent defect detection system built for smartphone "
        "component quality control using machine learning and computer vision.\n\n"
        "The system combines OpenCV-based preprocessing techniques with handcrafted LBP "
        "texture features and multiple machine learning classifiers including KNN, SVM, and Random Forest."
    )
    
    st.write("") # Spacer

    # ── Key Capabilities ─────────────────────────────────────────────────────
    st.header("Key Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.subheader("📤 Image Analysis")
            st.write("Upload single or batch images for instant defect detection.")
        with st.container(border=True):
            st.subheader("⚖️ Model Comparison")
            st.write("Compare KNN, SVM, and Random Forest predictions side-by-side.")

    with col2:
        with st.container(border=True):
            st.subheader("📹 Live Detection")
            st.write("Perform real-time defect detection using webcam streaming.")
        with st.container(border=True):
            st.subheader("📊 Detailed Metrics")
            st.write("Explore accuracy, precision, recall, and confusion matrices.")

    with col3:
        with st.container(border=True):
            st.subheader("🔍 Visualization")
            st.write("Visualize preprocessing steps and extracted image features.")
        with st.container(border=True):
            st.subheader("⚡ Fast Processing")
            st.write("Optimized inference pipeline for quick predictions.")

    st.divider()

    # ── How It Works ─────────────────────────────────────────────────────────
    st.header("How It Works")
    
    st.markdown("""
    **1️⃣ Image Acquisition**  
    Users upload smartphone component images or capture them directly through a webcam. Images are resized for consistent processing.
    
    **2️⃣ Preprocessing Pipeline**  
    Images are converted to grayscale, denoised using Gaussian blur, and processed with edge detection for structural analysis.
    
    **3️⃣ Feature Extraction**  
    The system extracts handcrafted texture and edge-based features including Local Binary Patterns and edge density maps.
    
    **4️⃣ Classification & Results**  
    Extracted features are passed into the selected machine learning classifier to predict whether the component is normal or defective.
    """)

    st.divider()

    # ── Team Section ─────────────────────────────────────────────────────────
    st.header("Meet the Team")
    
    team_col1, team_col2 = st.columns(2)
    
    with team_col1:
        with st.container(border=True):
            st.markdown("### 🎨 Ifra")
            st.markdown("**Repo Owner & Project Lead**")
            st.caption("DATA PIPELINE · FRONTEND")
            st.write("Manages project structure, frontend integration, and prediction workflow implementation.")
            
        with st.container(border=True):
            st.markdown("### ⚡ Ayesha")
            st.markdown("**ML Engineer**")
            st.caption("MODEL TRAINING · OPTIMIZATION")
            st.write("Handles model training, hyperparameter tuning, and performance optimization.")

    with team_col2:
        with st.container(border=True):
            st.markdown("### 🤖 Faiqa")
            st.markdown("**Feature Engineering Lead**")
            st.caption("FEATURE EXTRACTION · EDA")
            st.write("Designs handcrafted image features and contributes to real-time defect detection.")
            
        with st.container(border=True):
            st.markdown("### 📊 Wajiha")
            st.markdown("**Evaluation & Analytics**")
            st.caption("METRICS · ERROR ANALYSIS")
            st.write("Builds evaluation pipelines, analytics dashboards, and performance visualizations.")

    st.divider()

    # ── Technical Architecture ───────────────────────────────────────────────
    st.header("Technical Architecture")
    
    arch1, arch2, arch3 = st.columns(3)
    
    with arch1:
        with st.container(border=True):
            st.markdown("#### 📊 Data Pipeline")
            st.markdown("- Kaggle smartphone defects dataset\n- Image preprocessing using OpenCV\n- LBP and edge-density feature extraction\n- Train-test data splitting")
            
    with arch2:
        with st.container(border=True):
            st.markdown("#### 🤖 ML Models")
            st.markdown("- KNN classifier\n- SVM with RBF kernel\n- Random Forest ensemble\n- GridSearchCV optimization")
            
    with arch3:
        with st.container(border=True):
            st.markdown("#### 🎨 Frontend & Deploy")
            st.markdown("- Streamlit multi-page app\n- Custom CSS design system\n- Matplotlib & Plotly charts\n- Real-time prediction pipeline")

    st.divider()

    # ── Tech Stack ───────────────────────────────────────────────────────────
    st.header("Technology Stack")
    
    tech_left, tech_right = st.columns(2)
    
    with tech_left:
        st.markdown("##### 🔧 Backend & ML")
        # Using inline code ticks to create a "pill" look natively in Streamlit
        st.markdown("`Python` &nbsp; `OpenCV` &nbsp; `Scikit-Learn` &nbsp; `NumPy` &nbsp; `Pandas`", unsafe_allow_html=True)
        
    with tech_right:
        st.markdown("##### 🎨 Frontend & Visualisation")
        st.markdown("`Streamlit` &nbsp; `Plotly` &nbsp; `Matplotlib` &nbsp; `Pillow` &nbsp; `GitHub`", unsafe_allow_html=True)

    st.divider()

    # ── Dataset Overview ─────────────────────────────────────────────────────
    st.header("Dataset Overview")
    
    data_text, data_stats = st.columns([2, 1.2])
    
    with data_text:
        st.write("The dataset contains smartphone component images labelled as **NORMAL** or **DEFECTIVE** for supervised defect detection training.")
        st.write("Images are preprocessed and split into training and testing sets to ensure reliable evaluation and generalization.")
        
    with data_stats:
        m1, m2, m3 = st.columns(3)
        m1.metric(label="Images", value="1000+")
        m2.metric(label="Resolution", value="128²")
        m3.metric(label="Split", value="80:20")

    st.divider()

    # ── Repository ───────────────────────────────────────────────────────────
    st.header("Repository & Status")
    
    repo1, repo2 = st.columns(2)
    
    with repo1:
        st.markdown("**GitHub Repository**")
        st.markdown("[ifra817/VisionInspect-AI ↗](https://github.com/ifra817/VisionInspect-AI)")
        
    with repo2:
        st.markdown("**Development Status**")
        st.success("● Active Development")