# API Reference

This document provides detailed information about all the APIs and endpoints used in the n8n video generation setup.

## Server Overview

The setup consists of three main Flask servers, each handling a specific aspect of video generation:

1. **AnimateDiff Server** (Port 5002): Video generation from text prompts
2. **TTS Server** (Port 5001): Text-to-speech conversion
3. **Video Processor Server** (Port 5003): Video and audio merging

## AnimateDiff Server

**Base URL**: `http://localhost:5002`

### Endpoints

#### GET `/health`
Check server health status.

**Response**:
```json
{
  "status": "healthy",
  "device": "mps",
  "max_frames": 128,
  "max_duration": "16 seconds"
}
```

#### POST `/generate_video`
Generate a video from a text prompt.

**Request Body**:
```json
{
  "prompt": "A cinematic scene of a sunset over mountains",
  "num_frames": 64,
  "guidance_scale": 7.5,
  "num_inference_steps": 20
}
```

**Parameters**:
- `prompt` (string, required): Text description of the video
- `num_frames` (integer, optional): Number of frames (16-128, default: 64)
- `guidance_scale` (float, optional): Guidance scale for generation (1-20, default: 7.5)
- `num_inference_steps` (integer, optional): Number of inference steps (10-50, default: 20)

**Response**:
```json
{
  "status": "success",
  "video_path": "/tmp/generated_video_123456.mp4",
  "duration": "8 seconds",
  "frames": 64,
  "prompt": "A cinematic scene of a sunset over mountains"
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "Invalid prompt provided",
  "error_code": "INVALID_PROMPT"
}
```

### Usage Example
```bash
curl -X POST http://localhost:5002/generate_video \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over the ocean",
    "num_frames": 48,
    "guidance_scale": 8.0
  }'
```

## TTS Server

**Base URL**: `http://localhost:5001`

### Endpoints

#### GET `/health`
Check server health status.

**Response**:
```json
{
  "status": "healthy",
  "available_languages": ["en", "es", "fr", "de", "it"],
  "default_language": "en"
}
```

#### POST `/generate_audio`
Convert text to speech.

**Request Body**:
```json
{
  "text": "Welcome to our cinematic video generation system",
  "language": "en",
  "slow": false
}
```

**Parameters**:
- `text` (string, required): Text to convert to speech
- `language` (string, optional): Language code (default: "en")
- `slow` (boolean, optional): Slow speech rate (default: false)

**Response**:
```json
{
  "status": "success",
  "audio_path": "/tmp/generated_audio_123456.mp3",
  "duration": "3.2 seconds",
  "text": "Welcome to our cinematic video generation system",
  "language": "en"
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "Text too long for processing",
  "error_code": "TEXT_TOO_LONG"
}
```

### Usage Example
```bash
curl -X POST http://localhost:5001/generate_audio \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a beautiful cinematic video",
    "language": "en",
    "slow": false
  }'
```

## Video Processor Server

**Base URL**: `http://localhost:5003`

### Endpoints

#### GET `/health`
Check server health status.

**Response**:
```json
{
  "status": "healthy",
  "supported_formats": ["mp4", "avi", "mov"],
  "max_video_size": "100MB"
}
```

#### POST `/merge_video_audio`
Merge video and audio files into a single video.

**Request Body**:
```json
{
  "video_path": "/tmp/generated_video_123456.mp4",
  "audio_path": "/tmp/generated_audio_123456.mp3",
  "output_format": "mp4",
  "video_codec": "libx264",
  "audio_codec": "aac"
}
```

**Parameters**:
- `video_path` (string, required): Path to video file
- `audio_path` (string, required): Path to audio file
- `output_format` (string, optional): Output format (default: "mp4")
- `video_codec` (string, optional): Video codec (default: "libx264")
- `audio_codec` (string, optional): Audio codec (default: "aac")

**Response**:
```json
{
  "status": "success",
  "output_path": "/tmp/final_video_123456.mp4",
  "duration": "8.5 seconds",
  "file_size": "15.2 MB",
  "resolution": "512x512"
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "Video file not found",
  "error_code": "VIDEO_NOT_FOUND"
}
```

### Usage Example
```bash
curl -X POST http://localhost:5003/merge_video_audio \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "/tmp/video.mp4",
    "audio_path": "/tmp/audio.mp3",
    "output_format": "mp4"
  }'
```

## Error Codes

### AnimateDiff Server Errors
- `INVALID_PROMPT`: Prompt is empty or invalid
- `TOO_MANY_FRAMES`: Requested frame count exceeds limit
- `GENERATION_FAILED`: Video generation failed
- `MODEL_LOAD_ERROR`: Model failed to load

### TTS Server Errors
- `TEXT_TOO_LONG`: Text exceeds maximum length
- `INVALID_LANGUAGE`: Unsupported language code
- `AUDIO_GENERATION_FAILED`: Audio generation failed
- `INVALID_TEXT`: Text contains invalid characters

### Video Processor Errors
- `VIDEO_NOT_FOUND`: Video file doesn't exist
- `AUDIO_NOT_FOUND`: Audio file doesn't exist
- `MERGE_FAILED`: Video/audio merge failed
- `INVALID_FORMAT`: Unsupported output format

## Performance Guidelines

### AnimateDiff Server
- **Recommended frame count**: 32-64 frames
- **Generation time**: 30-60 seconds per video
- **Memory usage**: 4-8GB RAM
- **GPU acceleration**: MPS (Apple Silicon) or CUDA

### TTS Server
- **Text length limit**: 5000 characters
- **Generation time**: 5-10 seconds per audio
- **Memory usage**: 1-2GB RAM
- **Supported languages**: English, Spanish, French, German, Italian

### Video Processor Server
- **Video size limit**: 100MB
- **Processing time**: 10-20 seconds per merge
- **Memory usage**: 2-4GB RAM
- **Supported formats**: MP4, AVI, MOV

## Security Considerations

### Input Validation
- All servers validate input parameters
- File paths are sanitized
- Text content is checked for malicious patterns

### File Management
- Temporary files are automatically cleaned up
- File size limits are enforced
- Supported formats are validated

### Rate Limiting
- Consider implementing rate limiting for production use
- Monitor server resources during high load

## Monitoring

### Health Checks
```bash
# Check all servers
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
```

### Log Monitoring
```bash
# Monitor server logs
tail -f animatediff.log
tail -f tts.log
tail -f processor.log
```

### Performance Metrics
- Response times
- Memory usage
- CPU usage
- Error rates

## Integration with n8n

### HTTP Request Nodes
Use n8n's HTTP Request nodes to interact with the servers:

1. **AnimateDiff Node**:
   - Method: POST
   - URL: `http://localhost:5002/generate_video`
   - Body: JSON with prompt and parameters

2. **TTS Node**:
   - Method: POST
   - URL: `http://localhost:5001/generate_audio`
   - Body: JSON with text and language

3. **Video Processor Node**:
   - Method: POST
   - URL: `http://localhost:5003/merge_video_audio`
   - Body: JSON with video and audio paths

### Error Handling
- Check response status in n8n workflows
- Implement retry logic for failed requests
- Log errors for debugging

---

**Note**: All servers are designed for local development. For production use, implement proper security measures, authentication, and monitoring. 