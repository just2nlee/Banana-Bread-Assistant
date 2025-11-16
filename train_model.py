"""
Train ResNet18 model for banana ripeness prediction.
Fine-tunes pretrained ResNet18 to predict days until bake-ready.
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from PIL import Image
import os
from pathlib import Path
import json
import random
from prepare_data import prepare_dataset
import numpy as np

class BananaDataset(Dataset):
    """Dataset for banana images with day labels."""
    
    def __init__(self, image_paths, day_labels, death_days, transform=None):
        self.image_paths = image_paths
        self.day_labels = day_labels
        self.death_days = death_days
        self.transform = transform
        
    def __len__(self):
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        day = self.day_labels[idx]
        death_day = self.death_days[idx]
        
        if self.transform:
            image = self.transform(image)
        
        # Convert day to "days until death" using the specific death day for this banana
        days_until_death = death_day - day
        
        return image, torch.tensor(days_until_death, dtype=torch.float32)

def create_model(num_classes=1):
    """Create and return fine-tuned ResNet18 model."""
    # Load pretrained ResNet18
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    
    # Freeze early layers
    for param in model.parameters():
        param.requires_grad = False
    
    # Unfreeze last few layers for fine-tuning
    for param in model.layer4.parameters():
        param.requires_grad = True
    for param in model.fc.parameters():
        param.requires_grad = True
    
    # Replace final layer for regression (days until death)
    model.fc = nn.Linear(model.fc.in_features, 1)
    
    return model

def train_model(data_dir=".", epochs=50, batch_size=8, learning_rate=0.001):
    """Train the banana ripeness prediction model."""
    
    print("Preparing dataset...")
    image_paths, day_labels, death_days = prepare_dataset(data_dir)
    
    if len(image_paths) == 0:
        raise ValueError("No images found! Check your data directory.")
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    # Split data indices
    dataset_size = len(image_paths)
    indices = list(range(dataset_size))
    random.shuffle(indices)
    train_size = int(0.8 * dataset_size)
    train_indices = indices[:train_size]
    val_indices = indices[train_size:]
    
    # Create separate datasets with different transforms
    train_image_paths = [image_paths[i] for i in train_indices]
    train_day_labels = [day_labels[i] for i in train_indices]
    train_death_days = [death_days[i] for i in train_indices]
    val_image_paths = [image_paths[i] for i in val_indices]
    val_day_labels = [day_labels[i] for i in val_indices]
    val_death_days = [death_days[i] for i in val_indices]
    
    train_dataset = BananaDataset(train_image_paths, train_day_labels, train_death_days, train_transform)
    val_dataset = BananaDataset(val_image_paths, val_day_labels, val_death_days, val_transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    print(f"Train samples: {len(train_dataset)}, Val samples: {len(val_dataset)}")
    
    # Create model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    model = create_model()
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
    
    # Training loop
    best_val_loss = float('inf')
    train_losses = []
    val_losses = []
    
    print("\nStarting training...")
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images).squeeze()
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        train_losses.append(train_loss)
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images).squeeze()
                loss = criterion(outputs, labels)
                val_loss += loss.item()
        
        val_loss /= len(val_loader)
        val_losses.append(val_loss)
        
        scheduler.step(val_loss)
        
        print(f"Epoch {epoch+1}/{epochs} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), "banana_model.pt")
            print(f"  -> Saved best model (val_loss: {val_loss:.4f})")
    
    print(f"\nTraining complete! Best validation loss: {best_val_loss:.4f}")
    print("Model saved as banana_model.pt")
    
    # Save training history
    history = {
        "train_losses": train_losses,
        "val_losses": val_losses,
        "best_val_loss": best_val_loss
    }
    with open("training_history.json", "w") as f:
        json.dump(history, f, indent=2)
    
    return model

if __name__ == "__main__":
    train_model(epochs=50, batch_size=8, learning_rate=0.001)

