# test_viz.py
from src.preprocessing import show_preprocessing_steps

# Pick one normal and one defective image
show_preprocessing_steps("data/train/normal/13.png")
show_preprocessing_steps("data/train/defective/IMG_5407.PNG")