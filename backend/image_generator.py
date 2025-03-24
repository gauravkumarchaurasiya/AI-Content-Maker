import requests
from backend.logging_config import setup_logging
from dotenv import load_dotenv
import os
from pathlib import Path
import re

# Setup logging
logger = setup_logging(log_file='app.log')

# Load environment variables
load_dotenv()

# Get the API key for Hugging Face
HF_API_TOKEN = os.getenv('HF_API_TOKEN')

API_URL_SD = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Headers with authentication
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def extract_start_time(timestamp):
    """Extracts the start time in seconds from a timestamp string (e.g., '00:10 - 00:20')."""
    match = re.match(r"(\d{2}):(\d{2})", timestamp)
    if match:
        minutes, seconds = map(int, match.groups())
        return minutes * 60 + seconds
    return 0  # Default to 0 if parsing fails

def generate_images_from_script(script_json, output_dir):
    """Generate images for each scene based on the script JSON using Hugging Face API."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Loop through each scene and generate an image
    for i, scene in enumerate(script_json.get("scenes", [])):
        timestamp = scene.get("timestamp", "00:00") 
        start_time = extract_start_time(timestamp)  # Convert timestamp to seconds
        
        prompt = (
            f"A cinematic scene depicting {scene.get('scene_description', '')}. "
            f"The environment includes {scene.get('character_object_details', '')}. "
            f"The shot is taken using {scene.get('shot_type_camera_angle', '')} for dramatic effect. "
            f"The mood of the scene is {scene.get('mood_emotion', '')}. "
            f"Ultra-detailed, realistic, high-quality, professional lighting, dramatic composition."
        )

        # output_path = f"{output_dir}/scene_{start_time}.png"  # Save with start_time in seconds
        output_path = f"{output_dir}/scene_{i+1}.png"  # Save with start_time in seconds
        
        # Prepare the request payload
        payload = {"inputs": prompt}

        try:
            response = requests.post(API_URL_SD, headers=headers, json=payload, timeout=60)  # Added timeout
            
            # Check if the response is successful
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                logger.info(f"Image saved as {output_path}")
            else:
                logger.error(f"Error generating image for scene {i+1}: {response.json()}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for scene {i+1}: {str(e)}")
    
    logger.info("All images generated successfully.")
