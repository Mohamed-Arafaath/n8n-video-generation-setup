# Video Length Guide

This guide explains how to optimize video generation parameters for different use cases and performance requirements.

## 🎬 Video Generation Parameters

### Frame Count vs Duration

The AnimateDiff server generates videos based on frame count, not duration. Here's the relationship:

| Frames | Duration | Use Case |
|--------|----------|----------|
| 16     | 2 seconds | Quick previews, testing |
| 32     | 4 seconds | Short clips, social media |
| 48     | 6 seconds | Standard videos |
| 64     | 8 seconds | **Recommended default** |
| 96     | 12 seconds | Longer content |
| 128    | 16 seconds | Maximum length |

### Performance Impact

**Generation Time by Frame Count:**
- 16 frames: 10-15 seconds
- 32 frames: 20-30 seconds
- 48 frames: 30-45 seconds
- 64 frames: 45-60 seconds
- 96 frames: 60-90 seconds
- 128 frames: 90-120 seconds

## 🎯 Optimization Strategies

### For Quick Testing
```json
{
  "prompt": "A beautiful sunset",
  "num_frames": 16,
  "guidance_scale": 7.0,
  "num_inference_steps": 15
}
```

### For Social Media Content
```json
{
  "prompt": "Cinematic scene of mountains",
  "num_frames": 32,
  "guidance_scale": 7.5,
  "num_inference_steps": 20
}
```

### For Professional Videos
```json
{
  "prompt": "Epic cinematic landscape",
  "num_frames": 64,
  "guidance_scale": 8.0,
  "num_inference_steps": 25
}
```

### For Maximum Quality
```json
{
  "prompt": "Stunning cinematic masterpiece",
  "num_frames": 96,
  "guidance_scale": 8.5,
  "num_inference_steps": 30
}
```

## ⚡ Performance Optimization

### Apple Silicon Macs (M1/M2/M3)

**Optimal Settings:**
- **Frame Count**: 32-64 frames
- **Guidance Scale**: 7.0-8.0
- **Inference Steps**: 20-25
- **Device**: MPS (Metal Performance Shaders)

**Memory Usage:**
- 32 frames: 4-6GB RAM
- 64 frames: 6-8GB RAM
- 96+ frames: 8-12GB RAM

### Intel Macs

**Optimal Settings:**
- **Frame Count**: 16-48 frames
- **Guidance Scale**: 6.5-7.5
- **Inference Steps**: 15-20
- **Device**: CPU

**Memory Usage:**
- 16 frames: 2-4GB RAM
- 32 frames: 4-6GB RAM
- 48 frames: 6-8GB RAM

## 📊 Quality vs Speed Trade-offs

### High Quality (Slower)
```json
{
  "num_frames": 96,
  "guidance_scale": 8.5,
  "num_inference_steps": 30
}
```
- **Pros**: Smooth motion, high detail
- **Cons**: Long generation time (90-120 seconds)
- **Best for**: Final production videos

### Balanced (Recommended)
```json
{
  "num_frames": 64,
  "guidance_scale": 7.5,
  "num_inference_steps": 20
}
```
- **Pros**: Good quality, reasonable speed
- **Cons**: Moderate generation time (45-60 seconds)
- **Best for**: Most use cases

### Fast Generation
```json
{
  "num_frames": 32,
  "guidance_scale": 7.0,
  "num_inference_steps": 15
}
```
- **Pros**: Quick generation (20-30 seconds)
- **Cons**: Shorter duration, less detail
- **Best for**: Testing, previews, social media

## 🎨 Creative Guidelines

### Scene Types by Length

**Short Clips (16-32 frames):**
- Quick transitions
- Simple movements
- Abstract patterns
- Logo animations

**Medium Clips (48-64 frames):**
- Landscape pans
- Character movements
- Product showcases
- Story scenes

**Long Clips (96-128 frames):**
- Complex narratives
- Detailed animations
- Cinematic sequences
- Music videos

### Prompt Optimization

**For Short Videos:**
- Use simple, clear descriptions
- Focus on one main element
- Avoid complex scenes

**For Long Videos:**
- Include detailed descriptions
- Specify camera movements
- Add atmospheric elements

## 🔧 Technical Parameters

### Guidance Scale
- **Range**: 1.0-20.0
- **Recommended**: 7.0-8.5
- **Effect**: Controls adherence to prompt
- **Higher**: More faithful to prompt, less creative
- **Lower**: More creative, less faithful

### Inference Steps
- **Range**: 10-50
- **Recommended**: 15-25
- **Effect**: Quality vs speed trade-off
- **Higher**: Better quality, slower generation
- **Lower**: Faster generation, lower quality

### Frame Rate
- **Default**: 8 FPS (frames per second)
- **Effect**: Determines video smoothness
- **Note**: Fixed in current implementation

## 📱 Platform-Specific Recommendations

### Instagram Stories
```json
{
  "num_frames": 32,
  "guidance_scale": 7.0,
  "num_inference_steps": 15
}
```

### TikTok/Reels
```json
{
  "num_frames": 48,
  "guidance_scale": 7.5,
  "num_inference_steps": 20
}
```

### YouTube Shorts
```json
{
  "num_frames": 64,
  "guidance_scale": 8.0,
  "num_inference_steps": 25
}
```

### Professional Content
```json
{
  "num_frames": 96,
  "guidance_scale": 8.5,
  "num_inference_steps": 30
}
```

## 🚨 Troubleshooting

### Common Issues

**Out of Memory Errors:**
- Reduce frame count
- Close other applications
- Restart the server

**Slow Generation:**
- Reduce inference steps
- Use lower guidance scale
- Check system resources

**Poor Quality:**
- Increase inference steps
- Use higher guidance scale
- Improve prompt description

### Performance Monitoring

**Check System Resources:**
```bash
# Monitor CPU and memory
top -l 1

# Check available memory
vm_stat
```

**Server Health:**
```bash
# Check server status
curl http://localhost:5002/health
```

## 📈 Best Practices

### 1. Start Small
- Begin with 16-32 frames for testing
- Gradually increase for production

### 2. Batch Processing
- Generate multiple short videos
- Combine in post-processing

### 3. Prompt Engineering
- Be specific about desired length
- Include timing cues in prompts

### 4. Resource Management
- Monitor system resources
- Close unnecessary applications
- Use appropriate settings for your hardware

### 5. Quality Assurance
- Test with different parameters
- Keep track of successful combinations
- Document what works for your use case

## 🎯 Quick Reference

| Use Case | Frames | Duration | Time | Quality |
|----------|--------|----------|------|---------|
| Testing | 16 | 2s | 15s | Basic |
| Social Media | 32 | 4s | 30s | Good |
| Standard | 64 | 8s | 60s | Very Good |
| Professional | 96 | 12s | 90s | Excellent |
| Maximum | 128 | 16s | 120s | Best |

---

**Remember**: These are guidelines. Experiment with different settings to find what works best for your specific needs and hardware capabilities. 