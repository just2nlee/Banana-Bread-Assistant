# Performance Optimization Guide

## Current Optimizations Applied ✅

1. **Model Warmup**: Model runs a dummy prediction on startup to initialize caches
2. **Reduced Logging**: Only log errors, not every request (reduces I/O overhead)
3. **Faster Inference**: Using `torch.inference_mode()` instead of `torch.no_grad()` (slightly faster)
4. **Early Image Resizing**: Large images are resized before preprocessing
5. **Better UX**: Loading message indicates it may take a few seconds

## Why It's Still Slow

The latency is primarily due to:
- **CPU-only PyTorch**: ~2-5 seconds per prediction on CPU
- **Railway Free Tier**: Limited CPU/memory resources
- **Model Size**: ResNet18 is relatively large for CPU inference

## Additional Optimization Options

### Option 1: Upgrade Railway Resources (Recommended)

**Railway Hobby Plan ($5/month)**:
- More CPU/memory = faster inference
- Better for ML workloads
- Usually reduces latency by 30-50%

**Steps**:
1. Railway Dashboard → Your Service → Settings
2. Upgrade to Hobby plan
3. Increase CPU/Memory allocation

### Option 2: Use a Smaller Model

Train a smaller model (MobileNet, EfficientNet-Lite) that's faster on CPU:
- Smaller models = faster inference
- May have slightly lower accuracy
- Better for production

### Option 3: Model Quantization

Quantize the model to INT8 (smaller, faster):
```python
# Add to model loading
import torch.quantization
model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
```

### Option 4: Use ONNX Runtime

Convert model to ONNX for faster CPU inference:
- ONNX Runtime is optimized for CPU
- Can be 2-3x faster than PyTorch on CPU

### Option 5: Add Response Caching

Cache predictions for identical images (if users upload same image):
- Use image hash as cache key
- Return cached result instantly

### Option 6: Use GPU (If Available)

If Railway supports GPU (Pro plan):
- GPU inference is 10-100x faster
- Requires CUDA-enabled PyTorch

## Expected Performance

**Current (CPU, Free Tier)**:
- First prediction: ~5-8 seconds
- Subsequent predictions: ~3-5 seconds

**With Hobby Plan**:
- First prediction: ~3-5 seconds
- Subsequent predictions: ~2-3 seconds

**With Quantization**:
- Can reduce by 30-40%

**With ONNX**:
- Can reduce by 50-60%

## Quick Wins

1. **Upgrade Railway** to Hobby plan ($5/month) - easiest improvement
2. **Reduce image size** before upload (client-side compression)
3. **Add progress indicator** (already done)

## Monitoring

Check Railway logs to see where time is spent:
- Image loading: ~0.1s
- Preprocessing: ~0.2s
- Model inference: ~3-5s (this is the bottleneck)
- Response: ~0.1s

The model inference is the main bottleneck on CPU.

