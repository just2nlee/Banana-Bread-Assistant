# Deployment Steps - Fixed for PyTorch Issue

## The Problem
PyTorch is too large (~2-3GB) for Vercel serverless functions, causing SIGKILL errors.

## Solution: Separate Deployments

### ✅ Step 1: Deploy Frontend on Vercel

**Option A: Via Dashboard (Recommended)**

1. Go to [vercel.com](https://vercel.com) → Add New Project
2. Import your GitHub repository
3. **Important Settings**:
   - **Root Directory**: `frontend` ⚠️ (This is key!)
   - Framework: Next.js (auto-detected)
   - Build Command: (auto-detected)
   - Output Directory: (auto-detected)
4. Click **Deploy**

**Option B: Via CLI**

```bash
# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Follow prompts, make sure root is set to frontend/
```

### ✅ Step 2: Deploy API on Railway

1. **Go to [railway.app](https://railway.app)**
2. **Sign up/Login** (free tier available)
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Add Service** → **GitHub Repo** (if not auto-added)
6. **Configure Service**:
   - Click on the service
   - **Settings** tab:
     - **Root Directory**: `api`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. **Variables** tab:
   - `PORT` is auto-set by Railway
8. **Deploy** - Railway will automatically deploy

9. **Get your API URL**:
   - Go to **Settings** → **Networking**
   - Generate a public domain (e.g., `banana-api.railway.app`)
   - Copy the URL

### ✅ Step 3: Connect Frontend to API

1. **In Vercel Dashboard**:
   - Go to your project → **Settings** → **Environment Variables**
   - Add new variable:
     - **Name**: `NEXT_PUBLIC_API_URL`
     - **Value**: `https://your-api.railway.app` (your Railway URL)
     - **Environment**: Production, Preview, Development (select all)
   - Click **Save**

2. **Redeploy Frontend**:
   - Go to **Deployments** tab
   - Click **⋯** on latest deployment → **Redeploy**
   - Or push a new commit to trigger auto-deploy

## Testing

1. **Test API**: Visit `https://your-api.railway.app/health`
   - Should return: `{"status": "healthy", "model_loaded": true}`

2. **Test Frontend**: Visit `https://your-project.vercel.app`
   - Upload a banana image
   - Should get a prediction!

## File Structure

```
.
├── frontend/          ← Deploy this on Vercel (root: frontend/)
│   ├── app/
│   ├── components/
│   └── package.json
├── api/              ← Deploy this on Railway (root: api/)
│   ├── main.py
│   └── requirements.txt
└── banana_model.pt   ← Make sure this is in api/ or root
```

## Important Notes

- ✅ **Frontend**: Vercel (optimized for Next.js)
- ✅ **API**: Railway (handles PyTorch well)
- ✅ **Model File**: Make sure `banana_model.pt` is committed to git in `api/` folder
- ✅ **CORS**: API already configured to allow all origins

## Troubleshooting

### Frontend can't connect to API
- Check `NEXT_PUBLIC_API_URL` environment variable in Vercel
- Verify Railway API is running (check `/health` endpoint)
- Check browser console for CORS errors

### API returns 503 (Model not loaded)
- Verify `banana_model.pt` is in the `api/` directory
- Check Railway build logs for model loading errors
- Verify model path in `api/main.py`

### Railway deployment fails
- Check that `requirements.txt` includes all dependencies
- Verify Python version (Railway auto-detects, but you can set it)
- Check build logs for specific errors

