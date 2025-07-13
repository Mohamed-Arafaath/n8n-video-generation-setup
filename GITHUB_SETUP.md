# GitHub Repository Setup Guide

This guide explains how to push this local repository to GitHub so your friend can access it.

## Step 1: Create GitHub Repository

1. **Go to GitHub.com** and sign in to your account
2. **Click the "+" icon** in the top right corner
3. **Select "New repository"**
4. **Fill in the repository details**:
   - Repository name: `n8n-video-generation-setup`
   - Description: `Complete setup for n8n with AI-powered video generation capabilities`
   - Make it **Public** (so your friend can access it)
   - **Don't** initialize with README (we already have one)
   - **Don't** add .gitignore (we already have one)
   - **Don't** add a license (we already have one)
5. **Click "Create repository"**

## Step 2: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/n8n-video-generation-setup.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify the Upload

1. **Go to your GitHub repository** in the browser
2. **Verify all files are there**:
   - README.md
   - requirements.txt
   - servers/ (folder with Python files)
   - workflows/ (folder with JSON files)
   - scripts/ (folder with shell scripts)
   - docs/ (folder with documentation)

## Step 4: Share with Your Friend

**Send your friend this link**:
```
https://github.com/YOUR_USERNAME/n8n-video-generation-setup
```

**Or share the clone command**:
```bash
git clone https://github.com/YOUR_USERNAME/n8n-video-generation-setup.git
```

## Repository Contents Summary

Your friend will get a complete setup with:

### 📁 Main Files
- `README.md` - Complete setup guide
- `requirements.txt` - All Python dependencies
- `LICENSE` - MIT license

### 🖥️ Servers
- `servers/enhanced_animatediff_server.py` - Video generation server
- `servers/tts_server.py` - Text-to-speech server  
- `servers/video_processor.py` - Video/audio merge server

### 🔄 Workflows
- `workflows/comprehensive-video-workflow.json` - Full workflow with all features
- `workflows/simple-video-workflow.json` - Basic workflow for testing

### 🛠️ Scripts
- `scripts/start_all_servers.sh` - Start all servers
- `scripts/stop_all_servers.sh` - Stop all servers
- `scripts/health_check.sh` - Check server health

### 📚 Documentation
- `docs/SETUP_GUIDE.md` - Detailed step-by-step setup
- `docs/API_REFERENCE.md` - Complete API documentation
- `docs/TROUBLESHOOTING.md` - Common issues and solutions

## What Your Friend Needs to Do

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/n8n-video-generation-setup.git
   cd n8n-video-generation-setup
   ```

2. **Follow the README.md** for complete setup instructions

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start servers**:
   ```bash
   ./scripts/start_all_servers.sh
   ```

5. **Import workflow to n8n** and configure API keys

## Repository Features

✅ **Complete Setup**: Everything needed to run video generation  
✅ **Detailed Documentation**: Step-by-step guides and troubleshooting  
✅ **Production Ready**: Error handling, health checks, logging  
✅ **Cross-Platform**: Optimized for macOS (Apple Silicon + Intel)  
✅ **Easy to Use**: One-command server startup  
✅ **Well Documented**: API reference, troubleshooting guide  

## Support

If your friend has issues:

1. **Check the troubleshooting guide**: `docs/TROUBLESHOOTING.md`
2. **Run health check**: `./scripts/health_check.sh`
3. **Follow setup guide**: `docs/SETUP_GUIDE.md`
4. **Check API reference**: `docs/API_REFERENCE.md`

---

**Note**: Make sure to replace `YOUR_USERNAME` with your actual GitHub username in all the commands above. 