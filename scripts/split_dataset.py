"""
Dataset splitting script - organize images into train/val/test folders
Usage: python scripts/split_dataset.py

Expected structure from Kaggle:
├── Image_phones/          (normal class)
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
└── Image_brokenphones/    (defective class)
    ├── broken1.jpg
    ├── broken2.jpg
    └── ...
"""

import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

# ==================== CONFIGURATION ====================
DATA_ROOT = Path(__file__).parent.parent / "data"
TRAIN_SPLIT = 0.70
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
RANDOM_SEED = 42

# ==================== SETUP ====================
random.seed(RANDOM_SEED)

# Class mapping: source folder → output class name
CLASS_MAPPING = {
    "Image_phones": "normal",
    "Image_brokenphones": "defective"
}

def find_dataset_path():
    """Find dataset path from kagglehub cache or manual location"""
    
    # Option 1: Check kagglehub cache
    kagglehub_cache = Path.home() / ".cache" / "kagglehub" / "datasets" / "axondata" / \
                      "cracked-and-intact-smartphone-images-dataset" / "versions" / "1"
    
    if kagglehub_cache.exists():
        print(f"✅ Found dataset in kagglehub cache:")
        print(f"   {kagglehub_cache}\n")
        return kagglehub_cache
    
    # Option 2: Check data/raw
    data_raw = DATA_ROOT / "raw"
    if data_raw.exists() and any(data_raw.iterdir()):
        print(f"✅ Found dataset in data/raw\n")
        return data_raw
    
    raise FileNotFoundError(
        "❌ Dataset not found!\n"
        "Options:\n"
        "1. Run: python scripts/download_dataset.py\n"
        "2. Or manually extract Kaggle zip to data/raw/\n"
    )

def create_output_directories():
    """Create train/val/test directory structure"""
    
    print("📁 Creating output directories...")
    
    for split in ["train", "val", "test"]:
        for cls in ["normal", "defective"]:
            dir_path = DATA_ROOT / split / cls
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {dir_path}")
    
    print()

def get_images_by_class(source_path):
    """Load images from source folders (Image_phones, Image_brokenphones)"""
    
    source_path = Path(source_path)
    images_by_class = {"normal": [], "defective": []}
    
    print(f"🔍 Scanning dataset at: {source_path}\n")
    
    for source_folder, class_name in CLASS_MAPPING.items():
        folder_path = source_path / source_folder
        
        if not folder_path.exists():
            raise FileNotFoundError(f"❌ Folder not found: {folder_path}")
        
        # Find all image files (case-insensitive)
        images = []
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
            images.extend(folder_path.glob(ext))
        
        if not images:
            raise ValueError(f"❌ No images found in {folder_path}")
        
        images_by_class[class_name] = images
        print(f"   ✅ {class_name.upper():10s}: {len(images):4d} images from {source_folder}/")
    
    print()
    return images_by_class

def split_dataset(images_by_class):
    """Split images into train/val/test and copy to respective folders"""
    
    print("=" * 70)
    print("SPLITTING DATASET (70% train / 15% val / 15% test)")
    print("=" * 70 + "\n")
    
    split_stats = defaultdict(lambda: {"normal": 0, "defective": 0})
    
    for class_name, images in images_by_class.items():
        if not images:
            continue
        
        random.shuffle(images)
        
        total = len(images)
        train_count = int(total * TRAIN_SPLIT)
        val_count = int(total * VAL_SPLIT)
        
        train_images = images[:train_count]
        val_images = images[train_count:train_count + val_count]
        test_images = images[train_count + val_count:]
        
        print(f"📂 Splitting {class_name.upper()} ({total} images)...")
        
        splits_data = {"train": train_images, "val": val_images, "test": test_images}
        
        for split_name, split_images in splits_data.items():
            dest_dir = DATA_ROOT / split_name / class_name
            
            for img_path in split_images:
                try:
                    dest_path = dest_dir / img_path.name
                    shutil.copy2(str(img_path), str(dest_path))
                    split_stats[split_name][class_name] += 1
                except Exception as e:
                    print(f"   ❌ Error copying {img_path.name}: {e}")
        
        print(f"   ✅ train: {len(train_images)} | val: {len(val_images)} | test: {len(test_images)}\n")
    
    return split_stats

def print_statistics(split_stats):
    """Print detailed statistics"""
    
    print("\n" + "=" * 70)
    print("DATASET SPLIT STATISTICS")
    print("=" * 70)
    
    total_images = 0
    
    for split in ["train", "val", "test"]:
        normal = split_stats[split]["normal"]
        defective = split_stats[split]["defective"]
        total = normal + defective
        total_images += total
        
        normal_pct = (normal / total * 100) if total > 0 else 0
        defective_pct = (defective / total * 100) if total > 0 else 0
        
        print(f"\n{split.upper()}:")
        print(f"  Normal:    {normal:4d} ({normal_pct:5.1f}%)")
        print(f"  Defective: {defective:4d} ({defective_pct:5.1f}%)")
        print(f"  Total:     {total:4d}")
    
    print(f"\n{'=' * 70}")
    print(f"TOTAL IMAGES: {total_images}")
    print(f"{'=' * 70}\n")
    
    if total_images < 600:
        print("⚠️  WARNING: < 600 images total. Consider augmentation.\n")
    else:
        print("✅ Dataset size is excellent!\n")

def main():
    """Main execution"""
    
    print("\n" + "=" * 70)
    print("🚀 DATASET SPLITTING SCRIPT")
    print("=" * 70 + "\n")
    
    try:
        dataset_path = find_dataset_path()
        create_output_directories()
        images_by_class = get_images_by_class(dataset_path)
        split_stats = split_dataset(images_by_class)
        print_statistics(split_stats)
        
        print(f"✅ Dataset ready in: {DATA_ROOT}\n")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
