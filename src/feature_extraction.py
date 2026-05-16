"""
FEATURE EXTRACTION MODULE FOR VISIONINSPECT AI
FILE PURPOSE:
This module extracts handcrafted features from preprocessed images.
It combines two feature types:
  1. Local Binary Patterns (LBP) - 26 features (texture descriptor)
  2. Edge Density              - 16 features (spatial distribution)
  Total: 42-dimensional feature vector

USAGE:
  # Single image
  from src.feature_extraction import extract_all_features
  features = extract_all_features(gray_img, edge_map)

  # Batch processing
  from src.feature_extraction import extract_batch_features
  features, labels, paths = extract_batch_features("data/train")
================================================================================
"""

import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, List
import os
from skimage.feature import local_binary_pattern
import warnings
warnings.filterwarnings('ignore')

# SECTION 1: LBP FEATURES — TEXTURE DESCRIPTOR
def extract_lbp_features(gray_img: np.ndarray) -> np.ndarray:
    """
    Extract Local Binary Pattern (LBP) features from a grayscale image.
    LBP compares each pixel with its 8 neighbors, creating a binary code.
    The histogram of these codes is the feature vector (texture fingerprint).
    WHY LBP FOR CRACK DETECTION?
    - Cracks have unique irregular texture patterns
    - LBP captures these local intensity changes efficiently
    PARAMETERS:
        gray_img: Grayscale image, shape (128, 128), values in [0, 1]
    RETURNS:
        np.ndarray: Normalized LBP histogram, shape (26,)
    """
    radius   = 3          # Sampling circle radius (pixels)
    n_points = 8 * radius # 24 neighbor points on the circle
    method   = 'uniform'  # Only smooth/uniform patterns counted

    # Compute LBP image — each pixel gets a code 0-25 (uniform) or 26 (non-uniform)
    lbp_computed = local_binary_pattern(gray_img, P=n_points, R=radius, method=method)

    # Build normalized histogram of LBP codes
    hist, _ = np.histogram(lbp_computed, bins=26, range=(0, 26))
    hist_normalized = hist / (hist.sum() + 1e-7)   # +1e-7 avoids divide-by-zero

    return hist_normalized   # shape: (26,)


# SECTION 2: EDGE DENSITY FEATURES — SPATIAL DISTRIBUTION
def extract_edge_density_features(edge_map: np.ndarray) -> np.ndarray:
    """
    Extract edge density from a 4×4 spatial grid of the edge map.
    Divides the 128×128 edge map into 16 cells (32×32 each) and computes
    the fraction of edge pixels in each cell.
    WHY EDGE DENSITY?
    - Cracked screens have high edge density in crack regions
    - Normal screens have low, uniform edge density
    - Spatial layout helps distinguish crack patterns from noise
    PARAMETERS:
        edge_map: Binary edge map, shape (128, 128), values in {0, 1}
    RETURNS:
        np.ndarray: 16 edge density values, shape (16,)
    """
    height, width = edge_map.shape   # (128, 128)
    grid_size     = 4                # 4×4 = 16 cells
    cell_h        = height // grid_size   # 32
    cell_w        = width  // grid_size   # 32

    edge_density_features = []

    for i in range(grid_size):
        for j in range(grid_size):
            # Slice the cell from the edge map
            cell_roi = edge_map[
                i * cell_h : (i + 1) * cell_h,
                j * cell_w : (j + 1) * cell_w
            ]  # shape: (32, 32)

            # Edge density = fraction of pixels that are edges
            density = cell_roi.sum() / (cell_roi.size + 1e-7)
            edge_density_features.append(density)

    return np.array(edge_density_features)   # shape: (16,)


# SECTION 3: COMBINED FEATURE VECTOR — 42 DIMENSIONS
def extract_all_features(gray_img: np.ndarray, edge_map: np.ndarray) -> np.ndarray:
    """
    Combine LBP and edge density into a single 42-dimensional feature vector.
    Vector layout:
        indices  0-25  → LBP features      (26 values)
        indices 26-41  → Edge density grid  (16 values)
    WHY COMBINE?
    - LBP  captures WHAT a crack looks like (texture)
    - Edge density captures WHERE it is (spatial location)
    - Together they give complementary, richer information
    PARAMETERS:
        gray_img : Grayscale image, shape (128, 128), values in [0, 1]
        edge_map : Edge detection result, shape (128, 128), values in [0, 1]
    RETURNS:
        np.ndarray: 42-dimensional feature vector, shape (42,)
    """
    lbp_features          = extract_lbp_features(gray_img)          # (26,)
    edge_density_features = extract_edge_density_features(edge_map)  # (16,)

    combined_features = np.concatenate([lbp_features, edge_density_features])
    # shape: (26 + 16,) = (42,)

    return combined_features


# SECTION 4: BATCH PROCESSING — ENTIRE DATASET
def extract_batch_features(
    image_dir: str,
    verbose: bool = True
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Extract features from ALL images in a directory.
    EXPECTED FOLDER STRUCTURE:
        image_dir/
            normal/      ← images with label 0
            defective/   ← images with label 1
    PARAMETERS:
        image_dir : Path to directory containing normal/ and defective/ subfolders
        verbose   : Print progress messages (default True)
    RETURNS:
        features    : np.ndarray, shape (N, 42)
        labels      : np.ndarray, shape (N,)  — 0=normal, 1=defective
        image_paths : List[str], file paths for reference
    RAISES:
        FileNotFoundError : if image_dir does not exist
        ValueError        : if no images found
    """
    image_dir_obj = Path(image_dir)

    if not image_dir_obj.exists():
        raise FileNotFoundError(f"Directory not found: {image_dir}")

    # Collect all image files recursively
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = [
        f for f in image_dir_obj.rglob('*')
        if f.suffix.lower() in image_extensions
    ]

    if not image_files:
        raise ValueError(f"No images found in: {image_dir}")

    if verbose:
        print("\n" + "=" * 70)
        print("🔍 FEATURE EXTRACTION — Batch Processing")
        print("=" * 70)
        print(f"📁 Directory : {image_dir}")
        print(f"📊 Images found : {len(image_files)}")
        print("-" * 70)

    all_features    = []
    all_labels      = []
    all_image_paths = []

    for idx, img_path in enumerate(sorted(image_files)):   # ← BUG 4 FIXED
        try:
            # ── Label from folder name ──────────────────────────────────────
            parent_folder = img_path.parent.name.lower()

            if 'normal' in parent_folder:
                label = 0
            elif 'defect' in parent_folder:
                label = 1
            else:
                if verbose:
                    print(f"   ⚠️  Skipping {img_path.name}: unclear label (folder='{parent_folder}')")
                continue

            # ── Load grayscale image ────────────────────────────────────────
            gray_img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if gray_img is None:
                if verbose:
                    print(f"   ⚠️  Skipping {img_path.name}: cannot load (corrupted?)")
                continue

            # Normalize to [0, 1] float32
            gray_img = gray_img.astype(np.float32) / 255.0

            # Resize to 128×128 if needed
            if gray_img.shape != (128, 128):
                gray_img = cv2.resize(gray_img, (128, 128))

            # ── Compute edge map ────────────────────────────────────────────
            gray_uint8 = (gray_img * 255).astype(np.uint8)
            edges      = cv2.Canny(gray_uint8, 50, 150)
            edge_map   = edges.astype(np.float32) / 255.0

            # ── Extract 42D feature vector ──────────────────────────────────
            features = extract_all_features(gray_img, edge_map)

            # ── Store results ───────────────────────────────────────────────
            all_features.append(features)
            all_labels.append(label)                      # ← BUG 5 FIXED
            all_image_paths.append(str(img_path))

            if verbose and (idx + 1) % 10 == 0:
                print(f"   ✅ Processed {idx + 1}/{len(image_files)} images")

        except Exception as e:
            print(f"   ❌ Error processing {img_path.name}: {e}")
            continue

    if not all_features:
        raise ValueError(f"No features extracted from: {image_dir}")

    features_array = np.stack(all_features, axis=0)   # (N, 42)
    labels_array   = np.array(all_labels)             # (N,)

    if verbose:
        print("-" * 70)
        print(f"✅ Extracted features from {len(all_features)} images")
        print(f"📊 Feature array shape : {features_array.shape}")
        print(f"📊 Label array shape   : {labels_array.shape}")
        print(f"📈 Class distribution:")
        unique, counts = np.unique(labels_array, return_counts=True)
        for cls, cnt in zip(unique, counts):
            name = "Normal" if cls == 0 else "Defective"
            pct  = cnt / len(labels_array) * 100
            print(f"   - {name}: {cnt} images ({pct:.1f}%)")
        print("=" * 70 + "\n")

    return features_array, labels_array, all_image_paths


# SECTION 5: SAVE TO CSV
def save_features_to_csv(
    features: np.ndarray,
    labels: np.ndarray,
    output_path: str = "features.csv"
) -> None:
    """
    Save feature array + labels to a CSV file.
    CSV columns: feature_0, feature_1, ..., feature_41, label
    PARAMETERS:
        features    : shape (N, 42)
        labels      : shape (N,)
        output_path : destination file path
    """
    data_dict = {f"feature_{i}": features[:, i] for i in range(features.shape[1])}
    data_dict["label"] = labels

    df = pd.DataFrame(data_dict)
    df.to_csv(output_path, index=False)

    print(f"✅ Saved to : {output_path}")
    print(f"   Rows: {len(df)} | Columns: {len(df.columns)}")
    print(f"   File size: {os.path.getsize(output_path) / 1024:.1f} KB")


# SECTION 6: VISUALIZATION HELPER
def visualize_features_for_image(img_path: str, save_path: str = None) -> None:
    """
    Show grayscale image, edge map, LBP histogram, and edge density grid.
    PARAMETERS:
        img_path  : path to image file
        save_path : optional path to save the figure
    """
    try:
        import matplotlib.pyplot as plt

        gray_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if gray_img is None:
            print(f"❌ Cannot load: {img_path}")
            return

        gray_img   = gray_img.astype(np.float32) / 255.0
        gray_img   = cv2.resize(gray_img, (128, 128))
        gray_uint8 = (gray_img * 255).astype(np.uint8)
        edges      = cv2.Canny(gray_uint8, 50, 150)
        edge_map   = edges.astype(np.float32) / 255.0

        features      = extract_all_features(gray_img, edge_map)
        lbp_features  = features[:26]
        edge_features = features[26:]

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f"Feature Visualization: {Path(img_path).name}", fontsize=14, fontweight='bold')

        axes[0, 0].imshow(gray_img, cmap='gray')
        axes[0, 0].set_title("Grayscale Image")
        axes[0, 0].axis('off')

        axes[0, 1].imshow(edge_map, cmap='gray')
        axes[0, 1].set_title("Edge Map (Canny)")
        axes[0, 1].axis('off')

        axes[1, 0].bar(range(26), lbp_features, color='steelblue')
        axes[1, 0].set_title("LBP Features (26 bins)")
        axes[1, 0].set_xlabel("Bin")
        axes[1, 0].set_ylabel("Frequency")

        im = axes[1, 1].imshow(edge_features.reshape(4, 4), cmap='hot')
        axes[1, 1].set_title("Edge Density (4×4 Grid)")
        axes[1, 1].set_xlabel("Column")
        axes[1, 1].set_ylabel("Row")
        plt.colorbar(im, ax=axes[1, 1])

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"✅ Visualization saved to: {save_path}")
        else:
            plt.show()

        print(f"\n📊 Stats for {Path(img_path).name}:")
        print(f"   LBP (first 5)      : {lbp_features[:5]}")
        print(f"   Edge density range : [{edge_features.min():.3f}, {edge_features.max():.3f}]")
        print(f"   Mean edge density  : {edge_features.mean():.3f}")

    except Exception as e:
        print(f"❌ Visualization error: {e}")


# SECTION 7: MAIN — RUN DIRECTLY
if __name__ == "__main__":    # ← BUG 2 & 3 FIXED (double underscores, only once)
    """
    Run this script directly to extract features from all data splits:
        python src/feature_extraction.py
    """
    print("\n🎯 VISIONINSPECT AI — FEATURE EXTRACTION")
    print("=" * 70)

    data_splits = ["train", "val", "test"]

    for split in data_splits:
        image_dir   = f"data/{split}"
        output_file = f"features_{split}.csv"

        if not Path(image_dir).exists():
            print(f"⚠️  Skipping '{split}': directory not found ({image_dir})")
            continue

        print(f"\n{'='*70}")
        print(f"Processing {split.upper()} split...")
        print(f"{'='*70}")

        try:
            features, labels, paths = extract_batch_features(
                image_dir=image_dir,
                verbose=True
            )
            save_features_to_csv(
                features=features,
                labels=labels,
                output_path=output_file
            )
            print(f"✅ {split.upper()} done!\n")

        except Exception as e:
            print(f"❌ Error on {split}: {e}\n")

    print("✅ All splits done! Feature extraction complete.")