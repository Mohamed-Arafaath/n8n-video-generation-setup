#!/bin/bash

# n8n Video Generation - Health Check Script
# This script checks if all servers are running and responding

echo "🔍 n8n Video Generation - Health Check"
echo "======================================"

# Function to check server health
check_server_health() {
    local server_name=$1
    local url=$2
    local port=$3
    
    echo "Checking $server_name..."
    
    # Check if port is in use
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "  ✅ Port $port is active"
        
        # Check HTTP response
        if curl -s "$url" > /dev/null; then
            echo "  ✅ HTTP endpoint responding"
            echo "  ✅ $server_name is healthy"
            return 0
        else
            echo "  ❌ HTTP endpoint not responding"
            echo "  ❌ $server_name has issues"
            return 1
        fi
    else
        echo "  ❌ Port $port is not in use"
        echo "  ❌ $server_name is not running"
        return 1
    fi
}

# Check all servers
echo ""
check_server_health "AnimateDiff Server" "http://localhost:5002/health" 5002
animatediff_status=$?

echo ""
check_server_health "TTS Server" "http://localhost:5001/health" 5001
tts_status=$?

echo ""
check_server_health "Video Processor Server" "http://localhost:5003/health" 5003
processor_status=$?

echo ""
echo "======================================"
echo "📊 Health Check Summary:"
echo ""

if [ $animatediff_status -eq 0 ]; then
    echo "✅ AnimateDiff Server: HEALTHY"
else
    echo "❌ AnimateDiff Server: UNHEALTHY"
fi

if [ $tts_status -eq 0 ]; then
    echo "✅ TTS Server: HEALTHY"
else
    echo "❌ TTS Server: UNHEALTHY"
fi

if [ $processor_status -eq 0 ]; then
    echo "✅ Video Processor Server: HEALTHY"
else
    echo "❌ Video Processor Server: UNHEALTHY"
fi

echo ""

# Overall status
if [ $animatediff_status -eq 0 ] && [ $tts_status -eq 0 ] && [ $processor_status -eq 0 ]; then
    echo "🎉 All servers are healthy! Ready for video generation."
else
    echo "⚠️  Some servers are unhealthy. Please check the logs and restart if needed."
    echo ""
    echo "🛠️  Troubleshooting:"
    echo "   • Run: ./scripts/stop_all_servers.sh"
    echo "   • Run: ./scripts/start_all_servers.sh"
    echo "   • Check logs for error messages"
fi 