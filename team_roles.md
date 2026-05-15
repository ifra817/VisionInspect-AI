# 👥 VisionInspect AI — Team Roles & Responsibilities

A comprehensive guide for the 4-member team breakdown. This document details each person's tasks, deliverables, effort balance, and learning outcomes for the **VisionInspect-AI** Streamlit project.

---

## 📋 Team Overview

| Member | Role | Focus Area | Streamlit Page | ML % | UI % | Docs % |
|--------|------|-----------|-----------------|------|------|--------|
| **Ifra** | Lead & Data Pipeline | Repo, Data, Preprocessing | Predict | 55% | 35% | 10% |
| **Faiqa** | Feature Engineering | Feature Extraction, EDA | Live Demo | 55% | 35% | 10% |
| **Ayesha** | Model Training | ML Models, Hyperparameter Tuning | Model Compare | 55% | 35% | 10% |
| **Wajiha** | Evaluation & Metrics | Evaluation, Error Analysis | Metrics | 55% | 35% | 10% |

---

## 🎯 Role Breakdown

---

## 1️⃣ IFRA — Data Pipeline + Predict Page

**Title:** Repo Owner & Project Coordinator  
**Primary Responsibility:** Set up infrastructure, manage data, build Predict page  
**Streamlit Page:** 📄 **Predict** (+ App Shell)

### Build — ML Side (55%)

#### GitHub Repository Setup
- [ ] Initialize repository structure (done ✓ but verify .gitignore, branches)
- [ ] Create branch naming convention:
  - `main` — production-ready code
  - `develop` — integration branch
  - `feature/ifra-preprocessing`, `feature/faiqa-features`, etc. — personal feature branches
- [ ] Set up `.gitignore`:
  ```
  venv/
  __pycache__/
  *.pyc
  .DS_Store
  data/train/
  data/val/
  data/test/
  models/*.pkl
  results/*.png
  .streamlit/secrets.toml
  ```
- [ ] Create `requirements.txt` with all dependencies (OpenCV, scikit-learn, Streamlit, etc.)

#### Dataset Management
- [ ] **Download dataset** from Kaggle: "Cracked and Intact Smartphone Images Dataset"
  - Target: 300–500 images per class minimum
  - If smaller, plan augmentation for Day 1
- [ ] **Write `data_split.py`**
  ```python
  # Organize raw dataset into:
  # data/train/{normal, defective} — 70%
  # data/val/{normal, defective} — 15%
  # data/test/{normal, defective} — 15%
  ```
- [ ] Validate folder structure and image counts per class
- [ ] Create dataset summary doc (image counts, class balance, size)

#### OpenCV Preprocessing Pipeline
- [ ] **Write `src/preprocessing.py`**
  - `resize(img, (128, 128))` — standardize input
  - `cvtColor(img, COLOR_BGR2GRAY)` — convert to grayscale
  - `GaussianBlur(gray, (5,5), 0)` — noise reduction
  - `Canny(blurred, 50, 150)` — edge detection
  - `normalize(...)` — scale to [0, 1]
  - Return: preprocessed grayscale image + edge map

**Code structure:**
```python
def preprocess_image(img_path):
    """Load and preprocess single image"""
    
def preprocess_batch(image_dir):
    """Preprocess all images in a directory"""
```

#### Image Augmentation (Fallback)
- [ ] **Write `src/augmentation.py`** (use only if dataset < 300/class)
  - Horizontal/vertical flips
  - Brightness jitter (±20%)
  - Slight rotation (±15°)
  - Use OpenCV or `albumentations`

#### Prediction Pipeline
- [ ] **Write `src/predict.py`**
  - Load image → preprocess → extract features (Faiqa's function) → load model → predict
  - Return: label (NORMAL/DEFECTIVE), confidence score
  - Handle edge cases (corrupted images, invalid input)

### Build — UI Side (35%)

#### Streamlit App Shell
- [ ] **Build `app.py` — main entry point**
  ```python
  import streamlit as st
  from pages import predict, live_demo, model_compare, metrics
  
  st.set_page_config(page_title="VisionInspect AI", layout="wide")
  
  # Sidebar navigation
  page = st.sidebar.radio("Navigate", ["Predict", "Live Demo", "Model Compare", "Metrics"])
  
  if page == "Predict":
      predict.show()
  elif page == "Live Demo":
      live_demo.show()
  # ... etc
  ```
- [ ] Set up consistent theme (colors, fonts, CSS if needed)
- [ ] Sidebar with:
  - Project title + logo (optional)
  - Navigation buttons
  - Model selector (dropdown: KNN / SVM / RF)
  - Quick stats (accuracy of selected model)

#### Predict Page (`pages/predict.py`)
- [ ] **Page layout:**
  - Header: "🔍 Predict Defects"
  - Two-column layout:
    - **Left column:** Image upload + results
    - **Right column:** Preprocessing steps visualization
  
- [ ] **Image Input Methods:**
  - File uploader: `st.file_uploader("Upload smartphone image", type=['jpg', 'png'])`
  - Camera snapshot: `st.camera_input("Take a photo")`
  - Sample image selector (for demo purposes)

- [ ] **Prediction Display:**
  - Preprocessed image steps (original → grayscale → edges) side-by-side
  - Large result badge: 🟢 **NORMAL** or 🔴 **DEFECTIVE**
  - Confidence score: "Confidence: 92.5%"
  - Selected model name: "Model: SVM (RBF Kernel)"

- [ ] **Interactive Features:**
  - Model selector dropdown — dynamically loads correct `.pkl` model
  - Show preprocessing parameters (blur kernel, Canny thresholds)
  - Batch predict button (upload multiple images, show results table)

**Code structure:**
```python
def show():
    st.title("🔍 Predict Defects")
    uploaded_file = st.file_uploader("Upload image")
    if uploaded_file:
        img = cv2.imread(uploaded_file)
        pred, conf = predict_image(img)
        st.write(f"Result: {pred}, Confidence: {conf:.2%}")
```

#### App Configuration
- [ ] `.streamlit/config.toml` for consistent styling:
  ```toml
  [theme]
  primaryColor = "#FF6B6B"
  backgroundColor = "#FFFFFF"
  secondaryBackgroundColor = "#F0F2F6"
  textColor = "#31333F"
  font = "sans serif"
  ```

### Documentation (10%)

#### README.md
- [ ] Write **Getting Started** section (already drafted, refine)
- [ ] Add **Installation & Setup** subsection with step-by-step commands
- [ ] Include dataset download instructions

#### team_roles.md (this file)
- [ ] Own the document, ensure all team members update it with progress

#### GitHub Cleanup (Final)
- [ ] Merge all branches into `develop` → `main`
- [ ] Tag release: `v1.0.0`
- [ ] Verify all `.pkl` models are in `models/`
- [ ] Verify all `.png` results are in `results/`
- [ ] Final README pass — ensure all links work

### Daily Deliverables

**Day 1 (Foundation):**
- ✅ Repo initialized, .gitignore, requirements.txt
- ✅ Dataset downloaded and split (train/val/test)
- ✅ `preprocessing.py` complete and tested on 5 sample images
- ✅ App shell structure (app.py + pages/ folder) with routing working
- ✅ Predict page skeleton (uploader + dummy output)

**Day 2 (Integration):**
- ✅ Preprocessing pipeline tested on full dataset
- ✅ Augmentation.py written (if needed)
- ✅ `predict.py` fully functional (loads model, returns prediction + confidence)
- ✅ Predict page complete: uploader, preprocessed images display, result badge
- ✅ Model selector dropdown integrated (loads different .pkl files)

**Day 3 (Polish):**
- ✅ Webcam snapshot feature in Predict page working
- ✅ Batch predict feature (optional, nice-to-have)
- ✅ README finalized
- ✅ All .gitignore rules verified (no large files in repo)
- ✅ Dry run of full app with all pages

### Effort Balance

| Aspect | Time |
|--------|------|
| ML (preprocessing, data pipeline) | 55% |
| UI (Streamlit Predict page + app shell) | 35% |
| Docs (README, GitHub management) | 10% |

### Learning Outcomes

✨ **You will master:**
- Full OpenCV preprocessing pipeline and why each step matters
- How data quality and quantity determine the model's performance ceiling
- Streamlit session state, file uploaders, multi-page routing
- GitHub workflow (branching, merging, tagging) for team projects
- Data pipeline architecture (from raw images to prediction-ready features)

---

---

## 2️⃣ FAIQA — Feature Engineering + Live Demo Page

**Title:** Feature Extraction & EDA Lead  
**Primary Responsibility:** Design and extract handcrafted features, build Live Demo page  
**Streamlit Page:** 📄 **Live Demo**

### Build — ML Side (55%)

#### Feature Extraction Module
- [ ] **Write `src/feature_extraction.py`**

**Local Binary Patterns (LBP):**
```python
from skimage.feature import local_binary_pattern
import numpy as np

def extract_lbp_features(gray_img):
    """Extract LBP histogram (26 bins)"""
    radius = 3
    n_points = 8 * radius
    lbp = local_binary_pattern(gray_img, n_points, radius, method='uniform')
    hist, _ = np.histogram(lbp, bins=26, range=(0, 26))
    return hist / hist.sum()  # Normalize
```

**Edge Density Features:**
```python
def extract_edge_density(edge_map):
    """Extract edge density from 4×4 grid"""
    h, w = edge_map.shape
    grid_h, grid_w = h // 4, w // 4
    edge_features = []
    
    for i in range(4):
        for j in range(4):
            roi = edge_map[i*grid_h:(i+1)*grid_h, j*grid_w:(j+1)*grid_w]
            density = roi.sum() / roi.size
            edge_features.append(density)
    
    return np.array(edge_features)  # 16 values
```

**Full Feature Vector:**
```python
def extract_all_features(gray_img, edge_map):
    """Combine LBP (26) + edge density (16) = 42 features"""
    lbp_feat = extract_lbp_features(gray_img)
    edge_feat = extract_edge_density(edge_map)
    return np.concatenate([lbp_feat, edge_feat])

def extract_batch_features(image_dir):
    """Apply to full dataset, save features.csv"""
    features_list = []
    labels = []
    
    for class_name in ['normal', 'defective']:
        for img_file in os.listdir(f"{image_dir}/{class_name}"):
            img = cv2.imread(...)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(...)
            feat = extract_all_features(gray, edges)
            features_list.append(feat)
            labels.append(0 if class_name == 'normal' else 1)
    
    # Save to CSV
    df = pd.DataFrame(features_list)
    df['label'] = labels
    df.to_csv('features.csv', index=False)
```

#### Feature Scaler
- [ ] **Write scaler pipeline and save `scaler.pkl`**
  ```python
  from sklearn.preprocessing import StandardScaler
  
  X = pd.read_csv('features.csv').drop('label', axis=1)
  scaler = StandardScaler()
  X_scaled = scaler.fit_transform(X)
  
  joblib.dump(scaler, 'models/scaler.pkl')
  ```

#### Exploratory Data Analysis (EDA)
- [ ] **Write `notebooks/02_eda.ipynb`** — Jupyter notebook with:
  - Dataset summary (image counts, class balance %)
  - LBP feature distribution histograms (normal vs defective)
  - Edge density distribution (boxplot by class)
  - Sample image grid (3×3 per class)
  - Feature correlation heatmap (between LBP bins)
  - **Insight:** Which LBP bins are most discriminative?
  - **Insight:** Do classes have clearly separated feature distributions?

**Notebook sections:**
```markdown
1. Load Dataset
   - Image counts per class
   - Class balance check
   
2. Visualize Samples
   - Grid of sample images
   - Original, grayscale, edges side-by-side
   
3. Feature Distributions
   - LBP histogram per class
   - Edge density boxplot
   
4. Feature Analysis
   - Mean feature vector per class
   - Feature variance
   - Feature importance (rough ranking)
   
5. Insights & Recommendations
   - Are features discriminative enough?
   - Any preprocessing improvements?
```

### Build — UI Side (35%)

#### Live Demo Page (`pages/live_demo.py`)
- [ ] **Page layout:**
  - Header: "🎥 Live Defect Detection"
  - Real-time camera feed display
  - Control buttons
  - Prediction history sidebar

- [ ] **Camera Input & Streaming:**
  ```python
  st.title("🎥 Live Defect Detection")
  
  col1, col2 = st.columns([2, 1])
  with col1:
      with st.container():
          placeholder = st.empty()
  
  with col2:
      start_button = st.button("Start Detection")
      stop_button = st.button("Stop Detection")
  
  if start_button:
      cap = cv2.VideoCapture(0)
      frame_count = 0
      predictions_history = []
      
      while True:
          ret, frame = cap.read()
          frame_count += 1
          
          # Process frame
          pred, conf = predict_image(frame)
          predictions_history.append((frame, pred, conf))
          
          # Display annotated frame
          label = "🔴 DEFECTIVE" if pred == 1 else "🟢 NORMAL"
          cv2.putText(frame, label, (30, 50), ...)
          placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
          
          if stop_button or frame_count > 300:  # 10 sec at 30 fps
              break
      
      cap.release()
  ```

- [ ] **Start/Stop Controls:**
  - Buttons to begin and end live capture
  - Frame counter display
  - FPS indicator (frames processed per second)

- [ ] **Live Prediction History:**
  - Show last 5 captured frames in a grid
  - Display label and confidence for each
  - Scrollable history table
  ```python
  history_df = pd.DataFrame({
      'Frame #': [p[0] for p in predictions_history],
      'Prediction': [p[1] for p in predictions_history],
      'Confidence': [f"{p[2]:.1%}" for p in predictions_history]
  })
  st.dataframe(history_df)
  ```

- [ ] **Feature Visualization for Captured Frame:**
  - Show LBP pattern heatmap for last captured frame
  - Show edge map from that frame
  - Display feature vector as a bar chart (which features fired?)
  ```python
  if predictions_history:
      last_frame = predictions_history[-1][0]
      gray = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)
      edges = cv2.Canny(gray, 50, 150)
      
      col1, col2 = st.columns(2)
      with col1:
          st.image(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB), caption="Grayscale")
      with col2:
          st.image(edges, caption="Edges (Canny)")
      
      # Feature visualization
      feat = extract_all_features(gray, edges)
      st.bar_chart(feat)
  ```

#### OpenCV Backup Demo
- [ ] **Write `src/demo_live.py`** — pure OpenCV version (Streamlit webcam fallback)
  ```python
  import cv2
  import joblib
  from src.feature_extraction import extract_all_features
  
  cap = cv2.VideoCapture(0)
  model = joblib.load('models/best_model.pkl')
  scaler = joblib.load('models/scaler.pkl')
  
  while True:
      ret, frame = cap.read()
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      edges = cv2.Canny(gray, 50, 150)
      
      feat = extract_all_features(gray, edges)
      feat_scaled = scaler.transform([feat])
      pred = model.predict(feat_scaled)[0]
      
      label = "DEFECTIVE" if pred == 1 else "NORMAL"
      color = (0, 0, 255) if pred == 1 else (0, 255, 0)
      cv2.putText(frame, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
      
      cv2.imshow('VisionInspect AI - Live Demo', frame)
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  
  cap.release()
  cv2.destroyAllWindows()
  ```
  - Run with: `python src/demo_live.py`

### Documentation (10%)

#### Report Section: Data & Features
- [ ] Write 800–1000 word report section covering:
  - **Dataset Description:** Kaggle source, image counts, class balance
  - **Preprocessing Pipeline:** Why each step (grayscale, blur, Canny)
  - **Feature Engineering Rationale:**
    - Why LBP for crack detection? (texture patterns)
    - Why edge density? (structural information)
  - **Feature Distribution Analysis:** Insights from EDA
  - **Scaler Importance:** Why StandardScaler?

#### Presentation Slides
- [ ] Create 2–3 presentation slides:
  1. "What are LBP Features?" — visual explanation + histogram example
  2. "Feature Engineering for Crack Detection" — diagram of 42-dim vector
  3. "Live Demo Architecture" — data flow from camera → prediction

### Daily Deliverables

**Day 1 (Foundation):**
- ✅ `feature_extraction.py` — LBP function tested on 10 images
- ✅ Edge density extractor working correctly
- ✅ `notebooks/02_eda.ipynb` skeleton with data loading
- ✅ Live demo page shell (layout only, no camera yet)

**Day 2 (Integration):**
- ✅ Batch feature extraction completed on full dataset
- ✅ `features.csv` saved with labels
- ✅ `scaler.pkl` created and verified
- ✅ EDA notebook completed with all visualizations
- ✅ Live demo page: camera capture + basic prediction display

**Day 3 (Polish):**
- ✅ Feature visualization (LBP, edges, bar chart) in Live Demo
- ✅ Prediction history table with last 5 frames
- ✅ Pure OpenCV backup demo tested
- ✅ Report section written
- ✅ Presentation slides created

### Effort Balance

| Aspect | Time |
|--------|------|
| ML (LBP, edge density, EDA) | 55% |
| UI (Live Demo page + visualizations) | 35% |
| Docs (Report, slides, notebooks) | 10% |

### Learning Outcomes

✨ **You will master:**
- Local Binary Patterns (LBP) — why they encode texture, how to compute histograms
- Feature engineering from domain knowledge (why these 42 features for cracks?)
- How feature scaling affects ML model performance
- Real-time video processing with OpenCV (frame capture, annotation)
- Streamlit's camera_input and streaming patterns
- EDA techniques for understanding feature distributions and class separability

---

---

## 3️⃣ AYESHA — Model Training + Model Comparison Page

**Title:** ML Model Training & Hyperparameter Tuning Lead  
**Primary Responsibility:** Train 3 classifiers, optimize SVM, build Model Comparison page  
**Streamlit Page:** 📄 **Model Compare**

### Build — ML Side (55%)

#### Training Pipeline
- [ ] **Write `src/train.py`** — master training script
  ```python
  import pandas as pd
  import numpy as np
  from sklearn.model_selection import GridSearchCV, cross_val_score
  from sklearn.neighbors import KNeighborsClassifier
  from sklearn.svm import SVC
  from sklearn.ensemble import RandomForestClassifier
  import joblib
  
  # Load features
  X = pd.read_csv('features.csv').drop('label', axis=1).values
  y = pd.read_csv('features.csv')['label'].values
  
  # Train/val/test split (already done by Ifra, but we split features)
  # Assuming Ifra has organized train/val/test folders
  # Load features from each split
  X_train = ...  # train split features
  y_train = ...  # train split labels
  X_val = ...    # val split
  y_val = ...
  X_test = ...   # test split
  y_test = ...
  
  # Load scaler (trained by Faiqa)
  scaler = joblib.load('models/scaler.pkl')
  X_train = scaler.transform(X_train)
  X_val = scaler.transform(X_val)
  X_test = scaler.transform(X_test)
  
  # Model 1: KNN
  knn = KNeighborsClassifier(n_neighbors=5)
  knn.fit(X_train, y_train)
  knn_acc = knn.score(X_val, y_val)
  print(f"KNN Val Accuracy: {knn_acc:.4f}")
  joblib.dump(knn, 'models/knn.pkl')
  
  # Model 2: SVM with GridSearch
  svm_params = {
      'C': [0.1, 1, 10, 100],
      'gamma': ['scale', 'auto', 0.001, 0.01]
  }
  svm_base = SVC(kernel='rbf', probability=True)
  svm_grid = GridSearchCV(svm_base, svm_params, cv=5, scoring='f1')
  svm_grid.fit(X_train, y_train)
  
  print(f"Best SVM params: {svm_grid.best_params_}")
  svm_acc = svm_grid.score(X_val, y_val)
  print(f"SVM Val Accuracy: {svm_acc:.4f}")
  joblib.dump(svm_grid.best_estimator_, 'models/svm.pkl')
  
  # Model 3: Random Forest
  rf = RandomForestClassifier(n_estimators=200, max_depth=None)
  rf.fit(X_train, y_train)
  rf_acc = rf.score(X_val, y_val)
  print(f"RF Val Accuracy: {rf_acc:.4f}")
  joblib.dump(rf, 'models/rf.pkl')
  
  # Save training metadata
  metadata = {
      'knn_accuracy': knn_acc,
      'svm_accuracy': svm_acc,
      'rf_accuracy': rf_acc,
      'svm_best_params': svm_grid.best_params_,
      'training_date': datetime.now()
  }
  joblib.dump(metadata, 'models/metadata.pkl')
  ```

#### Model Training Details

**1. K-Nearest Neighbors (KNN)**
- [ ] Hyperparameter: `n_neighbors=5`
- [ ] Expected accuracy: 75–82%
- [ ] Train on full training set
- [ ] Evaluate on validation set

**2. Support Vector Machine (SVM) — RBF Kernel**
- [ ] **GridSearchCV on C and gamma:**
  - C values: [0.1, 1, 10, 100]
  - gamma values: ['scale', 'auto', 0.001, 0.01]
  - Cross-validation: 5-fold on training set
- [ ] Expected best params: C=10, gamma='scale'
- [ ] Expected accuracy: 83–90%
- [ ] **This is the expected winner** ⭐

**3. Random Forest**
- [ ] Hyperparameters: `n_estimators=200, max_depth=None`
- [ ] Expected accuracy: 80–88%
- [ ] Train on full training set

#### Training Notebook
- [ ] **Write `notebooks/03_model_training.ipynb`** — well-commented notebook
  ```markdown
  ## 1. Load Data & Features
  - Load features.csv (already created by Faiqa)
  - Load scaler.pkl
  - Apply StandardScaler to features
  
  ## 2. Model 1: KNN
  - Fit KNeighborsClassifier(n_neighbors=5)
  - Validate on val set
  - Explain: Why KNN? (distance-based, no assumptions)
  
  ## 3. Model 2: SVM (with GridSearch)
  - Explain: SVM maximizes margin between classes
  - Show GridSearchCV process
  - Plot: C vs gamma → accuracy heatmap
  - Print: Best parameters found
  
  ## 4. Model 3: Random Forest
  - Explain: Ensemble of decision trees
  - Feature importance ranking
  - Training time comparison
  
  ## 5. Results Summary
  - Table: Accuracy per model
  - Chart: Training time vs accuracy tradeoff
  - Conclusion: Which model wins and why
  ```

#### Model Saving & Metadata
- [ ] Save 3 trained models as `.pkl` files:
  - `models/knn.pkl`
  - `models/svm.pkl`
  - `models/rf.pkl`
- [ ] Save training metadata:
  - Validation accuracy per model
  - Training time per model
  - Best hyperparameters
  - Training date
  - Dataset version

### Build — UI Side (35%)

#### Model Comparison Page (`pages/model_compare.py`)
- [ ] **Page layout:**
  - Header: "⚖️ Model Comparison"
  - Key metrics comparison
  - Training time visualization
  - Summary table with highlighting

#### Grouped Bar Chart — Metrics
- [ ] Display metrics for all 3 models side-by-side:
  ```python
  import plotly.graph_objects as go
  
  models = ['KNN', 'SVM', 'Random Forest']
  accuracy = [0.78, 0.88, 0.84]
  precision = [0.75, 0.91, 0.85]
  recall = [0.80, 0.85, 0.82]
  f1 = [0.77, 0.88, 0.84]
  
  fig = go.Figure(data=[
      go.Bar(name='Accuracy', x=models, y=accuracy),
      go.Bar(name='Precision', x=models, y=precision),
      go.Bar(name='Recall', x=models, y=recall),
      go.Bar(name='F1-Score', x=models, y=f1)
  ])
  st.plotly_chart(fig)
  ```

#### Training Time Comparison
- [ ] Show speed vs accuracy tradeoff
  ```python
  training_times = {'KNN': 0.5, 'SVM': 15.2, 'RF': 8.7}  # seconds
  fig = go.Figure()
  fig.add_trace(go.Scatter(
      x=training_times.values(),
      y=accuracy,
      mode='markers+text',
      text=['KNN', 'SVM', 'RF'],
      textposition='top center',
      marker=dict(size=15)
  ))
  fig.update_layout(
      title="Speed vs Accuracy Tradeoff",
      xaxis_title="Training Time (seconds)",
      yaxis_title="Validation Accuracy"
  )
  st.plotly_chart(fig)
  ```

#### Summary Metrics Table
- [ ] Display all metrics in a table with highlighting:
  ```python
  metrics_df = pd.DataFrame({
      'Model': ['KNN', 'SVM', 'Random Forest'],
      'Accuracy': [0.78, 0.88, 0.84],
      'Precision': [0.75, 0.91, 0.85],
      'Recall': [0.80, 0.85, 0.82],
      'F1-Score': [0.77, 0.88, 0.84],
      'Training Time (s)': [0.5, 15.2, 8.7]
  })
  
  # Highlight best value per column
  def highlight_max(s):
      is_max = s == s.max()
      return ['background-color: lightgreen' if v else '' for v in is_max]
  
  st.dataframe(metrics_df.style.apply(highlight_max))
  ```

#### Best Model Callout
- [ ] Large banner highlighting the winner:
  ```python
  st.success("""
  🏆 **Best Model: SVM (RBF Kernel)**
  - Validation Accuracy: **88.2%**
  - F1-Score: **0.88**
  - Precision: **91.3%**
  
  SVM achieves the highest overall performance. It's optimized
  and ready for production deployment.
  """)
  ```

#### Model Explainer Sections
- [ ] Add expandable "How This Model Works" for each:
  ```python
  with st.expander("ℹ️ How KNN Works"):
      st.write("""
      **K-Nearest Neighbors** classifies based on the majority vote of 
      the k nearest training samples. With k=5, it looks at the 5 closest 
      neighbors in feature space and predicts the label that appears most.
      
      **Pros:** Simple, no training required, intuitive  
      **Cons:** Slow prediction, sensitive to irrelevant features
      """)
  
  with st.expander("ℹ️ How SVM Works"):
      st.write("""
      **Support Vector Machine** finds the optimal hyperplane that 
      maximizes the margin between classes. The RBF kernel allows 
      non-linear decision boundaries using a Gaussian basis function.
      
      **Pros:** Works well in high dimensions, effective for binary classification  
      **Cons:** Slower training, harder to interpret
      """)
  
  with st.expander("ℹ️ How Random Forest Works"):
      st.write("""
      **Random Forest** trains multiple decision trees on random subsets 
      of data and features, then aggregates their predictions by majority vote.
      
      **Pros:** Handles non-linear patterns, less prone to overfitting  
      **Cons:** Black box, can be slow for large datasets
      """)
  ```

#### GridSearch Visualization (Optional)
- [ ] Show GridSearch results as heatmap:
  ```python
  # Load SVM GridSearch results
  svm_results = pd.DataFrame({
      'C': [0.1, 0.1, 1, 1, 10, 10, 100, 100],
      'gamma': ['scale', 'auto'] * 4,
      'mean_score': [0.70, 0.68, 0.82, 0.80, 0.88, 0.86, 0.87, 0.85]
  })
  
  pivot_table = svm_results.pivot(index='C', columns='gamma', values='mean_score')
  fig = go.Figure(data=go.Heatmap(z=pivot_table.values, 
                                   x=pivot_table.columns, 
                                   y=pivot_table.index))
  st.plotly_chart(fig)
  ```

### Documentation (10%)

#### Report Section: Model Training & Comparison
- [ ] Write 1000–1200 word section covering:
  - **Overview:** Why 3 models? Rationale for choices
  - **KNN Details:** Hyperparameters, complexity, expected performance
  - **SVM Details:** 
    - RBF kernel explanation (handles non-linearity)
    - GridSearch methodology and results
    - Best hyperparameters found
  - **Random Forest Details:** Ensemble approach, generalization
  - **Comparison Results:** Which model won and why
  - **Production Choice:** Why SVM for deployment

#### Presentation Slides
- [ ] Create 2–3 slides:
  1. "Training 3 Classifiers" — model overview table
  2. "SVM GridSearch Results" — C vs gamma heatmap
  3. "Model Comparison & Winner" — metrics bar chart + callout

### Daily Deliverables

**Day 1 (Foundation):**
- ✅ Notebook skeleton for training (load data, split verification)
- ✅ KNN prototype trained and validated
- ✅ SVM GridSearch parameters defined
- ✅ Model Comparison page layout (skeleton, no data yet)

**Day 2 (Integration):**
- ✅ All 3 models trained on training set
- ✅ SVM GridSearch completed with best params recorded
- ✅ Validation accuracy measured for all models
- ✅ All 3 .pkl files saved
- ✅ Model Comparison page: bar chart + table with real data

**Day 3 (Polish):**
- ✅ Training time measurements added
- ✅ Best model callout banner
- ✅ "How This Model Works" expandables
- ✅ Final metrics verified on validation set
- ✅ Report section written
- ✅ Presentation slides created

### Effort Balance

| Aspect | Time |
|--------|------|
| ML (training, hyperparameter tuning, GridSearch) | 55% |
| UI (Model Comparison page, visualizations) | 35% |
| Docs (Report, slides, training notebook) | 10% |

### Learning Outcomes

✨ **You will master:**
- How KNN, SVM, and Random Forest differ fundamentally
- GridSearchCV workflow — parameter space, cross-validation, best estimator selection
- RBF kernel and non-linear decision boundaries in SVM
- Hyperparameter tuning and its impact on decision boundaries and generalization
- Why cross-validation matters more than a single train/test split
- Model performance comparison and selection criteria
- Training vs validation trade-offs and overfitting detection

---

---

## 4️⃣ WAJIHA — Evaluation & Metrics Page

**Title:** Evaluation & Error Analysis Lead  
**Primary Responsibility:** Comprehensive model evaluation, error analysis, build Metrics page  
**Streamlit Page:** 📄 **Metrics & Evaluation**

### Build — ML Side (55%)

#### Evaluation Pipeline
- [ ] **Write `src/evaluate.py`** — comprehensive evaluation script
  ```python
  import pandas as pd
  import numpy as np
  from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                               f1_score, confusion_matrix, roc_curve, auc, 
                               classification_report)
  import joblib
  import matplotlib.pyplot as plt
  import seaborn as sns
  
  # Load test set features
  X_test = ...  # test split features
  y_test = ...  # test split labels
  
  # Load scaler and models
  scaler = joblib.load('models/scaler.pkl')
  X_test = scaler.transform(X_test)
  
  knn = joblib.load('models/knn.pkl')
  svm = joblib.load('models/svm.pkl')
  rf = joblib.load('models/rf.pkl')
  
  # Predictions
  models = {'KNN': knn, 'SVM': svm, 'RF': rf}
  results = {}
  
  for model_name, model in models.items():
      y_pred = model.predict(X_test)
      y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
      
      # Metrics
      acc = accuracy_score(y_test, y_pred)
      prec = precision_score(y_test, y_pred)
      rec = recall_score(y_test, y_pred)
      f1 = f1_score(y_test, y_pred)
      
      # Confusion matrix
      cm = confusion_matrix(y_test, y_pred)
      
      # ROC curve
      if y_prob is not None:
          fpr, tpr, _ = roc_curve(y_test, y_prob)
          roc_auc = auc(fpr, tpr)
      
      results[model_name] = {
          'accuracy': acc,
          'precision': prec,
          'recall': rec,
          'f1': f1,
          'confusion_matrix': cm,
          'fpr': fpr,
          'tpr': tpr,
          'auc': roc_auc,
          'predictions': y_pred
      }
      
      print(f"\n{model_name}")
      print(f"Accuracy:  {acc:.4f}")
      print(f"Precision: {prec:.4f}")
      print(f"Recall:    {rec:.4f}")
      print(f"F1-Score:  {f1:.4f}")
      print(f"ROC-AUC:   {roc_auc:.4f}")
      print(f"\nConfusion Matrix:\n{cm}")
      print(f"\n{classification_report(y_test, y_pred)}")
  
  # Save results
  joblib.dump(results, 'results/eval_results.pkl')
  ```

#### Confusion Matrices
- [ ] **Generate and save confusion matrices for all 3 models:**
  ```python
  fig, axes = plt.subplots(1, 3, figsize=(15, 4))
  
  for idx, (model_name, result) in enumerate(results.items()):
      cm = result['confusion_matrix']
      sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx])
      axes[idx].set_title(f'{model_name} Confusion Matrix')
      axes[idx].set_ylabel('True Label')
      axes[idx].set_xlabel('Predicted Label')
  
  plt.tight_layout()
  plt.savefig('results/confusion_matrices.png', dpi=300, bbox_inches='tight')
  ```
  - **Interpretation guide** (for presentation):
    - TN (top-left): Correctly identified normal screens
    - FP (top-right): Normal screens misidentified as defective
    - FN (bottom-left): Defective screens missed (false negatives)
    - TP (bottom-right): Correctly identified defects

#### ROC Curves
- [ ] **Plot ROC curves for all 3 models on same axes:**
  ```python
  plt.figure(figsize=(10, 6))
  
  for model_name, result in results.items():
      fpr = result['fpr']
      tpr = result['tpr']
      auc_score = result['auc']
      plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc_score:.3f})')
  
  plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title('ROC Curve Comparison')
  plt.legend()
  plt.grid(True, alpha=0.3)
  plt.savefig('results/roc_curves.png', dpi=300, bbox_inches='tight')
  ```
  - **Interpretation:** Higher and more to the left = better classifier
  - AUC (Area Under Curve): 0.5 = random, 1.0 = perfect

#### Error Analysis
- [ ] **Identify misclassified images:**
  ```python
  def analyze_errors(X_test, y_test, y_pred, model_name):
      """Extract false positives and false negatives"""
      
      fp_indices = np.where((y_pred == 1) & (y_test == 0))[0]  # Predicted defective, actually normal
      fn_indices = np.where((y_pred == 0) & (y_test == 1))[0]  # Predicted normal, actually defective
      
      return {
          'false_positives': fp_indices,
          'false_negatives': fn_indices
      }
  
  # Save indices for later visualization
  for model_name, result in results.items():
      errors = analyze_errors(X_test, y_test, result['predictions'], model_name)
      joblib.dump(errors, f'results/{model_name.lower()}_errors.pkl')
  ```

#### Evaluation Notebook
- [ ] **Write `notebooks/04_evaluation.ipynb`** — analysis notebook
  ```markdown
  ## 1. Load Test Set & Models
  - Load test features (already split by Ifra)
  - Load 3 trained models
  
  ## 2. Compute Metrics
  - Accuracy, Precision, Recall, F1 per model
  - Classification report (detailed breakdown)
  
  ## 3. Confusion Matrix Analysis
  - Visualize all 3 matrices
  - Interpret TP, TN, FP, FN
  - Which model minimizes false negatives (critical for quality control)?
  
  ## 4. ROC Curve Analysis
  - Plot all 3 on same axes
  - Compute AUC for each
  - What does AUC mean?
  
  ## 5. Error Analysis
  - Extract false positives (normal screens flagged as defective)
  - Extract false negatives (defective screens missed)
  - Load and display actual images of errors
  - Analyze: why did the model fail on these?
  
  ## 6. Cost-Benefit Analysis
  - In production: what's worse, FP or FN?
  - False Negative: Miss a crack → customer complaints, returns
  - False Positive: Flag a good screen → extra review, higher cost
  - Recommendation: Optimize for high recall (catch all defects)?
  
  ## 7. Improvement Suggestions
  - More training data?
  - Better feature engineering?
  - Ensemble methods?
  - Threshold adjustment?
  ```

### Build — UI Side (35%)

#### Metrics Page (`pages/metrics.py`)
- [ ] **Page layout:**
  - Header: "📊 Evaluation & Metrics"
  - Model selector
  - Metrics display
  - Interactive visualizations
  - Error gallery

#### Model Selector & Metrics Display
- [ ] Interactive model selection:
  ```python
  st.title("📊 Evaluation & Metrics")
  
  selected_model = st.selectbox("Select Model", ['KNN', 'SVM', 'Random Forest'])
  
  # Load results
  results = joblib.load('results/eval_results.pkl')
  model_results = results[selected_model]
  
  # Display metrics
  col1, col2, col3, col4 = st.columns(4)
  with col1:
      st.metric("Accuracy", f"{model_results['accuracy']:.1%}")
  with col2:
      st.metric("Precision", f"{model_results['precision']:.1%}")
  with col3:
      st.metric("Recall", f"{model_results['recall']:.1%}")
  with col4:
      st.metric("F1-Score", f"{model_results['f1']:.1%}")
  ```

#### Confusion Matrix Display
- [ ] Show confusion matrix for selected model:
  ```python
  st.subheader("📋 Confusion Matrix")
  
  cm = model_results['confusion_matrix']
  
  fig = go.Figure(data=go.Heatmap(
      z=cm,
      x=['Predicted Normal', 'Predicted Defective'],
      y=['Actually Normal', 'Actually Defective'],
      text=cm,
      texttemplate="%{text}",
      colorscale='Blues'
  ))
  st.plotly_chart(fig)
  
  # Interpretation
  with st.expander("📖 How to Read This"):
      st.write("""
      - **Top-Left (TN):** Correctly identified normal screens
      - **Top-Right (FP):** Normal screens incorrectly flagged as defective
      - **Bottom-Left (FN):** Defective screens missed (critical errors!)
      - **Bottom-Right (TP):** Correctly identified defective screens
      
      **In quality control, FN (false negatives) are the most expensive** — 
      a defective product reaching a customer is worse than false alarms.
      """)
  ```

#### Classification Report Table
- [ ] Display detailed metrics:
  ```python
  st.subheader("📈 Detailed Classification Report")
  
  report_dict = classification_report(y_test, model_results['predictions'], 
                                      target_names=['Normal', 'Defective'], 
                                      output_dict=True)
  report_df = pd.DataFrame(report_dict).transpose()
  st.dataframe(report_df.style.highlight_max(axis=0))
  ```

#### ROC Curve Comparison (All Models)
- [ ] Plot ROC curves for all 3 models:
  ```python
  st.subheader("📉 ROC Curve Comparison (All Models)")
  
  fig = go.Figure()
  
  for model_name, model_res in results.items():
      fig.add_trace(go.Scatter(
          x=model_res['fpr'],
          y=model_res['tpr'],
          mode='lines',
          name=f"{model_name} (AUC={model_res['auc']:.3f})",
          line=dict(width=3)
      ))
  
  # Add random classifier line
  fig.add_trace(go.Scatter(
      x=[0, 1],
      y=[0, 1],
      mode='lines',
      name='Random Classifier',
      line=dict(dash='dash', color='gray')
  ))
  
  fig.update_layout(
      title="ROC Curves: All Models",
      xaxis_title="False Positive Rate",
      yaxis_title="True Positive Rate",
      hovermode='closest'
  )
  st.plotly_chart(fig)
  ```

#### Error Gallery
- [ ] Display misclassified images (FP + FN):
  ```python
  st.subheader("🔍 Error Gallery: Misclassified Images")
  
  errors = joblib.load(f'results/{selected_model.lower()}_errors.pkl')
  
  tab1, tab2 = st.tabs(["False Positives", "False Negatives"])
  
  with tab1:
      st.write(f"Normal screens incorrectly flagged as defective: {len(errors['false_positives'])} cases")
      
      fp_indices = errors['false_positives'][:9]  # Show max 9
      cols = st.columns(3)
      
      for idx, img_idx in enumerate(fp_indices):
          with cols[idx % 3]:
              img = load_test_image(img_idx)
              st.image(img, caption=f"FP #{idx+1}")
              st.caption("✅ Actually: Normal | ❌ Predicted: Defective")
  
  with tab2:
      st.write(f"Defective screens missed: {len(errors['false_negatives'])} cases (critical!)")
      
      fn_indices = errors['false_negatives'][:9]
      cols = st.columns(3)
      
      for idx, img_idx in enumerate(fn_indices):
          with cols[idx % 3]:
              img = load_test_image(img_idx)
              st.image(img, caption=f"FN #{idx+1}")
              st.caption("✅ Actually: Defective | ❌ Predicted: Normal")
  ```

#### Explainer Sections
- [ ] Add interpretation guides under each metric:
  ```python
  st.subheader("ℹ️ Metrics Explained")
  
  with st.expander("What does Accuracy mean?"):
      st.write("""
      **Accuracy** = (TP + TN) / (TP + TN + FP + FN)
      
      Percentage of all predictions that were correct. 
      **Warning:** Can be misleading for imbalanced datasets.
      """)
  
  with st.expander("What does Recall mean?"):
      st.write("""
      **Recall** = TP / (TP + FN)
      
      "Of all actual defects, how many did we catch?" 
      **Critical for quality control.** Missing defects (low recall) is expensive.
      """)
  
  with st.expander("What does Precision mean?"):
      st.write("""
      **Precision** = TP / (TP + FP)
      
      "Of all things we flagged as defective, how many actually were?"
      High precision = fewer false alarms.
      """)
  
  with st.expander("What is AUC/ROC?"):
      st.write("""
      **ROC Curve** shows the tradeoff between true positive rate and false positive rate.
      **AUC** (Area Under Curve) ranges from 0.5 (random) to 1.0 (perfect).
      Higher AUC = better classifier across all thresholds.
      """)
  ```

### Documentation (10%)

#### Report Section: Evaluation & Error Analysis
- [ ] Write 1000+ word section covering:
  - **Evaluation Methodology:** How was the model tested?
  - **Test Set Size & Composition:** How many images, class balance
  - **Metrics Definitions:** Accuracy, Precision, Recall, F1, ROC-AUC
  - **Results:** All 3 models' metrics side-by-side
  - **Confusion Matrix Interpretation:** What do FP/FN mean in production?
  - **Error Analysis:** 
    - What types of cracks does the model struggle with?
    - Are false positives or false negatives more common?
    - Why do these errors occur?
  - **Failure Modes:** Edge cases where the model fails
  - **Improvement Recommendations:** How could we do better?
  - **Production Implications:** Recall vs Precision tradeoff in quality control

#### Presentation Slides
- [ ] Create 2–3 slides:
  1. "Understanding Evaluation Metrics" — explain each metric visually
  2. "Confusion Matrix & ROC Curves" — show best model's matrices
  3. "Error Analysis & Insights" — live demo of error gallery, explain failure modes

### Daily Deliverables

**Day 1 (Foundation):**
- ✅ Evaluation script skeleton (metric computation functions)
- ✅ Confusion matrix generation code
- ✅ Metrics page layout (skeleton)

**Day 2 (Integration):**
- ✅ `evaluate.py` completed and tested on test set
- ✅ Confusion matrices generated and saved for all 3 models
- ✅ ROC curves plotted and saved
- ✅ Error indices extracted and saved
- ✅ Metrics page: model selector + confusion matrix display working

**Day 3 (Polish):**
- ✅ Error gallery populated with actual misclassified images
- ✅ All explainer sections written
- ✅ ROC comparison chart integrated
- ✅ Final evaluation notebook completed
- ✅ Report section written
- ✅ Presentation slides created

### Effort Balance

| Aspect | Time |
|--------|------|
| ML (evaluation, metrics, error analysis) | 55% |
| UI (Metrics page, visualizations, error gallery) | 35% |
| Docs (Report, slides, evaluation notebook) | 10% |

### Learning Outcomes

✨ **You will master:**
- Why accuracy alone is misleading; importance of precision/recall/F1
- Confusion matrix interpretation — costs of FP vs FN in real applications
- ROC curves and AUC — evaluating classifiers at all decision thresholds
- Error analysis techniques — understanding when and why models fail
- False positive vs false negative tradeoffs in quality control
- How to present model performance to non-technical stakeholders

---

---

## 🤝 Shared Responsibilities

### Presentation (Everyone)
- Each person creates **2–3 slides** about their own section
- Ifra assembles all slides and applies a **consistent visual theme**
- Final presentation: ~10 minutes + Q&A
- **Order:** Ifra (intro) → Faiqa (data+features) → Ayesha (models) → Wajiha (evaluation) → Ifra (conclusion)

### Report (Everyone)
- **Ifra:** Introduction + Conclusion + GitHub setup
- **Faiqa:** Dataset description + Preprocessing + Feature Engineering
- **Ayesha:** Model training + Hyperparameter tuning + Model comparison
- **Wajiha:** Evaluation methodology + Metrics + Error analysis
- **Format:** ~3000–4000 words total, academic style, include figures
- **Deadline:** Day 3, 2 PM (3 hours before presentation)

### About Page (Ifra)
- Simple Streamlit page with:
  - Team member names & roles
  - Project summary (2–3 sentences)
  - Tech stack
  - GitHub link
- **Time estimate:** 30 minutes
- **When:** Day 3 afternoon, after all core pages done

### Integration & Merging (Ifra)
- Each team member creates separate `.py` files for their Streamlit pages
- Ifra imports them all into `app.py` and handles routing
- **No merge conflicts** if everyone stays in their own file

---

## 📅 3-Day Timeline — Synchronized Checkpoints

### Day 1: Foundation

| Time | Ifra | Faiqa | Ayesha | Wajiha |
|------|------|-------|--------|--------|
| **Morning** | Repo setup, data download, split script | EDA skeleton, load dataset | Training notebook skeleton | Evaluation skeleton |
| **Afternoon** | Preprocessing.py implementation | LBP prototype on 5 images | KNN training | Confusion matrix generation |
| **EOD Checkpoint** | Can preprocess 1 image end-to-end | Can extract LBP + edge features | All 3 models trainable | Metrics computable |

### Day 2: Integration

| Time | Ifra | Faiqa | Ayesha | Wajiha |
|------|------|-------|--------|--------|
| **Morning** | Full dataset preprocessing | Batch feature extraction, scaler.pkl | SVM GridSearch start | Error analysis start |
| **Afternoon** | Predict page: uploader working | EDA notebook complete | GridSearch done, 3 models saved | Error images extracted |
| **EOD Checkpoint** | predict.py + Streamlit integration | features.csv ready, EDA done | All .pkl files saved, metadata logged | Confusion matrices + ROC curves done |

### Day 3: Polish

| Time | Ifra | Faiqa | Ayesha | Wajiha |
|------|------|-------|--------|--------|
| **Morning** | Webcam snapshot, batch predict | Feature viz in Live Demo, history table | Training time metrics, best model callout | Error gallery, explainers |
| **Afternoon** | README finalize, repo cleanup | Report section, slides | Report section, slides | Report section, slides |
| **EOD** | Tag v1.0.0, test full app | Final demo test | Final demo test | Final demo test |

---

## ✅ Integration Checklist (Ifra's Final Pass)

- [ ] All 4 Streamlit pages importable and working
- [ ] Sidebar navigation routing correctly
- [ ] Model selector dropdown loads correct .pkl across all pages
- [ ] All images load correctly (no broken paths)
- [ ] No hardcoded file paths (use relative paths: `models/`, `results/`)
- [ ] `.gitignore` excludes all large files (data/, models/*.pkl except one example)
- [ ] `requirements.txt` has all dependencies, pinned versions
- [ ] README has working installation & run instructions
- [ ] All team members' code follows same style (docstrings, variable names)
- [ ] GitHub repo ready for sharing (public, clean history, tagged release)

---

## 🎓 Key Learnings By Role

| Role | Key Concept | Why It Matters |
|------|------------|-----------------|
| **Ifra** | Data pipelines & preprocessing | 80% of model quality comes from data |
| **Faiqa** | Handcrafted features & textures | Classic ML depends on domain-specific features |
| **Ayesha** | Hyperparameter tuning & optimization | Small parameter changes = big accuracy gains |
| **Wajiha** | Evaluation & error analysis | Metrics reveal hidden patterns in failures |

---

## 📞 Communication Plan

- **Daily sync:** 15 min standup at 10 AM (or async Slack updates)
- **Blockers:** Mention immediately in chat
- **Code review:** Ifra merges branches end of Day 2, reviews for Day 3
- **Final check:** Ifra runs full app on Day 3 morning, reports any issues
- **Presentation rehearsal:** Day 3 at 4 PM (1 hour before final)

---

## 🚀 Success Metrics

✅ **Minimal:** All 4 pages working, live demo runs, presentation ready  
⭐ **Good:** Metrics on par with expectations (SVM ~88% accuracy), error analysis complete  
🏆 **Excellent:** Polished UI, comprehensive documentation, clear insights from error gallery  

---

**Document Updated:** 2026-05-15  
**Next Review:** Daily during project execution
