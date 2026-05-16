"""
PREDICTION MODULE FOR VISIONINSPECT AI
FILE PURPOSE:
This module handles the inference pipeline. It takes an input image,
runs it through preprocessing and feature extraction, and uses a trained 
ML model to predict whether the smartphone component is normal or defective.

USAGE:
    # From terminal (Run as a module)
    python -m src.predict path/to/image.jpg --model rf

    # As an imported module
    from src.predict import predict_image
    result = predict_image("path/to/image.jpg", model_name="svm")
================================================================================
"""

import os
import argparse
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, Union, Tuple, Any, Optional

# Import local pipeline modules
from src.preprocessing import preprocess_image
from src.feature_extraction import extract_all_features

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

MODELS_DIR = Path("models")
CLASS_NAMES = {0: "NORMAL", 1: "DEFECTIVE"}
SUPPORTED_MODELS = ["knn", "svm", "rf"]

# ============================================================================
# CORE PREDICTION FUNCTIONS
# ============================================================================

def load_inference_pipeline(model_name: str) -> Tuple[Any, Any]:
    """
    Load the trained model and the feature scaler.
    
    Args:
        model_name (str): Name of the model to load ('knn', 'svm', 'rf')
        
    Returns:
        Tuple: (trained_model, fitted_scaler)
        
    Raises:
        FileNotFoundError: If the model or scaler file is missing.
    """
    model_name = model_name.lower()
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(f"Model '{model_name}' not supported. Choose from {SUPPORTED_MODELS}")

    model_path = MODELS_DIR / f"{model_name}.pkl"
    scaler_path = MODELS_DIR / "scaler.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}. Did you train it?")
    if not scaler_path.exists():
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}. Did you save it during training?")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    return model, scaler

def predict_image(img_path: str, model_name: str = "rf", verbose: bool = False) -> Dict[str, Union[str, float, int, None]]:
    """
    Run the full inference pipeline on a single image.
    
    Args:
        img_path (str): Path to the target image.
        model_name (str): The classifier to use ('knn', 'svm', 'rf').
        verbose (bool): Whether to print step-by-step progress.
        
    Returns:
        Dict containing prediction details (label, class name, confidence).
    """
    if verbose:
        print(f"\n🔍 Analyzing Image: {Path(img_path).name}")
        print("-" * 50)

    # 1. Load Model & Scaler
    model, scaler = load_inference_pipeline(model_name)
    if verbose:
        print(f"✅ Loaded model: {model_name.upper()} and Scaler")

    # 2. Preprocess Image
    preprocessed_img, edge_map = preprocess_image(img_path)
    if verbose:
        print("✅ Preprocessing complete (128x128 Grayscale + Canny Edge Map)")

    # 3. Extract Features
    features = extract_all_features(preprocessed_img, edge_map)
    if verbose:
        print(f"✅ Extracted {len(features)} handcrafted features")

    # 4. Scale Features
    # Reshape to 2D array (1 sample, 42 features) as expected by scikit-learn
    features_2d = features.reshape(1, -1)
    features_scaled = scaler.transform(features_2d)

    # 5. Predict
    prediction = int(model.predict(features_scaled)[0])
    class_name = CLASS_NAMES[prediction]

    # Try to get prediction probability (confidence) if the model supports it
    confidence: Optional[float] = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features_scaled)[0]
        confidence = float(np.max(probabilities) * 100)
    
    if verbose:
        print("-" * 50)
        print(f"🎯 PREDICTION : {class_name}")
        if confidence is not None:
            print(f"📊 CONFIDENCE : {confidence:.2f}%")
        print("-" * 50 + "\n")

    return {
        "file": Path(img_path).name,
        "prediction_code": prediction,
        "class_name": class_name,
        "confidence": confidence,
        "model_used": model_name.upper()
    }


# ============================================================================
# CLI IMPLEMENTATION
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VisionInspect AI - Defect Prediction CLI")
    
    parser.add_argument(
        "image", 
        type=str, 
        help="Path to the image you want to inspect."
    )
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="rf", 
        choices=SUPPORTED_MODELS,
        help="Machine learning model to use (default: rf)."
    )
    
    parser.add_argument(
        "--quiet", 
        action="store_true", 
        help="Suppress detailed print logs."
    )

    args = parser.parse_args()

    try:
        result = predict_image(
            img_path=args.image, 
            model_name=args.model, 
            verbose=not args.quiet
        )
        
        # If running in quiet mode, just output the final dict
        if args.quiet:
            print(f"{result['class_name']}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")