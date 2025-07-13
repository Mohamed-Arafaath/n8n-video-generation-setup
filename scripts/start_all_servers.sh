#!/bin/bash

# n8n Video Generation - Start All Servers Script
# This script starts all three servers needed for video generation

echo "🚀 Starting n8n Video Generation Servers..."
echo "=============================================="

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use. Killing existing process..."
        lsof -ti:$port | xargs kill -9
        sleep 2
    fi
}

# Function to start server with error handling
start_server() {
    local server_name=$1
    local script_path=$2
    local port=$3
    
    echo "Starting $server_name on port $port..."
    
    # Check if port is in use
    check_port $port
    
    # Start server in background
    python3 "$script_path" &
    local pid=$!
    
    # Wait a moment and check if server started successfully
    sleep 3
    if curl -s "http://localhost:$port/health" > /dev/null; then
        echo "✅ $server_name started successfully (PID: $pid)"
    else
        echo "❌ Failed to start $server_name"
        return 1
    fi
}

# Change to the repository directory
cd "$(dirname "$0")/.."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import flask, torch, diffusers, gtts" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies are missing. Installing..."
    pip install -r requirements.txt
fi

# Start servers
echo ""
echo "🎬 Starting AnimateDiff Server (Video Generation)..."
start_server "AnimateDiff Server" "servers/enhanced_animatediff_server.py" 5002

echo ""
echo "🎵 Starting TTS Server (Text-to-Speech)..."
start_server "TTS Server" "servers/tts_server.py" 5001

echo ""
echo "🎞️  Starting Video Processor Server (Video/Audio Merge)..."
start_server "Video Processor Server" "servers/video_processor.py" 5003

echo ""
echo "=============================================="
echo "🎉 All servers started successfully!"
echo ""
echo "📊 Server Status:"
echo "   • AnimateDiff Server: http://localhost:5002"
echo "   • TTS Server: http://localhost:5001"
echo "   • Video Processor: http://localhost:5003"
echo ""
echo "🔍 Health Check URLs:"
echo "   • curl http://localhost:5002/health"
echo "   • curl http://localhost:5001/health"
echo "   • curl http://localhost:5003/health"
echo ""
echo "📝 Next Steps:"
echo "   1. Start n8n: n8n start"
echo "   2. Open http://localhost:5678"
echo "   3. Import workflow from workflows/comprehensive-video-workflow.json"
echo ""
echo "🛑 To stop all servers: ./scripts/stop_all_servers.sh" 