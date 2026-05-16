# File: download_dataset.py
import kagglehub
import os
from pathlib import Path

def download_dataset():
    """Download Kaggle dataset using kagglehub"""
    
    print("📥 Downloading Cracked & Intact Smartphone Images Dataset...")
    
    # Download using kagglehub (uses ~/.kaggle/kaggle.json automatically)
    path = kagglehub.dataset_download("axondata/cracked-and-intact-smartphone-images-dataset")
    
    print(f"✅ Downloaded to: {path}")
    
    # Create symbolic link or copy to data/raw/ for easier access
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    
    # List downloaded files
    print("\n📂 Dataset contents:")
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:3]:  # Show first 3 files per folder
            print(f"{subindent}{file}")
    
    return path

if __name__ == "__main__":
    dataset_path = download_dataset()
    print(f"\n✅ Use this path in data_split.py: {dataset_path}")