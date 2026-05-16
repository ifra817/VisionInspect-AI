"""
OpenCV-based preprocessing pipeline for smartphone screen images.

Pipeline:
1. Load image (BGR format from OpenCV)
2. Resize to 128×128 (standardize input)
3. Convert to grayscale (crack edges are clear in grayscale)
4. Gaussian Blur (remove sensor noise)
5. Canny Edge Detection (highlight cracks as white lines)
6. Normalize to [0, 1] (ML models expect normalized input)

Returns both the preprocessed image and edge map for visualization.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, List


# ============================================================================
# CORE PREPROCESSING FUNCTIONS
# ============================================================================

def preprocess_image(img_path: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load and preprocess a single image.
    
    Args:
        img_path (str): Path to the image file
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: 
            - preprocessed_img: 128×128 grayscale image, normalized to [0, 1]
            - edge_map: Canny edge detection result, normalized to [0, 1]
            
    Raises:
        FileNotFoundError: If image doesn't exist
        ValueError: If image can't be loaded or is corrupted
    """
    
    # ✅ Step 1: Load image
    img_path_obj = Path(img_path)
    if not img_path_obj.exists():
        raise FileNotFoundError(f"Image not found: {img_path}")
    
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Cannot load image (corrupted?): {img_path}")
    
    # ✅ Step 2: Resize to standardize input
    # All images → 128×128 (good balance: detail vs computation time)
    img_resized = cv2.resize(img, (128, 128), interpolation=cv2.INTER_LINEAR)
    
    # ✅ Step 3: Convert BGR → Grayscale
    # Crack detection is easier in grayscale (intensity-based edges)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    
    # ✅ Step 4: Gaussian Blur
    # Reduces sensor noise while preserving edges
    # (5, 5) kernel: good balance between noise removal and detail preservation
    # sigma=0: OpenCV calculates from kernel size
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # ✅ Step 5: Canny Edge Detection
    # Highlights cracks as white lines (255) on black background (0)
    # threshold1=50: lower threshold (edges weaker than this are ignored)
    # threshold2=150: upper threshold (edges stronger than this are definitely edges)
    # Use Canny ratio of 1:3 for better edge linking
    edges = cv2.Canny(blurred, 50, 150)
    
    # ✅ Step 6: Normalize to [0, 1]
    # ML models expect normalized input for faster training & convergence
    preprocessed = gray.astype(np.float32) / 255.0
    edge_map = edges.astype(np.float32) / 255.0
    
    return preprocessed, edge_map


def preprocess_batch(image_dir: str, verbose: bool = True) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Preprocess all images in a directory.
    
    Args:
        image_dir (str): Path to directory containing images
        verbose (bool): Print progress to console
        
    Returns:
        Tuple[np.ndarray, np.ndarray, List[str]]:
            - images: Array of shape (N, 128, 128) - preprocessed images
            - edges: Array of shape (N, 128, 128) - edge maps
            - image_paths: List of image file paths (for reference)
            
    Raises:
        FileNotFoundError: If directory doesn't exist
        ValueError: If no images found in directory
    """
    
    image_dir_obj = Path(image_dir)
    if not image_dir_obj.exists():
        raise FileNotFoundError(f"Directory not found: {image_dir}")
    
    # Find all image files (case-insensitive)
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    image_files = [
        f for f in image_dir_obj.rglob('*')
        if f.suffix.lower() in image_extensions
    ]
    
    if not image_files:
        raise ValueError(f"No images found in: {image_dir}")
    
    if verbose:
        print(f"\n📂 Processing {len(image_files)} images from: {image_dir}")
    
    # Process each image
    preprocessed_images = []
    edge_maps = []
    image_paths: List[str] = []
    
    for idx, img_path in enumerate(sorted(image_files)):
        try:
            preprocessed, edge_map = preprocess_image(str(img_path))
            preprocessed_images.append(preprocessed)
            edge_maps.append(edge_map)
            image_paths.append(str(img_path))
            
            if verbose and (idx + 1) % 10 == 0:
                print(f"   ✅ Processed {idx + 1}/{len(image_files)}")
                
        except Exception as e:
            print(f"   ⚠️  Skipping {img_path.name}: {str(e)}")
            continue
    
    if not preprocessed_images:
        raise ValueError(f"Failed to process any images from: {image_dir}")
    
    # Convert lists to numpy arrays
    images = np.stack(preprocessed_images, axis=0)  # Shape: (N, 128, 128)
    edges = np.stack(edge_maps, axis=0)              # Shape: (N, 128, 128)
    
    if verbose:
        print(f"   ✅ Successfully processed {len(preprocessed_images)} images")
        print(f"   📊 Shape: {images.shape}")
    
    return images, edges, image_paths


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def show_preprocessing_steps(img_path: str) -> None:
    """
    Display the preprocessing pipeline visually (for debugging).
    
    This function shows: Original → Grayscale → Blurred → Edges → Normalized
    
    Args:
        img_path (str): Path to image file
    """
    import matplotlib.pyplot as plt
    
    # Load original
    original = cv2.imread(img_path)
    if original is None:
        raise ValueError(f"Cannot load image: {img_path}")
    
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    
    # Resize
    resized = cv2.resize(original, (128, 128))
    resized_rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    
    # Grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    
    # Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Edges
    edges = cv2.Canny(blurred, 50, 150)
    
    # Normalized
    normalized = gray.astype(np.float32) / 255.0
    
    # Display
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("Preprocessing Pipeline", fontsize=16, fontweight='bold')
    
    axes[0, 0].imshow(original_rgb)
    axes[0, 0].set_title("1. Original (Color)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(resized_rgb)
    axes[0, 1].set_title("2. Resized (128×128)")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(gray, cmap='gray')
    axes[0, 2].set_title("3. Grayscale")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(blurred, cmap='gray')
    axes[1, 0].set_title("4. Gaussian Blur")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(edges, cmap='gray')
    axes[1, 1].set_title("5. Canny Edges")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(normalized, cmap='gray')
    axes[1, 2].set_title("6. Normalized [0, 1]")
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    """
    Quick test: Run this file directly to test preprocessing on sample images.
    
    Usage:
        python src/preprocessing.py
    """
    
    print("=" * 70)
    print("🔍 PREPROCESSING PIPELINE - TEST RUN")
    print("=" * 70)
    
    # Test on first 3 images from each class
    data_dir = Path("data/train")
    
    for class_name in ["normal", "defective"]:
        class_dir = data_dir / class_name
        
        if not class_dir.exists():
            print(f"\n⚠️  {class_dir} not found. Did you run split_dataset.py?")
            continue
        
        print(f"\n📂 Testing {class_name.upper()} class...")
        
        try:
            images, edges, paths = preprocess_batch(str(class_dir), verbose=True)
            
            # Show stats
            print(f"   ✅ Preprocessed images shape: {images.shape}")
            print(f"   ✅ Edge maps shape: {edges.shape}")
            print(f"   ✅ Min intensity: {images.min():.3f}, Max: {images.max():.3f}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Preprocessing test complete!")
    print("=" * 70)
