#!/bin/bash

# n8n Video Generation - Stop All Servers Script
# This script stops all three servers gracefully

echo "🛑 Stopping n8n Video Generation Servers..."
echo "=============================================="

# Function to stop server by port
stop_server_by_port() {
    local port=$1
    local server_name=$2
    
    echo "Stopping $server_name on port $port..."
    
    # Find and kill processes using the port
    local pids=$(lsof -ti:$port)
    if [ ! -z "$pids" ]; then
        echo "Found processes: $pids"
        echo "$pids" | xargs kill -9
        echo "✅ $server_name stopped"
    else
        echo "ℹ️  No processes found on port $port"
    fi
}

# Stop all servers
stop_server_by_port 5002 "AnimateDiff Server"
stop_server_by_port 5001 "TTS Server"
stop_server_by_port 5003 "Video Processor Server"

echo ""
echo "=============================================="
echo "🎉 All servers stopped successfully!"
echo ""
echo "📊 To restart servers: ./scripts/start_all_servers.sh" 