#!/usr/bin/env python3
"""
Enhanced AnimateDiff Server for N8N Integration
Generates longer cinematic videos from images using AnimateDiff
Optimized for MacBook Air M1 with 8GB RAM
"""

import os
import json
import base64
from flask import Flask, request, jsonify
from PIL import Image
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import tempfile
import uuid
import gc

app = Flask(__name__)

# Global variables for model caching
pipe = None
device = "mps" if torch.backends.mps.is_available() else "cpu"

def load_model():
    """Load the AnimateDiff model (cached globally)"""
    global pipe
    
    if pipe is None:
        print("Loading AnimateDiff model...")
        
        # Use a smaller model for M1 MacBook with 8GB RAM
        model_id = "cerspense/zeroscope_v2_XL"
        
        pipe = DiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            variant="fp16"
        )
        
        # Optimize for M1
        if device == "mps":
            pipe = pipe.to(device)
        
        # Use faster scheduler
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        
        print("Model loaded successfully!")
    
    return pipe

def generate_long_video(pipe, prompt, image, num_frames, num_inference_steps):
    """Generate longer video by processing in chunks"""
    
    # For very long videos, process in chunks
    max_frames_per_chunk = 64  # Maximum frames per chunk for memory efficiency
    
    if num_frames <= max_frames_per_chunk:
        # Single generation for shorter videos
        with torch.no_grad():
            video_frames = pipe(
                prompt,
                image=image,
                num_inference_steps=num_inference_steps,
                num_frames=num_frames,
                guidance_scale=7.5,
                height=512,
                width=512,
            ).frames
        return video_frames
    else:
        # Chunked generation for longer videos
        all_frames = []
        chunks = (num_frames + max_frames_per_chunk - 1) // max_frames_per_chunk
        
        print(f"Generating {num_frames} frames in {chunks} chunks...")
        
        for i in range(chunks):
            start_frame = i * max_frames_per_chunk
            end_frame = min((i + 1) * max_frames_per_chunk, num_frames)
            chunk_frames = end_frame - start_frame
            
            print(f"Generating chunk {i+1}/{chunks} ({chunk_frames} frames)...")
            
            with torch.no_grad():
                chunk_result = pipe(
                    prompt,
                    image=image,
                    num_inference_steps=num_inference_steps,
                    num_frames=chunk_frames,
                    guidance_scale=7.5,
                    height=512,
                    width=512,
                ).frames
            
            all_frames.extend(chunk_result)
            
            # Clear memory after each chunk
            if device == "mps":
                torch.mps.empty_cache()
            gc.collect()
        
        return all_frames

@app.route('/generate_video', methods=['POST'])
def generate_video():
    """Generate video from image and prompt"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get parameters
        image_path = data.get('image_path')
        prompt = data.get('prompt', 'cinematic scene')
        num_frames = data.get('num_frames', 64)  # Default 64 frames = 8 seconds
        num_inference_steps = data.get('num_inference_steps', 20)  # Reduced for speed
        
        if not image_path or not os.path.exists(image_path):
            return jsonify({"error": "Image path not found"}), 400
        
        # Validate frame count
        if num_frames > 128:
            return jsonify({"error": "Maximum 128 frames allowed for memory safety"}), 400
        
        # Load the model
        pipe = load_model()
        
        # Load and prepare the image
        image = Image.open(image_path).convert("RGB")
        
        # Generate video
        print(f"Generating video with {num_frames} frames...")
        
        video_frames = generate_long_video(pipe, prompt, image, num_frames, num_inference_steps)
        
        # Save video
        output_path = f"/tmp/generated_video_{uuid.uuid4()}.mp4"
        export_to_video(video_frames, output_path, fps=8)
        
        duration_seconds = num_frames / 8
        
        return jsonify({
            "success": True,
            "video_path": output_path,
            "num_frames": num_frames,
            "duration_seconds": duration_seconds,
            "fps": 8
        })
        
    except Exception as e:
        print(f"Error generating video: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "device": device})

if __name__ == '__main__':
    print("Starting Enhanced AnimateDiff Server...")
    print(f"Using device: {device}")
    print("Server will be available at http://localhost:5002")
    print("Supports videos up to 128 frames (16 seconds)")
    app.run(host='::', port=5002, debug=False) 