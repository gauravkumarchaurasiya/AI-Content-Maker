from backend.logging_config import setup_logging
from backend.text_generator import generate_video_script,extract_json,save_json
from pathlib import Path
import json
from backend.image_generator import generate_images_from_script
from backend.video_generator import *
from backend.audio_generator import generate_audio
from backend.music_generator import generate_music,generate_music_prompt
logger = setup_logging(log_file='app.log')




# def main():

#     #TEXT
#     current_path = Path(__file__)
#     root_path = current_path.parent.parent
#     output_data_dir = root_path/'output/video'
#     output_data_dir.mkdir(parents=True,exist_ok=True)
#     # topic = input("Enter topic : ")
#     # response_text  = generate_video_script(topic)
#     # video_script = extract_json(response_text)
#     # save_json(video_script,output_data_dir)
    
#     json_file = output_data_dir/"video_script.json"
#     with json_file.open("r", encoding="utf-8") as file:
#         script = json.load(file)
        
#     images_output_dir = output_data_dir / "output_images"
#     # generate_images_from_script(script,images_output_dir)
    
#     audio_output_dir = output_data_dir / "output_audio"
#     # generate_audio(script,audio_output_dir)
    
#     music_output_dir = output_data_dir / "output_music"
#     music_prompt = generate_music_prompt(script["background_music_prompt"],script["scenes"],script["overall_video_mood"])
#     # generate_music(music_prompt,music_output_dir)
#     # Generate the final video
#     create_final_video(script, f"{images_output_dir}",f"{ audio_output_dir}", f"{music_output_dir}/background_music.mp3", f'{output_data_dir}/"final_video.mp4"')
    
    
   
# if __name__=='__main__':
#     main()
        
    
import os
import re
from backend.logging_config import setup_logging
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from pathlib import Path
import json
from backend.text_generator import generate_video_script, extract_json, save_json
from backend.image_generator import generate_images_from_script
from backend.audio_generator import generate_audio
from backend.music_generator import generate_music, generate_music_prompt
from backend.video_generator import create_final_video,get_closest_file
from backend.logging_config import setup_logging
from fastapi.staticfiles import StaticFiles
import moviepy.editor as mp

logger = setup_logging(log_file='app.log')



import json
from pathlib import Path
current_path = Path(__file__).resolve()
root_path = current_path.parent.parent
output_data_dir = root_path / 'output/video4'
output_data_dir.mkdir(parents=True, exist_ok=True)
images_output_dir = output_data_dir / 'output_images'
audio_output_dir = output_data_dir / 'output_audio'
music_output_dir = output_data_dir / 'output_music'
json_file = output_data_dir / "video_script.json"
with json_file.open("r", encoding="utf-8") as file:
    script = json.load(file)   
final_video_path = output_data_dir / "final_video.mp4"
create_final_video(script, str(images_output_dir), str(audio_output_dir), str(music_output_dir/"background_music.mp3"), str(final_video_path))