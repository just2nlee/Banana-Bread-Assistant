# Quick Fix for Railway 4GB Limit

## ✅ Solution: CPU-Only PyTorch

I've updated `api/requirements.txt` to use **CPU-only PyTorch**, which reduces size from ~2-3GB to ~500MB.

### What to Do:

1. **Commit and push the changes**:
   ```bash
   git add api/requirements.txt
   git commit -m "Optimize PyTorch for Railway deployment"
   git push
   ```

2. **Railway will auto-rebuild** - should now be under 4GB!

### If It Still Fails:

**Option A: Use Render.com Instead** (No build size limit)
- Go to [render.com](https://render.com)
- New → Web Service
- Connect GitHub repo
- Root Directory: `api`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Option B: Upgrade Railway** ($5/month Hobby plan)
- Better limits
- Still cheaper than alternatives

**Option C: Use Dockerfile** (More control)
- Create `api/Dockerfile` with multi-stage build
- Railway will use it automatically

## Expected Results

- **Before**: 7.4GB (too large)
- **After**: ~2-3GB (should work on free tier)

The CPU-only version works identically, just uses CPU instead of GPU (which Railway doesn't have anyway).

