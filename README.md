# VisionInspect AI

**Intelligent Visual Quality Inspection System using Machine Learning and OpenCV**

An advanced machine learning-based quality inspection system that uses computer vision and classical ML models to detect defects in smartphone screens. This project implements a complete pipeline from image preprocessing through model training and evaluation, culminating in a real-time webcam demonstration.

---

## 🎯 Project Overview

VisionInspect AI is designed to automatically detect cracks and defects in smartphone screens using intelligent image analysis. The core architecture follows this pipeline:

```
Images → OpenCV Preprocessing → Feature Extraction (LBP + Edge Density) 
→ Train 3 Classifiers (KNN, SVM, Random Forest) → Evaluate & Compare → Live Webcam Demo
```

**Key Features:**
- ✅ Automated preprocessing with OpenCV
- ✅ Advanced feature extraction using Local Binary Patterns (LBP)
- ✅ Multiple classifier comparison (KNN, SVM, Random Forest)
- ✅ Real-time webcam-based defect detection
- ✅ Interactive Streamlit web interface
- ✅ Comprehensive model evaluation and metrics

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

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.10+ | Core development |
| **Computer Vision** | OpenCV | Image preprocessing & webcam capture |
| **Feature Extraction** | scikit-image | Local Binary Pattern (LBP) computation |
| **Machine Learning** | scikit-learn | KNN, SVM, Random Forest, GridSearch |
| **Data Processing** | NumPy, Pandas | Array & data manipulation |
| **Visualization** | Matplotlib, Seaborn | Confusion matrices & performance charts |
| **Web UI** | Streamlit | Interactive web interface |
| **Model Persistence** | joblib | Save/load trained models |

### Installation

```bash
# Clone the repository
git clone https://github.com/ifra817/VisionInspect-AI.git
cd VisionInspect-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Requirements File
```
opencv-python==4.8.0.74
scikit-image==0.21.0
scikit-learn==1.3.0
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.1
seaborn==0.12.2
streamlit==1.25.0
joblib==1.3.1
```

---

## 🔬 OpenCV Preprocessing Pipeline

The preprocessing pipeline is optimized for crack detection and follows this exact sequence:

1. **Resize** → `cv2.resize(img, (128, 128))` — standardize input size
2. **Grayscale** → `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` — cracks are texture patterns, not color-dependent
3. **Gaussian Blur** → `cv2.GaussianBlur(gray, (5,5), 0)` — reduce noise
4. **Edge Detection** → `cv2.Canny(blurred, 50, 150)` — extract crack patterns
5. **Normalization** → `cv2.normalize(...)` — scale to 0–1 range

**What's NOT included:** Contour detection, thresholding, or GLCM (computational efficiency over 3-day timeline).

---

## 🧠 Feature Extraction

### Local Binary Patterns (LBP)
- **Purpose:** Captures micro-texture patterns; cracks appear as irregular LBP patterns
- **Implementation:** `skimage.feature.local_binary_pattern`
- **Parameters:** `radius=3, n_points=24, method='uniform'`
- **Output:** Normalized histogram (26 bins)

### Edge Density
- **Purpose:** Quantifies crack concentration across the image
- **Method:** Divide preprocessed image into 4×4 grid (16 regions)
- **Metric:** Total edge pixels / total pixels per region
- **Output:** 16 feature values

### Feature Vector
**Total dimensions:** 26 (LBP) + 16 (edge density) = **42 features**

All features are standardized using `sklearn.preprocessing.StandardScaler` before model training.

---

## 🤖 Machine Learning Models

Three classifiers are trained and compared for optimal performance:

| Model | Key Hyperparameters | Expected Accuracy | Training Time |
|-------|-------------------|-------------------|---------------|
| **K-Nearest Neighbors (KNN)** | `n_neighbors=5` (tuned via GridSearch) | 75–82% | Fast |
| **Support Vector Machine (SVM)** | `kernel='rbf', C=10, gamma='scale'` | **83–90%** | Medium |
| **Random Forest** | `n_estimators=200, max_depth=None` | 80–88% | Medium |

### Model Selection
**SVM with RBF kernel** is expected to achieve the highest accuracy and is recommended as the production model.

### Hyperparameter Tuning
- GridSearchCV with 5-fold cross-validation applied to SVM
- KNN and RF trained with default tuned parameters to conserve time

---

## 📁 Project Structure

```
VisionInspect-AI/
├── data/                          # Dataset directory
│   ├── train/
│   │   ├── normal/
│   │   └── defective/
│   ├── val/
│   │   ├── normal/
│   │   └── defective/
│   └── test/
│       ├── normal/
│       └── defective/
├── notebooks/                     # Jupyter notebooks for exploration
│   ├── 01_eda.ipynb              # Exploratory data analysis
│   ├── 02_preprocessing.ipynb    # Preprocessing validation
│   └── 03_model_training.ipynb   # Training & evaluation
├── src/                          # Source code modules
│   ├── preprocessing.py          # OpenCV preprocessing pipeline
│   ├── feature_extraction.py     # LBP & edge density extraction
│   ├── train.py                  # Model training & GridSearch
│   └── demo.py                   # Pure OpenCV webcam demo
├── models/                       # Trained model files (.pkl)
│   └── best_model.pkl
├── results/                      # Evaluation outputs
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   └── model_comparison.png
├── app.py                        # Streamlit web application
├── requirements.txt              # Python dependencies
├── .gitignore                    # Exclude large datasets
└── README.md                     # This file
```

---

## 🚀 Quick Start

### 1. Data Preparation
```bash
# Download dataset from Kaggle
# Organize into data/ folder with train/val/test structure
# Place train/val/test splits as shown above
```

### 2. Training
```bash
# Run the complete training pipeline
python src/train.py

# Output: best_model.pkl saved in models/
```

### 3. Web Interface (Streamlit)
```bash
streamlit run app.py
```
Navigate to `http://localhost:8501` to access the web interface.

Features:
- Image upload for quick prediction
- Real-time webcam feed analysis
- Model performance metrics
- Interactive defect visualization

### 4. Webcam Demo (OpenCV)
```bash
python src/demo.py
```
- Live detection on webcam feed
- **Press 'q' to quit**
- Green label: Normal screen
- Red label: Defective screen

---

## 📈 Model Evaluation

The pipeline generates comprehensive evaluation metrics:

### Metrics
- **Accuracy:** Overall correctness
- **Precision:** True positives among predicted defects
- **Recall:** Defect detection rate
- **F1-Score:** Harmonic mean of precision & recall
- **Confusion Matrix:** TP, TN, FP, FN breakdown
- **ROC Curve:** Trade-off between true positive and false positive rates

### Output Files
- `results/confusion_matrix.png` — Model-wise confusion matrices
- `results/roc_curve.png` — ROC curves for all models
- `results/model_comparison.png` — Accuracy/F1 comparison chart

---

## 📋 Implementation Timeline (3 Days)

### **Day 1 — Foundation**
- ✅ Clone repository, download dataset, set up environment
- ✅ Implement OpenCV preprocessing pipeline
- ✅ Prototype LBP feature extraction
- ✅ Build Streamlit UI skeleton
- **Checkpoint:** Load image → preprocess → extract features

### **Day 2 — Core ML**
- ✅ Integrate complete feature extraction pipeline
- ✅ Train KNN, SVM, and Random Forest on training set
- ✅ Perform SVM GridSearch with 5-fold CV
- ✅ Generate confusion matrices and evaluation metrics
- ✅ Connect Streamlit to trained models
- **Checkpoint:** All models trained, metrics computed, Streamlit upload functional

### **Day 3 — Polish & Demo**
- ✅ Integrate webcam real-time detection
- ✅ Final evaluation on test set
- ✅ Create comparison charts
- ✅ Prepare presentation slides
- ✅ Practice live demo walkthrough
- **Checkpoint:** Full dry run of presentation with live webcam demo

---

## 🎮 Live Webcam Demo

The webcam demo is implemented using OpenCV and provides real-time defect detection:

```python
cap = cv2.VideoCapture(0)
model = joblib.load('models/best_model.pkl')

while True:
    ret, frame = cap.read()
    features = extract_features(frame)
    pred = model.predict([features])[0]
    label = "DEFECTIVE" if pred == 1 else "NORMAL"
    color = (0, 0, 255) if pred == 1 else (0, 255, 0)
    cv2.putText(frame, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
    cv2.imshow('VisionInspect AI', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### Demo Requirements
- **Lighting:** Use consistent background and ambient lighting
- **Props:** Phone photo (printed or displayed on another screen)
- **Stability:** Test early on Day 3 before final presentation

---

## ⚙️ Configuration

### Preprocessing Parameters
```python
# Image size
IMG_SIZE = 128

# Gaussian blur kernel
BLUR_KERNEL = (5, 5)

# Canny edge detection thresholds
CANNY_LOW = 50
CANNY_HIGH = 150

# LBP parameters
LBP_RADIUS = 3
LBP_N_POINTS = 24
LBP_METHOD = 'uniform'

# Edge density grid
EDGE_GRID = 4  # 4x4 grid = 16 features
```

### Model Parameters
```python
# KNN
KNN_NEIGHBORS = 5

# SVM
SVM_KERNEL = 'rbf'
SVM_C = 10
SVM_GAMMA = 'scale'

# Random Forest
RF_N_ESTIMATORS = 200
RF_MAX_DEPTH = None

# GridSearchCV
CV_FOLDS = 5
```

---

## 🚨 Risk Mitigations

### Dataset Size
- **Risk:** If dataset < 200 images per class
- **Solution:** Aggressively augment using OpenCV (flips, rotation, brightness jitter) on Day 1

### Webcam Lighting
- **Risk:** Poor lighting causes unstable detections
- **Solution:** Test lighting setup early on Day 3; maintain consistent background

### Streamlit Webcam Issues
- **Risk:** Webcam capture may be problematic in Streamlit
- **Solution:** Use pure OpenCV demo as fallback (20 lines, always reliable)

---

## 📚 Key References

- **OpenCV Documentation:** https://docs.opencv.org/
- **scikit-learn:** https://scikit-learn.org/stable/
- **scikit-image LBP:** https://scikit-image.org/docs/stable/api/skimage.feature.html#local_binary_pattern
- **Streamlit:** https://docs.streamlit.io/
- **Kaggle Datasets:** https://www.kaggle.com/datasets

---

## 👥 Team Collaboration

This project is designed for a 4-person team with clear role separation:

| Role | Responsibility |
|------|-----------------|
| **M1 — Data & Preprocessing** | Dataset setup, OpenCV pipeline, augmentation |
| **M2 — Feature Engineering** | LBP extraction, edge density, feature vectors |
| **M3 — ML Models** | KNN, SVM, RF training, GridSearch, evaluation |
| **M4 — Evaluation & Demo** | Metrics, Streamlit UI, webcam demo, presentation |

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📞 Support

For questions or issues, please open a GitHub Issue in the repository.

---

## ✨ Acknowledgments

This project implements a classical machine learning approach to visual quality inspection, combining traditional computer vision techniques (OpenCV, LBP) with modern ML frameworks (scikit-learn) for practical defect detection applications.

---

**Last Updated:** 2026-05-15  
**Project Status:** Development in Progress  
**Version:** 1.0.0
