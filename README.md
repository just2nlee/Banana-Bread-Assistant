# 🍌 BananaPredictor

A web app that predicts when your bananas will be bake-ready using AI! Upload a photo and get a prediction of days until your banana is perfect for banana bread.

## Features

- **Banana Ripeness Predictor**: Upload a banana photo → get a prediction like "2 days until bake-ready 🍞"
- Built with ResNet18 (fine-tuned on banana ripeness data)
- Modern Next.js frontend with beautiful UI
- FastAPI backend for predictions

## Project Structure

```
.
├── api/                 # FastAPI backend
│   └── main.py         # API endpoints
├── frontend/            # Next.js frontend
│   ├── app/            # Next.js app directory
│   └── components/     # React components
├── prepare_data.py     # Data preparation script
├── train_model.py      # Model training script
└── requirements.txt    # Python dependencies
```

## Setup & Installation

### 1. Prepare Data & Train Model

```bash
# Install Python dependencies
pip install -r requirements.txt

# Prepare dataset (optional - to verify data)
python prepare_data.py

# Train the model
python train_model.py
```

This will:
- Load all banana images from the `Banana_*_Pics` folders
- Extract day labels from filenames (e.g., B1D5.jpeg = Day 5)
- Fine-tune ResNet18 to predict days until bake-ready
- Save model as `banana_model.pt`

### 2. Run Backend API

```bash
cd api
pip install -r requirements.txt

# Make sure banana_model.pt is in the api directory or parent
python main.py
```

API will run on `http://localhost:8000`

### 3. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on `http://localhost:3000`

## Deployment

### Backend (Vercel/Railway/Render)

1. **Vercel**: Create `vercel.json` for Python API
2. **Railway**: Connect GitHub repo, set Python runtime
3. **Render**: Create web service, set build/start commands

### Frontend (Vercel)

1. Connect GitHub repo to Vercel
2. Set root directory to `frontend`
3. Set `NEXT_PUBLIC_API_URL` environment variable to your API URL

## Model Details

- **Architecture**: ResNet18 (pretrained on ImageNet)
- **Task**: Regression (predict days until bake-ready)
- **Input**: 224x224 RGB images
- **Output**: Days until bake-ready (0-14 days)

The model is fine-tuned on your 10-banana dataset with images from Day 1 to Day 16, learning to predict ripeness progression.

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /predict` - Upload banana image, get prediction

## Future Features

- Banana Tracker Dashboard (log multiple bananas)
- Ripeness Timeline (visual progression)
- Community data aggregation

## License

MIT

