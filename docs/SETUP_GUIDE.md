# Detailed Setup Guide

This guide provides step-by-step instructions for setting up n8n with video generation capabilities on macOS.

## Prerequisites

### System Requirements
- **macOS**: 10.15+ (Catalina or later)
- **RAM**: Minimum 8GB, recommended 16GB+
- **Storage**: At least 20GB free space
- **Python**: 3.9 or higher
- **Node.js**: 16 or higher (for n8n)

### Hardware Requirements
- **Apple Silicon Macs** (M1/M2/M3): Optimized performance with MPS acceleration
- **Intel Macs**: Supported but slower performance
- **GPU**: Integrated graphics sufficient, dedicated GPU not required

## Step 1: Environment Setup

### 1.1 Install Python
```bash
# Check if Python is installed
python3 --version

# If not installed, download from python.org
# Or use Homebrew:
brew install python@3.9
```

### 1.2 Install Node.js (for n8n)
```bash
# Install Node.js using Homebrew
brew install node

# Verify installation
node --version
npm --version
```

### 1.3 Install Git
```bash
# Install Git if not already installed
brew install git

# Verify installation
git --version
```

## Step 2: Repository Setup

### 2.1 Clone the Repository
```bash
# Clone the repository
git clone <your-repo-url>
cd n8n-video-generation-setup

# Verify the structure
ls -la
```

### 2.2 Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation
which python
```

## Step 3: Install Dependencies

### 3.1 Install Python Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# This may take 10-15 minutes for the first time
# as it downloads large ML models
```

### 3.2 Verify Installation
```bash
# Test if key packages are installed
python3 -c "
import flask
import torch
import diffusers
import gtts
import cv2
import moviepy
print('✅ All dependencies installed successfully!')
"
```

## Step 4: Server Setup

### 4.1 Start All Servers
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Start all servers
./scripts/start_all_servers.sh
```

### 4.2 Verify Server Health
```bash
# Check if all servers are running
./scripts/health_check.sh
```

### 4.3 Manual Server Start (Alternative)
If the automatic script doesn't work, start servers manually:

```bash
# Terminal 1: AnimateDiff Server
python3 servers/enhanced_animatediff_server.py

# Terminal 2: TTS Server
python3 servers/tts_server.py

# Terminal 3: Video Processor
python3 servers/video_processor.py
```

## Step 5: n8n Setup

### 5.1 Install n8n
```bash
# Install n8n globally
npm install -g n8n

# Verify installation
n8n --version
```

### 5.2 Start n8n
```bash
# Start n8n
n8n start

# This will start n8n on http://localhost:5678
```

### 5.3 Import Workflow
1. Open your browser and go to `http://localhost:5678`
2. Click "Import from file"
3. Select `workflows/comprehensive-video-workflow.json`
4. Configure API keys in the workflow nodes

## Step 6: API Configuration

### 6.1 Required API Keys

#### Freepik API (for image generation)
1. Go to [Freepik API](https://developers.freepik.com/)
2. Create an account and get API key
3. Add to n8n workflow

#### Google Drive API (for video upload)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Drive API
3. Create service account and download JSON key
4. Add to n8n workflow

#### OpenAI API (optional, for enhanced story generation)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create account and get API key
3. Add to n8n workflow

### 6.2 Configure API Keys in n8n
1. Open the imported workflow
2. Click on each node that requires API keys
3. Enter your API credentials
4. Save the workflow

## Step 7: Testing

### 7.1 Test Individual Servers
```bash
# Test AnimateDiff Server
curl http://localhost:5002/health

# Test TTS Server
curl http://localhost:5001/health

# Test Video Processor
curl http://localhost:5003/health
```

### 7.2 Test Complete Workflow
1. In n8n, click "Execute Workflow"
2. Check if all nodes execute successfully
3. Verify video generation and upload

## Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using the ports
lsof -i :5001
lsof -i :5002
lsof -i :5003

# Kill processes if needed
kill -9 <PID>
```

#### Missing Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt

# For specific packages
pip install torch torchvision diffusers transformers
```

#### Memory Issues
- Close other applications
- Restart your computer
- Consider upgrading RAM

#### GPU Issues (Apple Silicon)
```bash
# Verify MPS support
python3 -c "import torch; print(torch.backends.mps.is_available())"
```

### Performance Optimization

#### For Apple Silicon Macs
- Ensure PyTorch is installed with MPS support
- Close unnecessary applications
- Use SSD storage for faster I/O

#### For Intel Macs
- Close other applications during video generation
- Consider using CPU-only mode for stability

## Maintenance

### Regular Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Update n8n
npm update -g n8n
```

### Log Management
```bash
# Check server logs
tail -f animatediff.log
tail -f tts.log
tail -f processor.log
```

### Backup
```bash
# Backup your workflows
cp workflows/*.json ~/backup/

# Backup your API keys configuration
```

## Next Steps

After successful setup:

1. **Customize Workflows**: Modify the workflows to suit your needs
2. **Add More APIs**: Integrate additional services
3. **Scale Up**: Consider running on a dedicated server
4. **Monitor**: Set up monitoring for production use

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review server logs for error messages
3. Verify all dependencies are installed
4. Ensure ports are not in use by other applications
5. Check system resources (RAM, disk space)

---

**Note**: This setup is optimized for macOS. For other operating systems, some modifications may be required. 