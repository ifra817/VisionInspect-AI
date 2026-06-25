# VisionInspect AI

**Intelligent Visual Quality Inspection System using Machine Learning and OpenCV**

An advanced machine learning-based quality inspection system that uses computer vision and classical ML models to detect defects in smartphone screens. This project implements a complete pipeline from image preprocessing through model training and evaluation, culminating in a real-time Streamlit web application with live webcam demonstration.

---

## 🎯 Project Overview

VisionInspect AI is designed to automatically detect cracks and defects in smartphone screens using intelligent image analysis. The core architecture follows this pipeline:

```
Images → OpenCV Preprocessing → Feature Extraction (LBP + Edge Density) 
→ Train 3 Classifiers (KNN, SVM, Random Forest) → Evaluate & Compare 
→ Streamlit Web UI with Live Webcam Demo
```

**Key Features:**
- ✅ Automated preprocessing with OpenCV
- ✅ Advanced feature extraction using Local Binary Patterns (LBP)
- ✅ Multiple classifier comparison (KNN, SVM, Random Forest)
- ✅ Interactive 4-page Streamlit web application
- ✅ Real-time webcam-based defect detection
- ✅ Comprehensive model evaluation with error analysis
- ✅ Beautiful visualizations with Plotly and Seaborn
- ✅ Efficient Colab-based model training

---

## 📊 Dataset

### Dataset Source
**"Cracked and Intact Smartphone Images Dataset"** available on [Kaggle](https://www.kaggle.com/)

**Search terms:** `smartphone cracked screen dataset`

### Dataset Requirements
- **Minimum size:** 300–500 images per class
- **Classes:** 
  - Normal (intact screens)
  - Defective (cracked screens)
- **Augmentation:** If dataset is smaller, use OpenCV augmentation (flips, brightness jitter, slight rotation)

### Dataset Structure
```
data/
├── train/
│   ├── normal/
│   └── defective/
├── val/
│   ├── normal/
│   └── defective/
└── test/
    ├── normal/
    └── defective/
```

**Train/Val/Test Split:** 70% / 15% / 15%

---

## 🛠️ Tech Stack

| Category | Technology | Purpose | Version |
|----------|-----------|---------|---------|
| **Language** | Python | Core development | 3.10+ |
| **Computer Vision** | OpenCV | Image preprocessing & webcam capture | 4.8.0+ |
| **Feature Extraction** | scikit-image | Local Binary Pattern (LBP) computation | 0.21.0+ |
| **Machine Learning** | scikit-learn | KNN, SVM, RF, GridSearch, StandardScaler | 1.3.0+ |
| **Data Processing** | NumPy | Array & numerical operations | 1.24.0+ |
| **Data Analysis** | Pandas | Data manipulation & CSV handling | 2.0.0+ |
| **Visualization** | Matplotlib | Static plots & confusion matrices | 3.7.0+ |
| **Interactive Plots** | Seaborn | Enhanced heatmaps & statistical visualizations | 0.12.0+ |
| **Interactive Charts** | Plotly | Interactive ROC curves & bar charts | 5.13.0+ |
| **Web Framework** | Streamlit | Multi-page interactive web application | 1.25.0+ |
| **Model Persistence** | joblib | Save/load trained models & scalers | 1.3.0+ |

---

## 🌐 Streamlit Application

The project includes a **4-page Streamlit web application** with comprehensive visualization and prediction capabilities:

### Application Pages

**1. 🔍 Predict Page**
- Single image upload (drag & drop or file selector)
- Live camera snapshot capture
- Image preprocessing visualization (original → grayscale → edges)
- Real-time prediction with confidence score
- Model selector dropdown (KNN / SVM / RF)
- Batch prediction for multiple images
- Batch results download as CSV

**2. 🎥 Live Demo Page**
- Real-time webcam feed with continuous frame processing
- Start/Stop controls for live detection
- Frame-by-frame prediction display
- Live prediction history (last 5–10 frames)
- Feature visualization:
  - LBP pattern heatmap
  - Edge map visualization
  - Feature vector bar chart
- FPS (frames per second) indicator
- Downloadable detection report

**3. ⚖️ Model Comparison Page**
- Interactive metrics comparison (Accuracy, Precision, Recall, F1-Score)
- Grouped bar chart showing all metrics for KNN, SVM, Random Forest
- Training time vs accuracy tradeoff visualization
- Summary metrics table with best values highlighted
- Best model callout banner with confidence score
- Expandable "How This Model Works" sections (plain English explanations)
- GridSearch results heatmap (C vs gamma for SVM)

**4. 📊 Metrics & Evaluation Page**
- Model selector dropdown for detailed metrics
- Confusion matrix heatmap (with interpretation guide)
- Classification report table
- ROC curve comparison (all 3 models on same plot)
- Error gallery:
  - Grid of false positive images (normal flagged as defective)
  - Grid of false negative images (defective missed)
  - Image count per category
- Interactive explainers:
  - "What does Accuracy mean?"
  - "What does Recall mean?" (especially important for quality control)
  - "What is AUC/ROC?"
  - "Cost-benefit analysis of FP vs FN"

### Sidebar Navigation
- Project title & brief description
- Navigation buttons for all 4 pages
- Model selector dropdown (shared across all pages)
- Quick stats panel (selected model's accuracy)
- Project GitHub link

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Installation (Local)

1. **Clone the repository**
   ```bash
   git clone https://github.com/ifra817/VisionInspect-AI.git
   cd VisionInspect-AI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application**
   ```bash
   streamlit run app.py
   ```
   
   The application will open in your browser at `http://localhost:8501`

---

## 📋 Project Structure

```
VisionInspect-AI/
├── data/                          # Dataset directory (gitignored)
│   ├── train/
│   │   ├── normal/
│   │   └── defective/
│   ├── val/
│   │   ├── normal/
│   │   └── defective/
│   └── test/
│       ├── normal/
│       └── defective/
│
├── notebooks/                     # Jupyter notebooks for analysis
│   ├── 01_eda.ipynb              # Exploratory data analysis
│   ├── 02_preprocessing.ipynb    # Preprocessing validation & testing
│   ├── 03_model_training.ipynb   # Model training & GridSearch process
│   └── 04_evaluation.ipynb       # Evaluation & error analysis
│
├── src/                          # Source code modules
│   ├── __init__.py
│   ├── preprocessing.py          # OpenCV preprocessing pipeline
│   ├── feature_extraction.py     # LBP & edge density extraction
│   ├── train.py                  # Model training & GridSearch
│   ├── evaluate.py               # Model evaluation & metrics
│   └── demo_live.py              # Pure OpenCV backup demo (fallback)
│
├── pages/                        # Streamlit pages
│   ├── __init__.py
│   ├── predict.py                # Predict page (Ifra)
│   ├── live_demo.py              # Live Demo page (Faiqa)
│   ├── model_compare.py          # Model Comparison page (Ayesha)
│   └── metrics.py                # Metrics & Evaluation page (Wajiha)
│
├── models/                       # Trained model files
│   ├── knn.pkl                   # Trained KNN model
│   ├── svm.pkl                   # Trained SVM model (best)
│   ├── rf.pkl                    # Trained Random Forest model
│   ├── scaler.pkl                # Feature StandardScaler
│   └── metadata.pkl              # Training metadata
│
├── results/                      # Evaluation outputs & visualizations
│   ├── confusion_matrices.png    # Confusion matrix comparison
│   ├── roc_curves.png            # ROC curve comparison
│   ├── model_comparison.png      # Metrics bar chart
│   ├── training_time.png         # Training time comparison
│   └── eval_results.pkl          # Detailed evaluation metrics
│
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── COLAB_WORKFLOW.md             # Colab training guide
├── README.md                     # This file
├── team_roles.md                 # Team responsibilities & assignments
└── LICENSE                       # Project license
```

---

## 🔬 OpenCV Preprocessing Pipeline

The preprocessing pipeline is optimized for crack detection. Each image undergoes this exact sequence:

### Preprocessing Steps

1. **Resize** → `cv2.resize(img, (128, 128))`
   - Standardizes input size for consistent feature extraction
   - 128×128 balances detail preservation with computational efficiency

2. **Grayscale Conversion** → `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
   - Cracks are texture patterns, not color-dependent
   - Reduces dimensionality for faster feature extraction

3. **Gaussian Blur** → `cv2.GaussianBlur(gray, (5,5), 0)`
   - Noise reduction and smoothing
   - Kernel size (5,5) balances noise removal with edge preservation

4. **Canny Edge Detection** → `cv2.Canny(blurred, 50, 150)`
   - Extracts edge maps that highlight crack structures
   - Thresholds: 50 (low), 150 (high) for crack detection
   - Output: binary edge map

5. **Normalization** → `cv2.normalize(...)`
   - Scales pixel values to [0, 1] range
   - Ensures consistent input for feature extraction

### Code Example
```python
from src.preprocessing import preprocess_image

# Preprocess single image
img_path = "data/test/defective/image_001.jpg"
preprocessed = preprocess_image(img_path)  # Returns grayscale and edge map
```

---

## 🧠 Feature Extraction

### Local Binary Patterns (LBP) - 26 Features
**Purpose:** Captures micro-texture patterns; cracks appear as irregular LBP patterns

- **Implementation:** `skimage.feature.local_binary_pattern`
- **Parameters:** radius=3, n_points=24, method='uniform'
- **Output:** Normalized histogram with 26 bins
- **Why it works:** LBP encodes local texture variations that distinguish cracks from intact surfaces

### Edge Density - 16 Features
**Purpose:** Quantifies crack concentration and distribution across image

- **Method:** Divide preprocessed image into 4×4 grid (16 regions)
- **Metric:** Total edge pixels / total pixels per region
- **Output:** 16 feature values representing edge density per region
- **Why it works:** Defective screens have concentrated edge density in crack areas

### Feature Vector - 42 Dimensions
```
[26 LBP bins] + [16 Edge density values] = 42 total features
```

All features are standardized using `sklearn.preprocessing.StandardScaler` before model training.

### Code Example
```python
from src.feature_extraction import extract_all_features

# Extract features from preprocessed image
gray_img = ...     # grayscale image
edge_map = ...     # edge detection output
features = extract_all_features(gray_img, edge_map)  # 42-dim vector
```

---

## 🤖 Machine Learning Models

Three classifiers are trained, evaluated, and compared for optimal performance:

### Model Comparison

| Model | Algorithm | Key Hyperparameters | Expected Accuracy | Training Speed | Interpretability |
|-------|-----------|-------------------|------------------|-----------------|-----------------|
| **KNN** | K-Nearest Neighbors | `n_neighbors=5` | 75–82% | ⚡ Fast | ✅ High |
| **SVM** 🏆 | Support Vector Machine (RBF) | `kernel='rbf', C=10, gamma='scale'` | **83–90%** | ⏱️ Medium | ⚠️ Low |
| **RF** | Random Forest | `n_estimators=200, max_depth=None` | 80–88% | ⏱️ Medium | ✅ Medium |

### Recommended Model
**SVM with RBF kernel** is expected to achieve the highest accuracy and is recommended as the production model.

### Hyperparameter Tuning
- **GridSearchCV** applied to SVM with 5-fold cross-validation
- Parameter grid:
  - C values: [0.1, 1, 10, 100]
  - gamma values: ['scale', 'auto', 0.001, 0.01]
- KNN and RF use optimized default parameters for time efficiency

### Code Example
```python
from src.train import train_all_models

# Train all three models (runs in Colab)
train_all_models(X_train, y_train, X_val, y_val)
# Outputs: knn.pkl, svm.pkl, rf.pkl, metadata.pkl
```

---

## 📈 Model Evaluation

The project provides comprehensive evaluation metrics and visualizations:

### Evaluation Metrics

- **Accuracy** — Overall correctness rate
- **Precision** — True positives among predicted defects (important to avoid false alarms)
- **Recall** — Defect detection rate (critical: don't miss actual defects!)
- **F1-Score** — Harmonic mean of precision & recall
- **ROC-AUC** — Area Under Curve; evaluates performance across all decision thresholds
- **Confusion Matrix** — Breakdown of TP, TN, FP, FN

### Confusion Matrix Interpretation

```
                 Predicted
                Normal  Defective
Actual  Normal  [TN]    [FP]        ← False Positives (false alarms)
        Defective[FN]    [TP]        ↑ False Negatives (missed defects - critical!)
```

**In Quality Control:**
- **False Negatives (FN)** are most costly — defective product reaches customer
- **False Positives (FP)** cause extra review — less critical than FN

### ROC Curve
- Plots True Positive Rate vs False Positive Rate
- AUC: 0.5 (random) to 1.0 (perfect)
- Higher & further left = better classifier

### Output Files
- `results/confusion_matrices.png` — All 3 models' confusion matrices
- `results/roc_curves.png` — ROC curves comparison
- `results/eval_results.pkl` — Detailed metrics dictionary

---

## 🎮 Live Webcam Demo

### Streamlit Live Demo Page
The Streamlit Live Demo page provides real-time detection with full feature visualization:

```python
# Click "Start Detection" button
# - Captures frames from webcam
# - Preprocesses each frame
# - Extracts features
# - Predicts defect status
# - Displays with confidence score
# - Shows feature visualizations (LBP, edges, feature vector)
# - Maintains history of last 5-10 predictions
```

### Pure OpenCV Fallback Demo
If Streamlit webcam issues occur, run the pure OpenCV version:

```bash
python src/demo_live.py
```

**Output:**
- Live video window with annotations
- Green label: **NORMAL** (intact screen)
- Red label: **DEFECTIVE** (crack detected)
- Confidence score displayed
- Press **'q'** to quit

---

## ⚙️ Configuration Parameters

### Preprocessing Configuration
```python
IMG_SIZE = 128                  # Image resize dimension
BLUR_KERNEL = (5, 5)           # Gaussian blur kernel
CANNY_LOW = 50                 # Canny low threshold
CANNY_HIGH = 150               # Canny high threshold
NORMALIZE_RANGE = [0, 1]       # Normalization range
```

### Feature Extraction Configuration
```python
# LBP Parameters
LBP_RADIUS = 3
LBP_N_POINTS = 24
LBP_METHOD = 'uniform'
LBP_BINS = 26

# Edge Density Grid
EDGE_GRID_SIZE = 4             # 4x4 grid = 16 features
TOTAL_FEATURES = 42            # 26 LBP + 16 edge density
```

### Model Hyperparameters
```python
# KNN
KNN_NEIGHBORS = 5

# SVM (GridSearch best params)
SVM_KERNEL = 'rbf'
SVM_C = 10
SVM_GAMMA = 'scale'

# Random Forest
RF_N_ESTIMATORS = 200
RF_MAX_DEPTH = None
RF_MIN_SAMPLES_SPLIT = 2

# GridSearchCV Configuration
CV_FOLDS = 5
RANDOM_STATE = 42
```

### Data Split Configuration
```python
TRAIN_SPLIT = 0.70             # 70% training
VAL_SPLIT = 0.15               # 15% validation
TEST_SPLIT = 0.15              # 15% testing
```

---

## 📚 Jupyter Notebooks

Explore the project with detailed notebooks:

### 1. **01_eda.ipynb** — Exploratory Data Analysis
- Dataset statistics (image counts, class balance)
- Sample image visualizations
- Feature distributions (LBP, edge density)
- Class separability analysis
- Preprocessing step visualization

### 2. **02_preprocessing.ipynb** — Preprocessing Validation
- Preprocessing pipeline walkthrough
- Before/after image comparisons
- Augmentation techniques (if needed)
- Batch processing verification

### 3. **03_model_training.ipynb** — Model Training
- Feature loading and scaling
- Individual model training walkthrough
- GridSearchCV process for SVM
- Training time measurements
- Validation accuracy comparison

### 4. **04_evaluation.ipynb** — Evaluation & Error Analysis
- Test set evaluation
- Confusion matrix interpretation
- ROC curve analysis
- Error case visualization
- Failure mode analysis
- Improvement recommendations

---

## 🚨 Risk Mitigations & Troubleshooting

### Dataset Size
- **Risk:** Dataset too small (< 300 images per class)
- **Solution:** Use OpenCV augmentation (flips, rotation, brightness jitter)

### Webcam Issues
- **Risk:** Streamlit camera_input instability
- **Solution:** Fall back to pure OpenCV demo (`python src/demo_live.py`)

### Poor Lighting Conditions
- **Risk:** Unstable real-time predictions
- **Solution:** Test lighting setup early; maintain consistent background

### GPU/Memory Constraints
- **Risk:** Slow model training or evaluation
- **Solution:** Use Colab for training; download pre-trained models locally

### Model Performance
- **Risk:** SVM or RF underperforming expectations
- **Solution:** Revisit feature engineering; check data quality; tune hyperparameters further

---

## 👥 Team Collaboration

This project is developed by a 4-person team with clear role separation:

| Member | Role | Pages | Responsibilities |
|--------|------|-------|------------------|
| **Ifra** | Lead & Data Pipeline | Predict | Repo setup, preprocessing, app shell |
| **Faiqa** | Feature Engineering | Live Demo | LBP extraction, EDA, live webcam |
| **Ayesha** | Model Training | Model Compare | Colab training, GridSearch, model metrics |
| **Wajiha** | Evaluation | Metrics | Evaluation, error analysis, ROC curves |

For detailed responsibilities, see **[team_roles.md](team_roles.md)**.

---

## 📊 Key Insights

### Why This Architecture?

1. **OpenCV Preprocessing**
   - Proven effective for crack detection
   - Canny edges specifically highlight linear structures (cracks)

2. **Local Binary Patterns (LBP)**
   - Classical texture descriptor, effective for surface defects
   - Computationally efficient (no deep learning overhead)
   - Interpretable — shows what features matter

3. **Multiple Classifiers**
   - Comparison reveals which algorithm suits the data best
   - SVM RBF kernel handles non-linear patterns without overfitting

4. **Streamlit UI**
   - Interactive web app with zero frontend knowledge needed
   - Live demo directly addresses the use case
   - Error gallery provides transparency into failure modes

5. **Colab-based Training**
   - Keeps local machines lightweight
   - Leverages free GPU resources
   - Enables parallel UI development

---

## 🎓 Learning Outcomes

Participants will master:
- ✅ Full OpenCV preprocessing pipeline for computer vision
- ✅ Classical feature engineering (LBP, edge analysis)
- ✅ Classical ML model training and hyperparameter optimization
- ✅ Model evaluation beyond accuracy (precision, recall, ROC-AUC)
- ✅ Error analysis and debugging ML systems
- ✅ Building interactive web applications with Streamlit
- ✅ Real-time video processing and prediction
- ✅ End-to-end ML project management and team collaboration
- ✅ Cloud-based training workflows (Google Colab)

---

## 📝 References

- **OpenCV Documentation:** https://docs.opencv.org/
- **scikit-learn:** https://scikit-learn.org/stable/
- **scikit-image LBP:** https://scikit-image.org/docs/stable/api/skimage.feature.html
- **Streamlit Documentation:** https://docs.streamlit.io/
- **Plotly:** https://plotly.com/python/
- **Kaggle Datasets:** https://www.kaggle.com/datasets
- **Google Colab Guide:** https://colab.research.google.com/

---

## 📞 Support & Contribution

### Issues & Bugs
- Open an issue on GitHub with:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs actual behavior
  - Screenshots if applicable

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add feature description'`
4. Push to branch: `git push origin feature/your-feature`
5. Open Pull Request with detailed description

---

## ✨ Acknowledgments

VisionInspect AI combines classical computer vision techniques (OpenCV, LBP) with modern ML frameworks (scikit-learn, Streamlit) to create a practical quality inspection solution. This approach demonstrates that sophisticated ML systems don't always require deep learning — domain expertise and well-engineered features can be equally powerful. The Colab-based training workflow enables efficient resource utilization without expensive hardware.

---

**Team:** Ifra, Faiqa, Ayesha, Wajiha  

*For team-specific responsibilities and implementation timeline, see [team_roles.md](team_roles.md)*

*For Colab training workflow, see [COLAB_WORKFLOW.md](COLAB_WORKFLOW.md)*
