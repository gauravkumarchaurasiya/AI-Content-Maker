from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from pathlib import Path
import json
from backend.text_generator import generate_video_script, extract_json, save_json
from backend.image_generator import generate_images_from_script
from backend.audio_generator import generate_audio
from backend.music_generator import generate_music, generate_music_prompt
from backend.video_generator import create_final_video,apply_ken_burns
from backend.logging_config import setup_logging
from fastapi.staticfiles import StaticFiles

# Setup logger
logger = setup_logging(log_file='app.log')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Directories for storing outputs
current_path = Path(__file__).resolve()
root_path = current_path.parent.parent
output_data_dir = root_path / 'output/video4'

# Ensure output directories exist
output_data_dir.mkdir(parents=True, exist_ok=True)
images_output_dir = output_data_dir / 'output_images'
audio_output_dir = output_data_dir / 'output_audio'
music_output_dir = output_data_dir / 'output_music'

@app.post("/generate_video/")
async def generate_video(topic: str = Form(...)):
    try:
        # Generate the video script
        # response_text = generate_video_script(topic)
        # video_script = extract_json(response_text)
        
        # # Save the generated script to a JSON file
        # save_json(video_script, output_data_dir)

        # Read the saved video script
        json_file = output_data_dir / "video_script.json"
        with json_file.open("r", encoding="utf-8") as file:
            script = json.load(file)
        
        # Generate images from the script
        # generate_images_from_script(script, images_output_dir)

        # Generate audio from the script
        # generate_audio(script, audio_output_dir)

        # Generate background music based on the script
        # music_prompt = generate_music_prompt(script["background_music_prompt"], script["scenes"], script["overall_video_mood"])
        # generate_music(music_prompt, music_output_dir)

        # Create the final video using the generated script, images, audio, and music
        final_video_path = output_data_dir / "final_video.mp4"
        create_final_video(script, str(images_output_dir), str(audio_output_dir), str(music_output_dir/"background_music.flac"), str(final_video_path))

        # Return the generated video file as a response
        return FileResponse(final_video_path, media_type="video/mp4")

    except Exception as e:
        logger.error(f"Error generating video: {e}")
        return {"error": str(e)}

@app.get("/")
async def root():
    return FileResponse("static/index.html")
