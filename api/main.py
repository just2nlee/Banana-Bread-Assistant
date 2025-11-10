"""
FastAPI backend for BananaPredictor.
Handles image uploads and returns ripeness predictions.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import numpy as np

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None

def load_model():
    """Load the trained ResNet18 model."""
    global model
    import os
    from pathlib import Path
    
    # Get current working directory and script directory
    cwd = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current working directory: {cwd}")
    print(f"Script directory: {script_dir}")
    
    # Try multiple possible model paths
    possible_paths = [
        "banana_model.pt",
        "../banana_model.pt",
        os.path.join(script_dir, "banana_model.pt"),
        os.path.join(script_dir, "..", "banana_model.pt"),
        os.path.join(cwd, "banana_model.pt"),
        os.path.join(cwd, "api", "banana_model.pt"),
    ]
    
    print("Searching for model file in the following paths:")
    model_path = None
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        exists = os.path.exists(path)
        print(f"  {path} -> {abs_path} (exists: {exists})")
        if exists:
            model_path = path
            break
    
    if model_path is None:
        print("ERROR: banana_model.pt not found in any of the searched paths!")
        print(f"Listing files in current directory: {os.listdir(cwd)}")
        if os.path.exists(script_dir):
            print(f"Listing files in script directory: {os.listdir(script_dir)}")
        return False
    
    try:
        # Create model architecture
        model = models.resnet18(weights=None)  # Use weights=None instead of pretrained=False
        model.fc = nn.Linear(model.fc.in_features, 1)
        
        # Load weights
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        model = model.to(device)
        print(f"Model loaded successfully from {model_path}!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    load_model()
    yield
    # Shutdown (if needed, add cleanup here)

app = FastAPI(title="BananaPredictor API", lifespan=lifespan)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                        std=[0.229, 0.224, 0.225])
])

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "BananaPredictor API is running!", "model_loaded": model is not None}

@app.get("/health")
async def health():
    """Health check with model status."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": str(device)
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict days until bake-ready for uploaded banana image.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        print(f"Received file: {file.filename}, content_type: {file.content_type}, size: {file.size if hasattr(file, 'size') else 'unknown'}")
        
        # Read image
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        print(f"Read {len(contents)} bytes from file")
        
        # Open and convert image
        try:
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            print(f"Image opened successfully: {image.size}")
        except Exception as e:
            print(f"Error opening image: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        
        # Preprocess
        try:
            image_tensor = transform(image).unsqueeze(0).to(device)
            print(f"Image preprocessed, tensor shape: {image_tensor.shape}")
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            raise HTTPException(status_code=500, detail=f"Image preprocessing error: {str(e)}")
        
        # Predict
        try:
            with torch.no_grad():
                prediction = model(image_tensor).item()
            print(f"Prediction made: {prediction}")
        except Exception as e:
            print(f"Error during prediction: {e}")
            raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
        
        # Convert prediction to days until bake-ready
        # Model predicts days until death, so we need to convert
        # Assuming day 16 is "death", and bake-ready is around day 8-10
        days_until_death = max(0, round(prediction))
        days_until_bake_ready = max(0, days_until_death - 6)  # Adjust based on your data
        
        # Clamp to reasonable range
        days_until_bake_ready = min(14, max(0, days_until_bake_ready))
        
        result = {
            "prediction": days_until_bake_ready,
            "days_until_bake_ready": days_until_bake_ready,
            "message": f"Predicted: {days_until_bake_ready} days until bake-ready 🍞",
            "raw_prediction": float(prediction)
        }
        
        print(f"Returning result: {result}")
        return result
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Unexpected error in predict endpoint: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

