# Quick Vercel Deployment Guide

## Fixed Configuration ✅

The `vercel.json` has been fixed - removed the conflicting `builds` and `functions` properties.

## Deploy via CLI (Easiest)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Deploy** (from project root):
   ```bash
   vercel
   ```

4. **Follow prompts**:
   - Set up and deploy? **Yes**
   - Which scope? (select your account)
   - Link to existing project? **No** (first time)
   - Project name: `banana-bread-assistant`
   - Directory: `.` (press Enter for current directory)
   - Override settings? **No**

5. **For production deployment**:
   ```bash
   vercel --prod
   ```

## Configure in Vercel Dashboard

After first deployment via CLI:

1. Go to your project in Vercel Dashboard
2. **Settings → General**:
   - Root Directory: `.` (root)
   - Framework Preset: Next.js (auto-detected)

3. **Settings → Git** (optional - to enable auto-deploy):
   - Connect your GitHub repository
   - Enable "Automatic deployments from Git"

## Project Structure

- **Frontend**: `frontend/` - Next.js app (auto-detected)
- **API**: `api/main.py` - Python serverless function
- **Routes**: `/api/*` → Python API, `/*` → Next.js frontend

## Environment Variables (if needed)

In Vercel Dashboard → Settings → Environment Variables:
- `NEXT_PUBLIC_API_URL`: `/api` (or leave blank for default)

## Important Notes

⚠️ **PyTorch Size**: The API uses PyTorch which is very large. You may need:
- Vercel Pro plan for better limits
- Or deploy API separately on Railway/Render

## Troubleshooting

### "Failed to connect repository"
- Use CLI deployment instead (see above)
- Or check GitHub OAuth permissions

### Build fails
- Check that `banana_model.pt` is committed to git
- Verify Python version (3.11) in `api/vercel.json`

### API not working
- Check function logs in Vercel Dashboard
- Verify model file path in `api/main.py`

