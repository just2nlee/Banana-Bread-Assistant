# Analytics Setup Guide

## Option 1: Vercel Analytics (Already Set Up! ✅)

**Status**: Installed and configured!

**What it tracks**:
- Page views
- Unique visitors
- Traffic sources
- Performance metrics
- Geographic data

**How to view**:
1. Go to [vercel.com](https://vercel.com) dashboard
2. Click on your project
3. Go to **Analytics** tab
4. See daily/weekly/monthly stats

**Cost**: Free on Vercel (included)

## Option 2: Google Analytics (Optional)

For more detailed analytics, you can also add Google Analytics:

### Setup Steps:

1. **Create Google Analytics Account**:
   - Go to [analytics.google.com](https://analytics.google.com)
   - Create account and property
   - Get your Measurement ID (format: `G-XXXXXXXXXX`)

2. **Add to Vercel Environment Variables**:
   - Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add: `NEXT_PUBLIC_GA_ID` = `G-XXXXXXXXXX`
   - Select all environments
   - Save

3. **Enable in Code** (already created component):
   - Uncomment Google Analytics in `frontend/app/layout.tsx`
   - Or add it manually

4. **Redeploy**:
   - Vercel will auto-deploy or manually redeploy

### What Google Analytics Tracks:
- Detailed user behavior
- Session duration
- Bounce rate
- User flow
- Custom events
- Demographics

## Option 3: Railway Logs (API Usage)

Track API usage from Railway:

1. **Railway Dashboard** → Your Service → **Logs**
2. Count `POST /predict` requests
3. Or use **Metrics** tab for request counts

**Railway Metrics**:
- Request count
- Response times
- Error rates
- Resource usage

## Quick Stats Check

### Vercel Analytics:
- Dashboard → Analytics tab
- See visitors, page views, top pages

### Railway Metrics:
- Dashboard → Metrics tab
- See API request count, response times

### Google Analytics (if set up):
- analytics.google.com
- Real-time and historical data

## Recommended Setup

**For most users**: Vercel Analytics is enough!
- Already set up ✅
- Free
- Shows daily visitors
- Easy to view

**For detailed tracking**: Add Google Analytics
- More detailed insights
- Better for marketing
- Free tier available

## Current Setup

✅ **Vercel Analytics**: Active (tracks frontend)
✅ **Railway Logs**: Available (tracks API usage)

You can check your daily visitors right now in Vercel Dashboard → Analytics!

