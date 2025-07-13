# Troubleshooting Guide

This guide helps you resolve common issues when setting up and running the n8n video generation system.

## Quick Diagnostic

Run this command to check your system status:
```bash
./scripts/health_check.sh
```

## Common Issues and Solutions

### 1. Port Conflicts

**Problem**: "Address already in use" or "Port XXXX is in use"

**Symptoms**:
- Servers fail to start
- Error messages about ports being occupied

**Solutions**:

#### Check what's using the ports:
```bash
# Check ports 5001, 5002, 5003
lsof -i :5001
lsof -i :5002
lsof -i :5003
```

#### Kill existing processes:
```bash
# Kill processes on specific ports
lsof -ti:5001 | xargs kill -9
lsof -ti:5002 | xargs kill -9
lsof -ti:5003 | xargs kill -9
```

#### Use the stop script:
```bash
./scripts/stop_all_servers.sh
```

### 2. Missing Dependencies

**Problem**: "ModuleNotFoundError: No module named 'X'"

**Common missing modules**:
- `gtts` (Google Text-to-Speech)
- `diffusers` (Hugging Face Diffusers)
- `torch` (PyTorch)
- `flask` (Flask web framework)

**Solutions**:

#### Install all dependencies:
```bash
pip install -r requirements.txt
```

#### Install specific packages:
```bash
pip install gtts diffusers torch flask
```

#### For Apple Silicon Macs (M1/M2/M3):
```bash
# Install PyTorch with MPS support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 3. Memory Issues

**Problem**: Servers crash or become unresponsive

**Symptoms**:
- "Out of memory" errors
- Slow performance
- Servers freezing

**Solutions**:

#### Check available memory:
```bash
# Check memory usage
top -l 1 | grep PhysMem
```

#### Close unnecessary applications:
- Close browser tabs
- Quit other development servers
- Close memory-intensive applications

#### Restart your computer:
```bash
sudo shutdown -r now
```

#### Reduce video generation parameters:
- Use fewer frames (32 instead of 64)
- Lower resolution settings
- Reduce batch sizes

### 4. GPU/Acceleration Issues

**Problem**: "MPS not available" or CUDA errors

**Solutions**:

#### For Apple Silicon Macs:
```bash
# Check MPS availability
python3 -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```

#### Install PyTorch with MPS support:
```bash
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### Force CPU mode (if GPU fails):
Edit the server files to use CPU instead of MPS:
```python
# In enhanced_animatediff_server.py, change:
device = "cpu"  # instead of "mps"
```

### 5. Python Version Issues

**Problem**: "Python version not supported"

**Solutions**:

#### Check Python version:
```bash
python3 --version
```

#### Install Python 3.9+:
```bash
# Using Homebrew
brew install python@3.9

# Or download from python.org
```

#### Use virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. File Permission Issues

**Problem**: "Permission denied" errors

**Solutions**:

#### Make scripts executable:
```bash
chmod +x scripts/*.sh
```

#### Check file permissions:
```bash
ls -la scripts/
ls -la servers/
```

#### Fix permissions:
```bash
chmod 755 scripts/*.sh
chmod 644 servers/*.py
```

### 7. Network/Connection Issues

**Problem**: Can't connect to servers

**Solutions**:

#### Check if servers are running:
```bash
ps aux | grep python
```

#### Test server endpoints:
```bash
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

#### Check firewall settings:
- Ensure localhost connections are allowed
- Check if antivirus is blocking connections

### 8. n8n Integration Issues

**Problem**: n8n can't connect to servers

**Solutions**:

#### Verify server URLs in n8n:
- Use `http://localhost:5001` (not `127.0.0.1`)
- Check port numbers match
- Ensure servers are running

#### Test HTTP requests manually:
```bash
# Test AnimateDiff
curl -X POST http://localhost:5002/generate_video \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}'

# Test TTS
curl -X POST http://localhost:5001/generate_audio \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'
```

### 9. Model Download Issues

**Problem**: "Model not found" or download failures

**Solutions**:

#### Clear model cache:
```bash
rm -rf ~/.cache/huggingface/
rm -rf ~/.cache/torch/
```

#### Manual model download:
```bash
python3 -c "
from diffusers import DiffusionPipeline
pipeline = DiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')
"
```

#### Check internet connection:
```bash
ping google.com
```

### 10. Audio/Video Processing Issues

**Problem**: Audio or video files not generated

**Solutions**:

#### Check file paths:
```bash
ls -la /tmp/
```

#### Verify file permissions:
```bash
ls -la /tmp/generated_*
```

#### Check disk space:
```bash
df -h
```

#### Test individual components:
```bash
# Test TTS
python3 -c "
from gtts import gTTS
tts = gTTS('test')
tts.save('test.mp3')
"

# Test video processing
python3 -c "
import cv2
import numpy as np
img = np.zeros((512,512,3), dtype=np.uint8)
cv2.imwrite('test.jpg', img)
"
```

## Performance Optimization

### For Apple Silicon Macs:

1. **Enable MPS acceleration**:
```python
device = "mps" if torch.backends.mps.is_available() else "cpu"
```

2. **Optimize memory usage**:
```python
torch.backends.cudnn.benchmark = True
```

3. **Use smaller models**:
- Reduce frame count
- Lower resolution
- Use faster inference settings

### For Intel Macs:

1. **Use CPU optimization**:
```python
torch.set_num_threads(4)  # Adjust based on your CPU
```

2. **Close other applications** during video generation

3. **Use lower quality settings** for faster processing

## Debugging Steps

### 1. Enable Verbose Logging

Add debug prints to server files:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Check Server Logs

Monitor server output:
```bash
# In separate terminals
python3 servers/enhanced_animatediff_server.py
python3 servers/tts_server.py
python3 servers/video_processor.py
```

### 3. Test Individual Components

Test each server independently:
```bash
# Test AnimateDiff
curl -X POST http://localhost:5002/generate_video \
  -H "Content-Type: application/json" \
  -d '{"prompt": "simple test"}'

# Test TTS
curl -X POST http://localhost:5001/generate_audio \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'
```

### 4. System Resource Monitoring

Monitor system resources:
```bash
# Monitor CPU and memory
top -l 1

# Monitor disk usage
df -h

# Monitor network
netstat -an | grep LISTEN
```

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Run the health check script**: `./scripts/health_check.sh`
3. **Check server logs** for error messages
4. **Verify system requirements** are met
5. **Test with minimal examples**

### Information to Provide

When asking for help, include:

1. **System information**:
   ```bash
   uname -a
   python3 --version
   pip list
   ```

2. **Error messages** (copy exact text)

3. **Steps to reproduce** the issue

4. **What you've already tried**

5. **Health check output**:
   ```bash
   ./scripts/health_check.sh
   ```

### Common Solutions Summary

| Issue | Quick Fix |
|-------|-----------|
| Port conflicts | `./scripts/stop_all_servers.sh` |
| Missing dependencies | `pip install -r requirements.txt` |
| Memory issues | Restart computer, close apps |
| GPU issues | Reinstall PyTorch with MPS support |
| Python version | Install Python 3.9+ |
| File permissions | `chmod +x scripts/*.sh` |
| Network issues | Check if servers are running |
| Model issues | Clear cache, check internet |

---

**Remember**: Most issues can be resolved by following the setup guide carefully and ensuring all prerequisites are met. 