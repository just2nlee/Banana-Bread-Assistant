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

def extract_banana_number_from_folder(folder_name: str) -> int:
    """Extract banana number from folder name like 'Banana_1_Pics' -> 1"""
    match = re.search(r'Banana_(\d+)', folder_name)
    if match:
        return int(match.group(1))
    return None

def get_death_days() -> dict:
    """Return dictionary mapping banana number to death day."""
    return {
        1: 23,
        2: 16,
        3: 23,
        4: 23,
        5: 14,
        6: 23,
        7: 23,
        8: 17,
        9: 17,
        10: 16
    }

def prepare_dataset(data_dir: str = ".", output_dir: str = "dataset") -> Tuple[List[str], List[int], List[int]]:
    """
    Prepare dataset from banana image folders.
    Returns: (image_paths, day_labels, death_days)
    """
    data_path = Path(data_dir)
    image_paths = []
    day_labels = []
    death_days = []
    
    death_day_map = get_death_days()
    
    # Find all banana folders
    banana_folders = sorted([d for d in data_path.iterdir() 
                            if d.is_dir() and d.name.startswith("Banana_")])
    
    print(f"Found {len(banana_folders)} banana folders")
    
    for folder in banana_folders:
        banana_num = extract_banana_number_from_folder(folder.name)
        if banana_num is None:
            print(f"  Warning: Could not extract banana number from {folder.name}, skipping...")
            continue
            
        banana_death_day = death_day_map.get(banana_num)
        if banana_death_day is None:
            print(f"  Warning: No death day defined for banana {banana_num}, skipping...")
            continue
        
        # Get all images in this folder
        images = sorted([f for f in folder.iterdir() 
                        if f.suffix.lower() in ['.jpeg', '.jpg', '.png']])
        
        for img_path in images:
            day = extract_day_from_filename(img_path.name)
            if day is not None:
                image_paths.append(str(img_path))
                day_labels.append(day)
                death_days.append(banana_death_day)
                print(f"  {img_path.name} -> Day {day} (Banana {banana_num}, Death Day: {banana_death_day})")
    
    print(f"\nTotal images: {len(image_paths)}")
    if day_labels:
        print(f"Day range: {min(day_labels)} to {max(day_labels)}")
    
    return image_paths, day_labels, death_days

if __name__ == "__main__":
    image_paths, day_labels, death_days = prepare_dataset()
    
    # Save dataset info
    import json
    dataset_info = {
        "total_images": len(image_paths),
        "min_day": min(day_labels) if day_labels else 0,
        "max_day": max(day_labels) if day_labels else 0,
        "death_days": get_death_days(),
        "samples": list(zip(image_paths[:5], day_labels[:5], death_days[:5]))  # First 5 as examples
    }
    
    with open("dataset_info.json", "w") as f:
        json.dump(dataset_info, f, indent=2)
    
    print("\nDataset info saved to dataset_info.json")

