# n8n Video Generation Setup

A complete setup for self-hosting n8n with AI-powered video generation capabilities. This repository contains all the prerequisites and servers needed to create cinematic videos with voice-over audio using n8n workflows.

## 🎯 What This Setup Provides

- **AnimateDiff Server**: Generates cinematic videos from text prompts
- **TTS Server**: Converts text to speech for voice-over audio
- **Video Processor**: Merges video and audio into final videos
- **n8n Workflows**: Complete workflow templates for video generation
- **Google Drive Integration**: Automatic upload of final videos

## 🚀 Quick Start

### Prerequisites
- macOS with Apple Silicon (M1/M2/M3) or Intel Mac
- Python 3.9+ installed
- Git installed
- At least 8GB RAM (16GB recommended)
- 20GB+ free disk space

### Installation Steps

1. **Clone this repository**
   ```bash
   git clone <your-repo-url>
   cd n8n-video-generation-setup
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start all servers**
   ```bash
   ./scripts/start_all_servers.sh
   ```

4. **Import n8n workflow**
   - Open n8n in your browser
   - Import the workflow from `workflows/comprehensive-video-workflow.json`

## 📁 Repository Structure

```
n8n-video-generation-setup/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── servers/                           # Flask servers
│   ├── animatediff_server.py          # Video generation server
│   ├── tts_server.py                  # Text-to-speech server
│   └── video_processor.py             # Video processing server
├── workflows/                         # n8n workflow templates
│   ├── comprehensive-video-workflow.json
│   └── simple-video-workflow.json
├── scripts/                           # Utility scripts
│   ├── start_all_servers.sh
│   ├── install_dependencies.sh
│   └── health_check.sh
└── docs/                             # Detailed documentation
    ├── SETUP_GUIDE.md
    ├── API_REFERENCE.md
    └── TROUBLESHOOTING.md
```

## 🔧 Detailed Setup Guide

### Step 1: Environment Setup

1. **Install Python 3.9+**
   ```bash
   # Check if Python is installed
   python3 --version
   
   # If not installed, download from python.org
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Server Setup

Each server runs on a different port and handles specific functionality:

- **AnimateDiff Server** (Port 5002): Generates videos from text prompts
- **TTS Server** (Port 5001): Converts text to speech
- **Video Processor** (Port 5003): Merges video and audio

Start all servers:
```bash
./scripts/start_all_servers.sh
```

### Step 3: n8n Setup

1. **Install n8n**
   ```bash
   npm install -g n8n
   ```

2. **Start n8n**
   ```bash
   n8n start
   ```

3. **Import workflow**
   - Open http://localhost:5678
   - Import workflow from `workflows/comprehensive-video-workflow.json`

## 🎬 How It Works

### Video Generation Process

1. **Trigger**: Chat message or manual trigger starts the workflow
2. **Story Generation**: AI creates a cinematic story prompt
3. **Image Generation**: Freepik API generates base image
4. **Video Creation**: AnimateDiff converts image to video
5. **Audio Generation**: TTS creates voice-over audio
6. **Video Processing**: Merge video and audio
7. **Upload**: Final video uploaded to Google Drive

### Server Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   n8n Workflow  │    │  AnimateDiff    │    │     TTS         │
│                 │    │    Server       │    │   Server        │
│  - Triggers     │───▶│  - Port 5002    │    │  - Port 5001    │
│  - Orchestrates │    │  - Video Gen    │    │  - Audio Gen    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Video Proc    │
                    │    Server       │
                    │  - Port 5003    │
                    │  - Merge A/V    │
                    └─────────────────┘
```

## 🔑 API Keys Required

You'll need to configure these API keys in your n8n workflow:

- **Freepik API**: For image generation
- **Google Drive API**: For video upload
- **OpenAI API** (optional): For enhanced story generation

## 📊 Performance Notes

- **Video Generation**: 30-60 seconds per video
- **Audio Generation**: 5-10 seconds per audio
- **Video Processing**: 10-20 seconds per merge
- **Total Time**: 1-2 minutes per complete video

## 🛠️ Troubleshooting

### Common Issues

1. **Port conflicts**: Kill existing processes on ports 5001, 5002, 5003
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Memory issues**: Close other applications, ensure 8GB+ RAM
4. **GPU issues**: Ensure PyTorch is installed with MPS support

### Health Checks

Test all servers are running:
```bash
curl http://localhost:5001/health  # TTS Server
curl http://localhost:5002/health  # AnimateDiff Server
curl http://localhost:5003/health  # Video Processor
```

## 📚 Additional Resources

- [Detailed Setup Guide](docs/SETUP_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Video Length Guide](docs/VIDEO_LENGTH_GUIDE.md)

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This setup is optimized for macOS with Apple Silicon. For other platforms, some modifications may be required. 