#!/usr/bin/env python3
"""
Video Processor for N8N Integration
Merges video and audio files using FFmpeg
Optimized for MacBook Air M1
"""

import os
import subprocess
import json
import uuid
from flask import Flask, request, jsonify
import tempfile

app = Flask(__name__)

def merge_video_audio(video_path, audio_path, output_path):
    """Merge video and audio using FFmpeg"""
    try:
        # FFmpeg command to merge video and audio
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',  # Copy video codec
            '-c:a', 'aac',   # Use AAC audio codec
            '-shortest',      # End when shortest input ends
            '-y',             # Overwrite output file
            output_path
        ]
        
        print(f"Running FFmpeg command: {' '.join(cmd)}")
        
        # Execute FFmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False, result.stderr
        
        return True, output_path
        
    except subprocess.TimeoutExpired:
        return False, "FFmpeg timeout"
    except Exception as e:
        return False, str(e)

@app.route('/merge_video_audio', methods=['POST'])
def merge_video_audio_endpoint():
    """Merge video and audio files"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get parameters
        video_path = data.get('video_path')
        audio_path = data.get('audio_path')
        
        if not video_path or not audio_path:
            return jsonify({"error": "Video and audio paths required"}), 400
        
        if not os.path.exists(video_path):
            return jsonify({"error": "Video file not found"}), 400
        
        if not os.path.exists(audio_path):
            return jsonify({"error": "Audio file not found"}), 400
        
        # Generate output path
        output_path = f"/tmp/final_video_{uuid.uuid4()}.mp4"
        
        # Merge video and audio
        success, result = merge_video_audio(video_path, audio_path, output_path)
        
        if success:
            return jsonify({
                "success": True,
                "output_path": output_path,
                "message": "Video and audio merged successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": result
            }), 500
        
    except Exception as e:
        print(f"Error merging video and audio: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    # Check if FFmpeg is available
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        ffmpeg_available = result.returncode == 0
    except:
        ffmpeg_available = False
    
    return jsonify({
        "status": "healthy",
        "ffmpeg_available": ffmpeg_available
    })

if __name__ == '__main__':
    print("Starting Video Processor Server...")
    print("Server will be available at http://localhost:5003")
    app.run(host='::', port=5003, debug=False) 