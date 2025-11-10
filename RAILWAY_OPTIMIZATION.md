# Railway Deployment Optimization

## Problem
Build image size is 7.4GB, exceeding Railway's 4GB free tier limit.

## Solution 1: Use CPU-Only PyTorch (Recommended) ✅

I've updated `api/requirements.txt` to use **CPU-only PyTorch**, which is much smaller (~500MB vs ~2-3GB).

### What Changed:
- Added `--index-url https://download.pytorch.org/whl/cpu` to use CPU-only builds
- This reduces PyTorch size from ~2-3GB to ~500MB
- Your code already uses CPU (falls back if CUDA unavailable), so no code changes needed

### Try Deploying Again:
1. Commit the updated `requirements.txt`
2. Push to GitHub
3. Railway will rebuild automatically
4. Should now be under 4GB limit!

## Solution 2: Use .dockerignore (Additional Optimization)

Create `api/.dockerignore` to exclude unnecessary files:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.pt
*.pth
*.pkl
.git/
.gitignore
*.md
.env
.venv/
venv/
```

## Solution 3: Multi-Stage Build (Advanced)

If still too large, use a Dockerfile with multi-stage build to reduce final image size.

## Solution 4: Alternative Platforms

If Railway still doesn't work:

### Render.com
- **Free tier**: 750 hours/month
- **No build size limit** (but slower builds)
- Better for ML workloads

### Fly.io
- **Free tier**: 3 shared VMs
- **No build size limit**
- Good for containerized apps

### Google Cloud Run
- **Free tier**: 2 million requests/month
- **No build size limit**
- Pay per use

## Solution 5: Upgrade Railway Plan

If you want to stick with Railway:
- **Hobby Plan**: $5/month - Higher limits
- **Pro Plan**: $20/month - Even higher limits

## Recommended Approach

1. **First**: Try the CPU-only PyTorch (already done) - should reduce to ~2-3GB
2. **If still too large**: Try Render.com (no build size limit)
3. **If you need Railway specifically**: Consider upgrading to Hobby plan

## Testing the Optimization

After deploying with CPU-only PyTorch:
1. Check Railway build logs - should show smaller size
2. Test API: `https://your-api.railway.app/health`
3. Test prediction: Upload a banana image

The CPU-only version works the same, just slower (but still fast enough for predictions).

