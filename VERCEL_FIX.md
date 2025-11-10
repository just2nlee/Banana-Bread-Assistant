# Fixing Vercel Deployment - SIGKILL Error

## Problem
The build is being killed (SIGKILL) because **PyTorch is too large** (~2-3GB) for Vercel's serverless functions (50MB limit).

## Solution: Deploy Frontend on Vercel, API Separately

### Step 1: Deploy Frontend Only on Vercel

The `vercel.json` has been updated to deploy only the frontend.

1. **Deploy frontend**:
   ```bash
   vercel --prod
   ```

2. **Or via Dashboard**:
   - Go to Vercel Dashboard
   - Import project
   - **Root Directory**: `frontend`
   - Deploy

### Step 2: Deploy API on Railway (Recommended)

Railway handles PyTorch much better:

1. **Go to [railway.app](https://railway.app)**
2. **New Project** → Deploy from GitHub
3. **Select your repository**
4. **Settings**:
   - Root Directory: `api`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   - Add `PORT` (Railway sets this automatically)
6. **Deploy!**

### Step 3: Connect Frontend to API

1. **Get your Railway API URL** (e.g., `https://your-api.railway.app`)

2. **Set environment variable in Vercel**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-api.railway.app`

3. **Redeploy frontend**:
   ```bash
   vercel --prod
   ```

## Alternative: Render.com

If Railway doesn't work:

1. Go to [render.com](https://render.com)
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - Root Directory: `api`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Current Configuration

- ✅ `vercel.json` - Now configured for frontend only
- ✅ Frontend will auto-detect API URL from environment variable
- ✅ API should be deployed separately

## Test Your Deployment

1. **Frontend**: `https://your-project.vercel.app`
2. **API Health**: `https://your-api.railway.app/health`
3. **Full Flow**: Upload a banana image on the frontend

## Why This Works

- **Vercel**: Great for Next.js frontend (small, fast)
- **Railway/Render**: Better for ML workloads with large dependencies
- **Separation**: Each service optimized for its purpose

