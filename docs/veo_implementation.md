# Veo 3 Image-to-Video Implementation

## Overview
This project implements a Python client for Google's Veo 3 "Image-to-Video" generation model using the **Gemini API** with API key authentication. 
The implementation uses the `google-generativeai` library to access Veo 3 through Google AI Studio.

## Prerequisites

1.  **Gemini API Key**: Get your API key from [Google AI Studio](https://ai.google.dev)
   - Go to https://ai.google.dev
   - Sign in with your Google account
   - Click "Get API Key" and create/generate a key
   - Copy the API key (starts with `AIza...`)
2.  **Python Environment**: Python 3.8+.

## Installation

Install the required libraries:

```bash
pip install google-generativeai requests
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Configuration

### Setting up your API Key

You can set the API key in three ways:

**Option 1: Using .env file (Recommended)**
Create a `.env` file in the project root directory:
```bash
GEMINI_API_KEY=your-api-key-here
```

The code automatically loads variables from `.env` using `python-dotenv`. Make sure `.env` is in your `.gitignore` file.

**Option 2: Environment Variable**
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Windows CMD
set GEMINI_API_KEY=your-api-key-here

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

**Option 3: Direct in Code (Not Recommended)**
```python
API_KEY = "your-api-key-here"
```

⚠️ **Security Note**: Never commit your API key to version control. Use `.env` file or environment variables (and ensure `.env` is in `.gitignore`).

## Usage

The core logic is encapsulated in `veo_generator.py`.

### Basic Example

```python
from veo_generator import generate_video_from_image

# Generate video using Gemini API key
video_path = generate_video_from_image(
    api_key="your-gemini-api-key",
    image_path="path/to/image.jpg",
    prompt="A cinematic drone shot of this landscape, moving forward, 4k",
    output_file="output_video.mp4"
)
print(f"Video saved to {video_path}")
```

### Advanced Example with Custom Parameters

```python
from veo_generator import generate_video_from_image

video_path = generate_video_from_image(
    api_key="your-gemini-api-key",
    image_path="landscape.jpg",
    prompt="A slow cinematic pan from left to right, showing the mountains at sunset, 4k quality",
    output_file="sunset_video.mp4",
    model_name="veo-3.0-generate-preview",  # Veo 3 model
    aspect_ratio="16:9",                   # Video aspect ratio
    duration_seconds=8                      # Max 8 seconds for Veo 3
)
```

### Using Environment Variable

```python
import os
from veo_generator import generate_video_from_image

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

video_path = generate_video_from_image(
    api_key=api_key,
    image_path="input.jpg",
    prompt="A cinematic pan of this scene, 4k, high quality",
    output_file="output.mp4"
)
```

## API Reference

### `generate_video_from_image()`

Main function to generate video from an image.

**Parameters:**
- `api_key` (str, required): Gemini API key from Google AI Studio
- `image_path` (str, required): Path to the input image file
- `prompt` (str, required): Text description of the desired video motion/content
- `output_file` (str, optional): Output video file path (default: "output.mp4")
- `model_name` (str, optional): Veo model name (default: "veo-3.0-generate-preview")
- `aspect_ratio` (str, optional): Video aspect ratio (default: "16:9")
- `duration_seconds` (int, optional): Video duration in seconds, max 8 (default: 8)

**Returns:**
- `str`: Path to the saved video file if successful
- `None`: If generation failed

### `generate_video_from_image_rest()`

Alternative function using REST API directly (fallback method).

Same parameters as `generate_video_from_image()`.

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

## Model Information

- **Model**: Veo 3.0 (via Gemini API)
- **Max Duration**: 8 seconds
- **Supported Aspect Ratios**: 16:9, 9:16, 1:1, etc.
- **API Endpoint**: Google AI Studio / Gemini API

## Error Handling

The functions include comprehensive error handling:
- File not found errors
- API authentication errors
- Invalid response format errors
- Network errors

All errors are printed to console with full traceback for debugging.

## Troubleshooting

### Error: "API key not valid"
- Verify your API key is correct
- Check that the API key is active in Google AI Studio
- Ensure you have access to Veo 3 (may require special access)

### Error: "Model not found"
- Verify the model name is correct: `veo-3.0-generate-preview`
- Check if Veo 3 is available in your region/account

### Error: "Video not found in response"
- The API response format may have changed
- Try using the REST API method (`generate_video_from_image_rest()`)
- Check the response structure printed in the error message

### Error: "Permission denied"
- Verify your API key has access to Veo 3
- Some features may require special access or be in preview

## Reference
- [Google AI Studio](https://ai.google.dev) - Get your API key here
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google Colab: Veo 3 Video Generation](https://colab.research.google.com/github/GoogleCloudPlatform/generative-ai/blob/main/vision/getting-started/veo3_video_generation.ipynb)
