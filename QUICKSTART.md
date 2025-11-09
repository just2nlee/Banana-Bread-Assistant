# Quick Start Guide

## Step 1: Train the Model

First, you need to train the ResNet18 model on your banana images:

```bash
# Install dependencies
pip install -r requirements.txt

# Train the model (this will take a while)
python train_model.py
```

This will:
- Load all images from `Banana_*_Pics` folders
- Extract day labels from filenames
- Fine-tune ResNet18
- Save `banana_model.pt` in the root directory

**Note**: Training may take 10-30 minutes depending on your hardware. The model will be saved as `banana_model.pt`.

## Step 2: Set Up Virtual Environment (Recommended)

Create and activate a virtual environment to avoid dependency conflicts:

```bash
# Create virtual environment
py -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Step 3: Start the Backend API

With the virtual environment activated:

```bash
# Install dependencies (if not already installed)
python -m pip install -r requirements.txt

# Start the API
cd api
python main.py
```

The API will start on `http://localhost:8000`

**Important**: 
- Make sure `banana_model.pt` exists in the root directory
- Use `python` (not `py`) when the virtual environment is activated
- The "Could not find platform independent libraries" warning is harmless and can be ignored

## Step 4: Start the Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will start on `http://localhost:3000`

## Step 5: Test It!

1. Open `http://localhost:3000` in your browser
2. Upload a banana image
3. See the prediction!

## Troubleshooting

### Model not found error
- Make sure you've run `python train_model.py` first
- Check that `banana_model.pt` exists in the root directory
- The API will look for the model in multiple locations

### CORS errors
- Make sure the API is running on port 8000
- Check that `NEXT_PUBLIC_API_URL` in frontend matches your API URL

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- For frontend: `npm install` in the `frontend` directory
- **Use a virtual environment** to avoid Python path issues

### "Could not find platform independent libraries" warning
- This is a harmless warning from Python 3.14 and can be safely ignored
- The API will still work correctly despite this message
- Using a virtual environment helps isolate dependencies

## Next Steps

- Deploy to Vercel (frontend) and Railway/Render (backend)
- Fine-tune the model with more data
- Add the Banana Tracker Dashboard feature

