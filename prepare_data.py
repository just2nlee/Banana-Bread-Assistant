"""
Data preparation script for BananaPredictor.
Organizes banana images and extracts day labels from filenames.
"""
import os
import re
from pathlib import Path
from typing import List, Tuple
import shutil

def extract_day_from_filename(filename: str) -> int:
    """Extract day number from filename like 'B1D5.jpeg' -> 5"""
    match = re.search(r'D(\d+)', filename)
    if match:
        return int(match.group(1))
    return None

def prepare_dataset(data_dir: str = ".", output_dir: str = "dataset") -> Tuple[List[str], List[int]]:
    """
    Prepare dataset from banana image folders.
    Returns: (image_paths, day_labels)
    """
    data_path = Path(data_dir)
    image_paths = []
    day_labels = []
    
    # Find all banana folders
    banana_folders = sorted([d for d in data_path.iterdir() 
                            if d.is_dir() and d.name.startswith("Banana_")])
    
    print(f"Found {len(banana_folders)} banana folders")
    
    for folder in banana_folders:
        # Get all images in this folder
        images = sorted([f for f in folder.iterdir() 
                        if f.suffix.lower() in ['.jpeg', '.jpg', '.png']])
        
        for img_path in images:
            day = extract_day_from_filename(img_path.name)
            if day is not None:
                image_paths.append(str(img_path))
                day_labels.append(day)
                print(f"  {img_path.name} -> Day {day}")
    
    print(f"\nTotal images: {len(image_paths)}")
    print(f"Day range: {min(day_labels)} to {max(day_labels)}")
    
    return image_paths, day_labels

if __name__ == "__main__":
    image_paths, day_labels = prepare_dataset()
    
    # Save dataset info
    import json
    dataset_info = {
        "total_images": len(image_paths),
        "min_day": min(day_labels),
        "max_day": max(day_labels),
        "samples": list(zip(image_paths[:5], day_labels[:5]))  # First 5 as examples
    }
    
    with open("dataset_info.json", "w") as f:
        json.dump(dataset_info, f, indent=2)
    
    print("\nDataset info saved to dataset_info.json")

