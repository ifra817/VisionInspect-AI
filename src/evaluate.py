"""
EVALUATION MODULE FOR VISIONINSPECT AI
================================================================================
FILE PURPOSE:
This module evaluates trained models on test sets. It generates:
  1. Classification Metrics (Accuracy, Precision, Recall, F1)
  2. Confusion Matrix visualization
  3. ROC-AUC curve and score
  4. Per-class performance breakdown
  5. Batch predictions on entire datasets
================================================================================
"""

import sys
import argparse
import warnings
from pathlib import Path
from typing import Tuple, Dict, List, Any, Optional, Union

# Data science imports
import numpy as np
import pandas as pd
import cv2
import joblib

# Sklearn metrics
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    classification_report,
)

warnings.filterwarnings('ignore')

# ============================================================================

MODELS_DIR = Path("models")
CLASS_NAMES = {0: "NORMAL", 1: "DEFECTIVE"}
SUPPORTED_MODELS = ["knn", "svm", "rf"]

# ============================================================================

def extract_lbp_features(gray_img: np.ndarray) -> np.ndarray:
    from skimage.feature import local_binary_pattern
    radius = 3
    n_points = 8 * radius
    method = 'uniform'
    lbp_computed = local_binary_pattern(gray_img, P=n_points, R=radius, method=method)
    hist, _ = np.histogram(lbp_computed, bins=26, range=(0, 26))
    hist_normalized = hist / (hist.sum() + 1e-7)
    return hist_normalized

def extract_edge_density_features(edge_map: np.ndarray) -> np.ndarray:
    height, width = edge_map.shape
    grid_size = 4
    cell_h = height // grid_size
    cell_w = width // grid_size
    edge_density_features = []
    for i in range(grid_size):
        for j in range(grid_size):
            cell_roi = edge_map[i * cell_h : (i + 1) * cell_h, j * cell_w : (j + 1) * cell_w]
            density = cell_roi.sum() / (cell_roi.size + 1e-7)
            edge_density_features.append(density)
    return np.array(edge_density_features)

def extract_all_features(gray_img: np.ndarray, edge_map: np.ndarray) -> np.ndarray:
    lbp_features = extract_lbp_features(gray_img)
    edge_density_features = extract_edge_density_features(edge_map)
    return np.concatenate([lbp_features, edge_density_features])

def preprocess_image(img_path: str) -> Tuple[np.ndarray, np.ndarray]:
    img_path_obj = Path(img_path)
    if not img_path_obj.exists():
        raise FileNotFoundError(f"Image not found: {img_path}")
    img = cv2.imread(str(img_path))
    if img is None:
        raise ValueError(f"Cannot load image: {img_path}")
    img_resized = cv2.resize(img, (128, 128))
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    preprocessed = gray.astype(np.float32) / 255.0
    edge_map = edges.astype(np.float32) / 255.0
    return preprocessed, edge_map

# ============================================================================

def load_model_and_scaler(model_name: str) -> Tuple[Any, Any]:
    model_name = model_name.lower()
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(f"Model '{model_name}' not supported. Choose from {SUPPORTED_MODELS}")
    model_path = MODELS_DIR / f"{model_name}.pkl"
    scaler_path = MODELS_DIR / "scaler.pkl"
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not scaler_path.exists():
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def extract_batch_features(image_dir: str, verbose: bool = False) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    image_dir_obj = Path(image_dir)
    if not image_dir_obj.exists():
        raise FileNotFoundError(f"Directory not found: {image_dir}")
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = [f for f in image_dir_obj.rglob('*') if f.suffix.lower() in image_extensions]
    if not image_files:
        raise ValueError(f"No images found in: {image_dir}")
    if verbose:
        print("\n" + "="*70)
        print("🔍 FEATURE EXTRACTION — Batch Processing")
        print("="*70)
        print(f"📁 Directory : {image_dir}")
        print(f"📊 Images found : {len(image_files)}")
        print("-"*70)
    all_features, all_labels, all_image_paths = [], [], []
    for idx, img_path in enumerate(sorted(image_files)):
        try:
            parent_folder = img_path.parent.name.lower()
            if 'normal' in parent_folder:
                label = 0
            elif 'defect' in parent_folder:
                label = 1
            else:
                if verbose:
                    print(f"   ⚠️  Skipping {img_path.name}: unclear label")
                continue
            gray_img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if gray_img is None:
                if verbose:
                    print(f"   ⚠️  Skipping {img_path.name}: cannot load")
                continue
            gray_img = gray_img.astype(np.float32) / 255.0
            if gray_img.shape != (128, 128):
                gray_img = cv2.resize(gray_img, (128, 128))
            gray_uint8 = (gray_img * 255).astype(np.uint8)
            edges = cv2.Canny(gray_uint8, 50, 150)
            edge_map = edges.astype(np.float32) / 255.0
            features = extract_all_features(gray_img, edge_map)
            all_features.append(features)
            all_labels.append(label)
            all_image_paths.append(str(img_path))
            if verbose and (idx + 1) % 10 == 0:
                print(f"   ✅ Processed {idx + 1}/{len(image_files)} images")
        except Exception as e:
            if verbose:
                print(f"   ❌ Error processing {img_path.name}: {e}")
            continue
    if not all_features:
        raise ValueError(f"No features extracted from: {image_dir}")
    return np.stack(all_features, axis=0), np.array(all_labels), all_image_paths

# ============================================================================

def evaluate_model(model: Any, scaler: Any, features: np.ndarray, true_labels: np.ndarray, model_name: str = "Unknown", verbose: bool = True) -> Dict[str, Any]:
    if verbose:
        print("\n" + "="*70)
        print(f"📊 EVALUATING MODEL: {model_name.upper()}")
        print("="*70)
    features_scaled = scaler.transform(features)
    predictions = model.predict(features_scaled)
    accuracy = accuracy_score(true_labels, predictions)
    precision = precision_score(true_labels, predictions, zero_division=0)
    recall = recall_score(true_labels, predictions, zero_division=0)
    f1 = f1_score(true_labels, predictions, zero_division=0)
    conf_matrix = confusion_matrix(true_labels, predictions)
    roc_auc, fpr, tpr = None, None, None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(features_scaled)[:,1]
            roc_auc = roc_auc_score(true_labels, proba)
            fpr, tpr, _ = roc_curve(true_labels, proba)
        except:
            pass
    if verbose:
        print("\n📈 PERFORMANCE METRICS:")
        print(f"   ✓ Accuracy  : {accuracy:.4f}")
        print(f"   ✓ Precision : {precision:.4f}")
        print(f"   ✓ Recall    : {recall:.4f}")
        print(f"   ✓ F1-Score  : {f1:.4f}")
        if roc_auc: print(f"   ✓ ROC-AUC   : {roc_auc:.4f}")
        print("\n📊 CONFUSION MATRIX:")
        print(f"   ┌───────────────┐")
        print(f"   │ TN: {conf_matrix[0,0]:4d} │ FP: {conf_matrix[0,1]:4d} │")
        print(f"   │ FN: {conf_matrix[1,0]:4d} │ TP: {conf_matrix[1,1]:4d} │")
        print(f"   └───────────────┘")
        print("\n📋 PER-CLASS METRICS:")
        class_report = classification_report(true_labels, predictions, zero_division=0)
        print(class_report)
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "conf_matrix": conf_matrix,
        "class_report": class_report
    }

# ============================================================================

def compare_all_models(features: np.ndarray, labels: np.ndarray, verbose: bool = True) -> Dict[str, Dict[str, Any]]:
    results = {}
    for model_name in SUPPORTED_MODELS:
        try:
            model, scaler = load_model_and_scaler(model_name)
            res = evaluate_model(model, scaler, features, labels, model_name=model_name, verbose=verbose)
            results[model_name] = res
        except Exception as e:
            if verbose:
                print(f"❌ Error evaluating {model_name}: {e}")
            results[model_name] = {}
    return results

# ============================================================================

def save_evaluation_report(
    results: Dict[str, Dict],
    output_path: str = "evaluation_report.csv"
) -> None:
    """
    Save evaluation results to CSV.
    Works for single-model or multi-model results.
    """
    rows = []

    # If results is a single model dict (has 'accuracy' key)
    if isinstance(results, dict) and 'accuracy' in results:
        rows.append({
            "Model": "Model",
            "Accuracy": results.get('accuracy', None),
            "Precision": results.get('precision', None),
            "Recall": results.get('recall', None),
            "F1-Score": results.get('f1', None),
            "ROC-AUC": results.get('roc_auc', None),
        })
    else:
        # Multi-model results
        for model_name, res in results.items():
            if not res:
                continue
            rows.append({
                "Model": model_name,
                "Accuracy": res.get('accuracy', None),
                "Precision": res.get('precision', None),
                "Recall": res.get('recall', None),
                "F1-Score": res.get('f1', None),
                "ROC-AUC": res.get('roc_auc', None),
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"✅ Report saved to: {output_path}")

# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Evaluate VisionInspect AI models")
    parser.add_argument("image_dir", type=str, help="Directory containing test images")
    parser.add_argument("--all", action="store_true", help="Evaluate all models")
    parser.add_argument("--save-report", action="store_true", help="Save results to CSV")
    parser.add_argument("--verbose", action="store_true", help="Print verbose logs")
    args = parser.parse_args()

    features, labels, image_paths = extract_batch_features(args.image_dir, verbose=args.verbose)
    if args.verbose:
        print(f"\n✅ Extracted features from {len(features)} images")
        print(f"📊 Feature array shape : {features.shape}")
        print(f"📊 Label array shape   : {labels.shape}")

    results = {}
    if args.all:
        results = compare_all_models(features, labels, verbose=args.verbose)
    else:
        model, scaler = load_model_and_scaler("rf")
        results["rf"] = evaluate_model(model, scaler, features, labels, model_name="rf", verbose=args.verbose)

    if args.save_report:
        save_evaluation_report(results)

# ============================================================================

if __name__ == "__main__":
    main()