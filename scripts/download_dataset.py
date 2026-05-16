"""
Download Cracked & Intact Smartphone Images Dataset from Kaggle.

This script downloads the dataset using kagglehub (automatic caching).
Each team member needs their own Kaggle API credentials (one-time setup).

Setup Instructions:
1. Create Kaggle account: https://www.kaggle.com/
2. Go to Account Settings → API → "Create New API Token"
3. This downloads kaggle.json
4. Place kaggle.json at: ~/.kaggle/kaggle.json
   
   Windows:  C:\\Users\\[YourUsername]\\.kaggle\\kaggle.json
   Mac:      /Users/[YourUsername]/.kaggle/kaggle.json
   Linux:    /home/[YourUsername]/.kaggle/kaggle.json

5. Set permissions (Mac/Linux only):
   chmod 600 ~/.kaggle/kaggle.json

Then run: python scripts/download_dataset.py
"""

import kagglehub
import os
import sys
from pathlib import Path


def check_kaggle_credentials():
    """
    Verify that Kaggle API credentials exist.
    
    Returns:
        bool: True if credentials found, False otherwise
    """
    
    kaggle_json_path = Path.home() / ".kaggle" / "kaggle.json"
    
    if not kaggle_json_path.exists():
        print("\n" + "=" * 70)
        print("❌ ERROR: Kaggle API credentials not found!")
        print("=" * 70)
        print(f"\nExpected location: {kaggle_json_path}")
        print("\n📋 SETUP INSTRUCTIONS:")
        print("-" * 70)
        print("1. Go to https://www.kaggle.com/ and sign in")
        print("2. Click your profile → Settings → API")
        print("3. Click 'Create New API Token'")
        print("4. This downloads 'kaggle.json'")
        print("5. Move it to:")
        print(f"   {kaggle_json_path}")
        print("\n6. (Mac/Linux only) Set permissions:")
        print("   chmod 600 ~/.kaggle/kaggle.json")
        print("-" * 70)
        print("\n⏭️  After setup, run again: python scripts/download_dataset.py\n")
        print("=" * 70 + "\n")
        return False
    
    return True


def download_dataset():
    """
    Download Cracked & Intact Smartphone Images Dataset from Kaggle.
    
    Dataset: axondata/cracked-and-intact-smartphone-images-dataset
    
    Uses kagglehub for automatic caching:
    - First run: Downloads to ~/.cache/kagglehub/
    - Subsequent runs: Uses cached copy (instant)
    
    Returns:
        str: Path to downloaded dataset
    """
    
    print("\n" + "=" * 70)
    print("📥 DOWNLOADING CRACKED & INTACT SMARTPHONE IMAGES DATASET")
    print("=" * 70)
    
    # Check credentials first
    if not check_kaggle_credentials():
        sys.exit(1)
    
    try:
        print("\n⏳ Downloading dataset (this may take 1-2 minutes on first run)...")
        print("   (Subsequent runs use cached copy — instant!)\n")
        
        # Download using kagglehub (uses ~/.kaggle/kaggle.json automatically)
        dataset_path = kagglehub.dataset_download(
            "axondata/cracked-and-intact-smartphone-images-dataset"
        )
        
        print(f"✅ Dataset ready at: {dataset_path}\n")
        
        # List contents
        print("📂 Dataset structure:")
        print("-" * 70)
        
        for root, dirs, files in os.walk(dataset_path):
            level = root.replace(dataset_path, '').count(os.sep)
            indent = ' ' * 2 * level
            folder_name = os.path.basename(root) or "root"
            print(f"{indent}📁 {folder_name}/  ({len(files)} images)")
            
            if level < 2:  # Show file details for top 2 levels
                subindent = ' ' * 2 * (level + 1)
                for file in sorted(files)[:3]:  # Show first 3 files
                    print(f"{subindent}📄 {file}")
                if len(files) > 3:
                    print(f"{subindent}... and {len(files) - 3} more files")
        
        print("-" * 70)
        print("\n" + "=" * 70)
        print("✅ NEXT STEP: Run the dataset splitting script")
        print("=" * 70)
        print(f"\npython scripts/split_dataset.py\n")
        print("=" * 70 + "\n")
        
        return dataset_path
    
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERROR: Failed to download dataset")
        print("=" * 70)
        print(f"\nError details: {str(e)}")
        print("\nTroubleshooting:")
        print("1. ✅ Verify kaggle.json exists and is valid")
        print("2. ✅ Check internet connection")
        print("3. ✅ Try again in a few minutes")
        print("4. ✅ Visit https://www.kaggle.com/datasets/axondata/cracked-and-intact-smartphone-images-dataset")
        print("      (Manual download if script fails)")
        print("\n" + "=" * 70 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 VisionInspect AI - Dataset Download Script")
    print("=" * 70)
    
    dataset_path = download_dataset()
