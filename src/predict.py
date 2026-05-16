# # src/predict.py
# import joblib
# import numpy as np
# from src.preprocessing import preprocess_image
# from src.feature_extraction import extract_all_features

# def predict_image(img_path: str, model_name: str = "svm"):
#     """
#     Single-image prediction pipeline.
    
#     Args:
#         img_path: Path to image to predict
#         model_name: Which model to use ("svm", "knn", "rf")
        
#     Returns:
#         label: "NORMAL" or "DEFECTIVE"
#         confidence: 0.0 to 1.0
#     """
    
#     # Step 1: Preprocess
#     preprocessed, edge_map = preprocess_image(img_path)
    
#     # Step 2: Extract features (Faiqa's function)
#     features = extract_all_features(preprocessed, edge_map)
    
#     # Step 3: Scale features
#     scaler = joblib.load(f"models/scaler.pkl")
#     features_scaled = scaler.transform([features])
    
#     # Step 4: Load model & predict
#     model = joblib.load(f"models/{model_name}_model.pkl")
#     prediction = model.predict(features_scaled)[0]
#     confidence = model.predict_proba(features_scaled)[0].max()
    
#     label = "DEFECTIVE" if prediction == 1 else "NORMAL"
    
#     return label, confidence