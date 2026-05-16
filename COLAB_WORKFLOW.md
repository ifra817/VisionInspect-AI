# 🚀 COLAB WORKFLOW GUIDE

This document outlines the **complete workflow for training models using Google Colab** while keeping the local development environment clean and lightweight.

---

## 📋 TABLE OF CONTENTS

1. [Overview](#-overview)
2. [Setup Instructions](#️-setup-instructions) — **READ THIS FIRST**
3. [Individual Workflows](#-individual-workflows)
4. [Execution Timeline](#-execution-timeline)
5. [Troubleshooting](#-troubleshooting)

---

## 🎯 OVERVIEW

This project uses a **two-phase workflow**:

### **Phase 1: Local Preparation** (Ifra, Faiqa)
- Preprocess images
- Extract features
- Prepare datasets
- Push code to GitHub

### **Phase 2: Colab Training** (Ayesha)
- Download repo from GitHub in Colab
- Run expensive computations (model training)
- Save trained models as `.pkl` files
- Download back to local `models/` folder
- Push to GitHub

### **Phase 3: Local Evaluation** (Wajiha)
- Load pre-trained models
- Evaluate on test set
- Generate visualizations
- Push results to GitHub

**Why Colab?**
- ✅ Free GPU (faster training)
- ✅ Keeps local machines light (no heavy computation)
- ✅ Everyone can work in parallel
- ✅ Professional ML workflow

---

## ⚙️ SETUP INSTRUCTIONS

### **STEP 1: Create Kaggle API Credentials** ⭐ IMPORTANT

Everyone needs their own Kaggle API key to download the dataset.

#### **A. Go to Kaggle Account Settings**
1. Visit: https://www.kaggle.com/settings/account
2. Scroll down to **"API"** section
3. Click **"Create New API Token"**
4. A file named **`kaggle.json`** will be downloaded

**The file looks like:**
```json
{
  "username": "your_kaggle_username",
  "key": "abcd1234efgh5678ijkl9012mnop3456"
}
```

#### **B. Place It in the Correct Location**

**On Windows:**
```
C:\Users\<YOUR_USERNAME>\.kaggle\kaggle.json
```

**On macOS/Linux:**
```
~/.kaggle/kaggle.json
```

#### **C. Set File Permissions (macOS/Linux only)**
```bash
chmod 600 ~/.kaggle/kaggle.json
```

#### **D. Verify It Works**
```bash
python -c "import kagglehub; print('✅ Kaggle API works!')"
```

**⚠️ IMPORTANT:**
- ❌ **DO NOT** share your `kaggle.json` with anyone
- ❌ **DO NOT** commit `kaggle.json` to GitHub
- ✅ Each person must create their own token
- ✅ Your token is personal and secure

---

## 👥 INDIVIDUAL WORKFLOWS

### **1️⃣ IFRA — Data Pipeline**

**Your Responsibilities:**
- ✅ Repository setup (DONE)
- ✅ Data download & split (DONE)
- ✅ Preprocessing pipeline (DONE)
- ✅ Streamlit app shell (TODO)
- ✅ Predict page UI (TODO)

**What You DON'T Do:**
- ❌ Model training (that's Ayesha in Colab)
- ❌ Feature extraction (that's Faiqa)

**Timeline:**
- Days 1-2: Complete local work
- Day 3: Finalize UI with models

---

### **2️⃣ FAIQA — Feature Engineering**

**Prerequisites:**
- ✅ Your own `kaggle.json` (see Setup Step 1)
- ✅ Python 3.10+
- ✅ Virtual environment

**Your Workflow:**

```bash
# Step 1: Clone the repo
git clone https://github.com/ifra817/VisionInspect-AI.git
cd VisionInspect-AI

# Step 2: Create virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Download & split dataset
python scripts/download_dataset.py
python scripts/split_dataset.py

# Expected output:
# ✅ NORMAL    : 68 images
# ✅ DEFECTIVE : 74 images
# ✅ Total: 142 images split into train/val/test

# Step 5: Write feature extraction code
# → Edit: src/feature_extraction.py
# → Extract LBP (26 features) + edge density (16 features)
# → Should return 42-dimensional feature vector

# Step 6: Extract features on dataset
python src/feature_extraction.py

# Expected output:
# ✅ features.csv created with 142 rows × 43 columns (42 features + label)
# ✅ models/scaler.pkl created (StandardScaler)

# Step 7: Create EDA notebook
# → Create: notebooks/02_eda.ipynb
# → Show feature distributions, class balance, sample visualizations

# Step 8: Write Live Demo page
# → Create: pages/live_demo.py
# → Implement webcam capture, real-time prediction, feature visualization

# Step 9: Push to GitHub
git add src/feature_extraction.py pages/live_demo.py notebooks/02_eda.ipynb models/scaler.pkl
git commit -m "feat: Add feature extraction and Live Demo page"
git push origin develop
```

**Key Files You Create:**
- `src/feature_extraction.py` — LBP + edge density extraction
- `pages/live_demo.py` — Webcam demo page
- `notebooks/02_eda.ipynb` — EDA analysis
- `models/scaler.pkl` — Feature scaler

**DO NOT commit to GitHub:**
- ❌ `data/` folder (too large)
- ❌ `features.csv` (regenerable)
- ✅ Everything else!

**Timeline:** Days 1-2 (can start immediately after Ifra pushes code)

---

### **3️⃣ AYESHA — Model Training (COLAB ONLY)** ⭐ MOST IMPORTANT

**⚠️ CRITICAL:** This workflow is **ENTIRELY in Google Colab**. No local training.

#### **Why Colab?**
- ✅ Free GPU (training 10x faster)
- ✅ Colab notebooks = saved in cloud
- ✅ Easy to share code + execution
- ✅ Don't need local GPU

#### **Your Colab Workflow:**

**Step 1: Create Colab Notebook**
1. Go to https://colab.research.google.com/
2. Create new notebook: **`training_notebook.ipynb`**

**Step 2: Clone Repository in Colab**
```python
# Cell 1: Clone repo
!git clone https://github.com/ifra817/VisionInspect-AI.git
%cd VisionInspect-AI
```

**Step 3: Setup Kaggle API in Colab**
```python
# Cell 2: Upload kaggle.json to Colab
from google.colab import files
files.upload()

# Cell 3: Move it to correct location
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
```

**Step 4: Install Dependencies**
```python
# Cell 4: Install requirements
!pip install -r requirements.txt
```

**Step 5: Download & Split Dataset**
```python
# Cell 5: Download dataset
!python scripts/download_dataset.py

# Cell 6: Split dataset
!python scripts/split_dataset.py

# Expected output:
# TOTAL IMAGES: 142
# TRAIN: 98 | VAL: 21 | TEST: 23
```

**Step 6: Extract Features**
```python
# Cell 7: Run feature extraction
# (Using Faiqa's code from GitHub)
!python src/feature_extraction.py

# Expected output:
# ✅ features.csv created
# ✅ models/scaler.pkl created
```

**Step 7: Train Models**
```python
# Cell 8: Write and run training script
# → Create/edit: src/train.py
# → Train KNN, SVM (with GridSearch), Random Forest
# → Save: models/knn.pkl, models/svm.pkl, models/rf.pkl, models/metadata.pkl

!python src/train.py

# Expected output:
# KNN Val Accuracy: 0.7619
# SVM Val Accuracy: 0.8571
# RF Val Accuracy: 0.8095
# ✅ All .pkl files saved to models/
```

**Step 8: Evaluate Models**
```python
# Cell 9: Run evaluation
# → Create/edit: src/evaluate.py
# → Generate confusion matrices, ROC curves, metrics

!python src/evaluate.py

# Expected output:
# ✅ results/confusion_matrices.png
# ✅ results/roc_curves.png
# ✅ results/eval_results.pkl
```

**Step 9: Download Models & Results Locally**
```python
# Cell 10: Download all output files
from google.colab import files

# Download .pkl files
!zip -r models.zip models/
files.download('models.zip')

# Download results
!zip -r results.zip results/
files.download('results.zip')
```

**Step 10: Push to GitHub Locally**
```bash
# After downloading:
# 1. Extract models.zip and results.zip to your local VisionInspect-AI/
# 2. Run:

git add models/ results/
git commit -m "feat: Add trained models and evaluation results from Colab"
git push origin develop
```

**Key Points:**
- ✅ **All code runs in Colab** (no local training)
- ✅ **Download .pkl files** to local `models/` folder after training
- ✅ **Push to GitHub** so Wajiha can evaluate
- ✅ **Save Colab notebook** as `colabs/training_notebook.ipynb`

**Your Code:**
- `src/train.py` — Training script (pushed to GitHub first, then run in Colab)
- `pages/model_compare.py` — Model comparison UI page
- `notebooks/03_model_training.ipynb` — Training analysis notebook

**Timeline:** Days 2-3 (after Faiqa finishes features)

---

### **4️⃣ WAJIHA — Evaluation & Metrics**

**Prerequisites:**
- ✅ Your own `kaggle.json`
- ✅ Pre-trained models in `models/` folder (pushed by Ayesha)

**Your Workflow:**

```bash
# Step 1: Clone repo (now has pre-trained models)
git clone https://github.com/ifra817/VisionInspect-AI.git
cd VisionInspect-AI

# Step 2: Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Download & split dataset
python scripts/download_dataset.py
python scripts/split_dataset.py

# Step 5: Extract features (use Faiqa's code)
python src/feature_extraction.py

# Step 6: Write evaluation script
# → Edit: src/evaluate.py
# → Load pre-trained models from models/
# → Evaluate on test set
# → Generate confusion matrices, ROC curves, metrics

python src/evaluate.py

# Expected output:
# ✅ results/confusion_matrices.png
# ✅ results/roc_curves.png
# ✅ results/model_comparison.png
# ✅ results/training_time.png
# ✅ results/eval_results.pkl

# Step 7: Write Metrics page
# → Create: pages/metrics.py
# → Display confusion matrices, ROC curves, error analysis

# Step 8: Create evaluation notebook
# → Create: notebooks/04_evaluation.ipynb
# → Detailed analysis of model performance, error cases

# Step 9: Push to GitHub
git add src/evaluate.py pages/metrics.py notebooks/04_evaluation.ipynb results/
git commit -m "feat: Add model evaluation and Metrics page"
git push origin develop
```

**Key Files You Create:**
- `src/evaluate.py` — Evaluation script
- `pages/metrics.py` — Metrics visualization page
- `notebooks/04_evaluation.ipynb` — Evaluation analysis
- `results/*.png` — Visualization outputs

**Timeline:** Day 3 (after Ayesha pushes trained models)

---

## ⏱️ EXECUTION TIMELINE

```
┌──────────────────────────────────────────────────────────────────┐
│ DAY 1 (May 17)                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ IFRA:   ✅ Preprocessing done (src/preprocessing.py)             │
│         ✅ Predict.py skeleton done                              │
│         → Push to develop                                        │
│                                                                  │
│ FAIQA:  ⏳ Waiting for Ifra to push code                          │
│         ✅ Set up Kaggle API (see Setup Step 1)                  │
│                                                                  │
│ AYESHA: ⏳ Waiting for Faiqa's features                           │
│                                                                  │
│ WAJIHA: ⏳ Waiting for everyone                                   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ DAY 2 (May 18)                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ IFRA:   ✅ app.py shell                                          │
│         ✅ pages/predict.py complete                             │
│         → Push to develop                                        │
│                                                                  │
│ FAIQA:  ✅ src/feature_extraction.py                             │
│         ✅ Extract features locally                              │
│         ✅ pages/live_demo.py                                    │
│         ✅ notebooks/02_eda.ipynb                                │
│         → Push to develop (NO data/, NO features.csv)            │
│                                                                  │
│ AYESHA: ⬜ COLAB TRAINING STARTS:                                │
│         ✅ Clone repo                                            │
│         ✅ Setup Kaggle API in Colab                             │
│         ✅ Download dataset                                      │
│         ✅ Extract features (Faiqa's code)                       │
│         ✅ Train models (src/train.py)                           │
│         ⏳ Still training... (GPU handles it)                     │
│                                                                  │
│ WAJIHA: ⏳ Waiting for trained models                             │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ DAY 2-3 EVENING (May 18-19)                                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ AYESHA: ✅ Models trained                                        │
│         ✅ Evaluate in Colab (src/evaluate.py)                   │
│         ✅ Download .pkl files                                   │
│         ✅ Download results/ visualizations                      │
│         ✅ pages/model_compare.py                                │
│         → Push to develop (models/ + results/)                   │
│                                                                  │
│ OTHERS: ⏳ Git pull to get latest models                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ DAY 3 (May 19)                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ IFRA:   ✅ Final Predict page polish                             │
│         ✅ Integrate with models                                 │
│         ✅ Test app.py end-to-end                                │
│                                                                  │
│ FAIQA:  ✅ Live Demo polish                                      │
│         ✅ Test webcam features                                  │
│                                                                  │
│ AYESHA: ✅ Model Compare page complete                           │
│         ✅ Test metrics display                                  │
│                                                                  │
│ WAJIHA: ✅ src/evaluate.py final run locally                     │
│         ✅ pages/metrics.py complete                             │
│         ✅ Error gallery + visualizations                        │
│         → Push final results                                     │
│                                                                  │
│ FINAL:  ✅ All 4 Streamlit pages working                         │
│         ✅ All code tested                                       │
│         ✅ develop branch → main                                 │
│         ✅ Tag v1.0.0                                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🚨 TROUBLESHOOTING

### **Problem: Kaggle API Authentication Error**

**Error Message:**
```
kaggle.api.kaggle_api_extended.KaggleApiHTTPError: 
Invalid API credentials. Please check your kaggle.json credentials.
```

**Solution:**
1. ✅ Verify `kaggle.json` exists in correct location:
   - Windows: `C:\Users\<YOUR_USERNAME>\.kaggle\kaggle.json`
   - macOS/Linux: `~/.kaggle/kaggle.json`
2. ✅ Check file permissions:
   - Should be readable (Windows: default OK)
   - macOS/Linux: `chmod 600 ~/.kaggle/kaggle.json`
3. ✅ Verify content has correct format:
   ```json
   {
     "username": "your_username",
     "key": "your_api_key"
   }
   ```
4. ✅ Don't share your API key!

---

### **Problem: Colab Out of Memory (OOM)**

**Error Message:**
```
RuntimeError: CUDA out of memory
```

**Solution:**
- ✅ Reduce batch size in `src/train.py`
- ✅ Reduce `n_estimators` in Random Forest
- ✅ Use `max_depth=15` for Random Forest (limit tree depth)
- ✅ Clear Colab cache: `!rm -rf /tmp/*`

---

### **Problem: Feature Extraction Takes Too Long**

**Error Message:**
```
Cell execution taking > 5 minutes
```

**Solution:**
- ✅ Normal for first run (142 images × feature extraction)
- ✅ Should take 2-5 minutes locally
- ✅ Faster in Colab with better CPU
- ⏳ Let it run, don't interrupt

---

### **Problem: Downloaded .pkl Files Won't Work Locally**

**Error Message:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'models/svm.pkl'
```

**Solution:**
1. ✅ Verify you extracted `models.zip` to repo root
2. ✅ Check file structure:
   ```
   VisionInspect-AI/
   ├── models/
   │   ├── knn.pkl ✅
   │   ├── svm.pkl ✅
   │   ├── rf.pkl  ✅
   │   └── scaler.pkl ✅
   ```
3. ✅ Run `git add models/` before push
4. ✅ Verify: `git status` shows `models/*.pkl`

---

### **Problem: features.csv Keeps Getting Committed**

**Error Message:**
```
On branch develop
Changes not staged for commit:
  modified:   features.csv
```

**Solution:**
- ✅ features.csv is in `.gitignore` (already done)
- ✅ Run: `git rm --cached features.csv`
- ✅ This removes it from Git tracking (keeps it locally)
- ✅ Don't commit it!

---

## 📝 CHECKLIST FOR EACH PERSON

### **FAIQA'S CHECKLIST**
- [ ] Kaggle API credentials set up (see Setup Step 1)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Dataset downloaded and split (scripts/ run)
- [ ] `src/feature_extraction.py` written
- [ ] Features extracted locally (`features.csv` created)
- [ ] `models/scaler.pkl` created
- [ ] `pages/live_demo.py` written
- [ ] `notebooks/02_eda.ipynb` created
- [ ] All changes pushed to `develop` branch
- [ ] Verified: no `data/` or `features.csv` in commits

### **AYESHA'S CHECKLIST**
- [ ] Kaggle API credentials set up in Colab
- [ ] Colab notebook created and shared/saved
- [ ] Dataset downloaded in Colab
- [ ] Features extracted in Colab (using Faiqa's code)
- [ ] `src/train.py` written (trains KNN, SVM, RF)
- [ ] Models trained and saved as `.pkl` files
- [ ] Evaluation script run (`src/evaluate.py`)
- [ ] Visualizations saved to `results/`
- [ ] `pages/model_compare.py` written
- [ ] `.pkl` files downloaded to local `models/`
- [ ] `results/` files downloaded to local `results/`
- [ ] All changes pushed to `develop` branch
- [ ] Colab notebook saved as `colabs/training_notebook.ipynb`

### **WAJIHA'S CHECKLIST**
- [ ] Kaggle API credentials set up
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Dataset downloaded and split
- [ ] Pre-trained models in `models/` folder
- [ ] Features extracted using Faiqa's code
- [ ] `src/evaluate.py` written
- [ ] Evaluation run on test set
- [ ] Visualizations saved to `results/`
- [ ] `pages/metrics.py` written
- [ ] `notebooks/04_evaluation.ipynb` created
- [ ] All changes pushed to `develop` branch
- [ ] Verified: all metrics accurate

---

## 🎯 KEY TAKEAWAYS

1. **Everyone needs their own `kaggle.json`** — Don't share it!
2. **Scripts are downloadable instructions** — Everyone runs them independently
3. **Colab does heavy lifting** — Ayesha trains, everyone else develops UI
4. **Don't commit `data/`, `features.csv`, `.pkl` files locally** — They're in `.gitignore`
5. **Ayesha downloads `.pkl` files** — Then commits them to GitHub for others
6. **Work in parallel** — Ifra/Faiqa work locally while Ayesha trains in Colab
7. **Final merge** — All branches merge to `develop` → `main` on Day 3

---

## 📞 SUPPORT

If you get stuck:
1. ✅ Check Troubleshooting section above
2. ✅ Check team_roles.md for detailed responsibilities
3. ✅ Check README.md for architecture overview
4. ✅ Ask in team Slack/Discord

---

**Last Updated:** 2026-05-16  
**Status:** Ready for team collaboration  
**Next Step:** Everyone follow their workflow above!
