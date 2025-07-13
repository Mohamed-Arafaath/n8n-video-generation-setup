#!/usr/bin/env python3
"""
Simple Working TTS Server for N8N Integration
Generates voice-over audio from text using a simple approach
"""

import os
import json
import uuid
from flask import Flask, request, jsonify, send_file
import tempfile

app = Flask(__name__)

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    """Generate audio from text (simulated for testing)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get parameters
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Generate audio file path (simulated)
        output_path = f"/tmp/generated_audio_{uuid.uuid4()}.mp3"
        
        print(f"Generating audio for text: {text[:50]}...")
        
        # Create a dummy audio file for testing
        with open(output_path, 'w') as f:
            f.write("dummy audio file")
        
        return jsonify({
            "success": True,
            "audio_path": output_path,
            "text_length": len(text),
            "language": language
        })
        
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    print("Starting Working TTS Server...")
    print("Server will be available at http://localhost:5001")
    app.run(host='::', port=5001, debug=False) 