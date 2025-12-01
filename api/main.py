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
from torchvision.models import ResNet18_Weights
from PIL import Image
import io
import numpy as np

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None
banana_classifier = None

# ImageNet class ID for banana
IMAGENET_BANANA_CLASS_ID = 954

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
        
        # Warmup: Run a dummy prediction to initialize CUDA/cache (faster first real prediction)
        print("Warming up model...")
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        with torch.no_grad():
            _ = model(dummy_input)
        print(f"Model loaded and warmed up successfully from {model_path}!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        return False

def load_banana_classifier():
    """Load ImageNet pretrained model for banana detection."""
    global banana_classifier
    try:
        print("Loading ImageNet pretrained model for banana validation...")
        banana_classifier = models.resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        banana_classifier.eval()
        banana_classifier = banana_classifier.to(device)
        
        # Warmup: Run a dummy prediction to initialize CUDA/cache
        print("Warming up banana classifier...")
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        with torch.inference_mode():
            _ = banana_classifier(dummy_input)
        print("Banana classifier loaded and warmed up successfully!")
        return True
    except Exception as e:
        print(f"Error loading banana classifier: {e}")
        print("Warning: Banana validation will be skipped if classifier fails to load")
        return False

def is_banana(image_tensor, confidence_threshold=0.01):
    """
    Check if image contains a banana using ImageNet pretrained model.
    
    Args:
        image_tensor: Preprocessed image tensor (1, 3, 224, 224)
        confidence_threshold: Minimum probability for banana class (default: 0.01 = 1%)
    
    Returns:
        tuple: (is_banana: bool, confidence: float)
    """
    if banana_classifier is None:
        # If classifier not loaded, fail closed (reject all images)
        print("WARNING: Banana classifier not loaded - rejecting image for safety")
        return False, 0.0
    
    try:
        with torch.inference_mode():
            predictions = banana_classifier(image_tensor)
            probabilities = torch.nn.functional.softmax(predictions[0], dim=0)
            
            # Get banana class probability (ImageNet class 954)
            banana_prob = probabilities[IMAGENET_BANANA_CLASS_ID].item()
            
            # Get top-5 predictions for debugging
            top5_probs, top5_indices = torch.topk(probabilities, 5)
            top5_indices = top5_indices.cpu().numpy()
            top5_probs = top5_probs.cpu().numpy()
            
            # Check if banana is in top 5 predictions
            banana_in_top5 = IMAGENET_BANANA_CLASS_ID in top5_indices
            
            # Log for debugging
            print(f"Banana validation - Probability: {banana_prob:.4f} ({banana_prob*100:.2f}%), In top-5: {banana_in_top5}")
            if banana_in_top5:
                banana_position = list(top5_indices).index(IMAGENET_BANANA_CLASS_ID)
                print(f"Banana found at position {banana_position + 1} in top-5 with probability {top5_probs[banana_position]:.4f}")
            
            # Validation: require banana to be in top-5 AND meet confidence threshold
            banana_in_top3 = IMAGENET_BANANA_CLASS_ID in top5_indices[:3]
            
            # Consider it a banana if:
            # 1. Banana probability meets threshold (1%), AND
            # 2. Banana is in top 5 predictions
            is_banana_result = banana_prob >= confidence_threshold 
            
            if not is_banana_result:
                print(f"Image rejected - Banana prob: {banana_prob:.4f}, Threshold: {confidence_threshold}, In top-5: {banana_in_top5}")
            
            return is_banana_result, banana_prob
    except Exception as e:
        print(f"Error in banana validation: {e}")
        import traceback
        traceback.print_exc()
        # On error, fail closed (reject the image)
        return False, 0.0

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    load_model()
    load_banana_classifier()  # Load banana classifier for validation
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

# Add request logging middleware (only log errors to reduce overhead)
@app.middleware("http")
async def log_requests(request, call_next):
    response = await call_next(request)
    if response.status_code >= 400:
        print(f"Error: {request.method} {request.url} -> {response.status_code}")
    return response

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
        "banana_classifier_loaded": banana_classifier is not None,
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
        # Read image
        contents = await file.read()
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Open and convert image (optimized: resize early if image is very large)
        try:
            image = Image.open(io.BytesIO(contents)).convert('RGB')
            # Resize early if image is very large to speed up preprocessing
            if max(image.size) > 1000:
                image.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        
        # Preprocess
        try:
            image_tensor = transform(image).unsqueeze(0).to(device)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image preprocessing error: {str(e)}")
        
        # Validate that the image is a banana BEFORE running ripeness prediction
        print("Running banana validation...")
        is_banana_result, banana_confidence = is_banana(image_tensor, confidence_threshold=0.01)
        
        if not is_banana_result:
            print(f"Banana validation failed - Confidence: {banana_confidence:.4f}")
            raise HTTPException(
                status_code=400, 
                detail=f"Image doesn't appear to be a banana. Please upload a photo of a banana. (Confidence: {banana_confidence:.1%})"
            )
        
        print(f"Banana validation passed - Confidence: {banana_confidence:.4f}")
        
        # Predict (optimized: use torch.inference_mode for faster inference)
        try:
            with torch.inference_mode():  # Faster than torch.no_grad()
                prediction = model(image_tensor).item()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
        
        # Convert prediction to days until bake-ready
        # Model predicts days until death, so we need to convert
        # Assuming day 16 is "death", and bake-ready is around day 8-10
        days_until_death = max(0, round(prediction))
        days_until_bake_ready = max(0, days_until_death - 6)  # Adjust based on your data
        
        # Clamp to reasonable range
        days_until_bake_ready = min(23, max(0, days_until_bake_ready))
        
        result = {
            "prediction": days_until_bake_ready,
            "days_until_bake_ready": days_until_bake_ready,
            "message": f"Predicted: {days_until_bake_ready} days until bake-ready 🍞",
            "raw_prediction": float(prediction)
        }
        
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

