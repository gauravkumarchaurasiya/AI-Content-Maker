import re
import os
import random
import moviepy.editor as mp
from moviepy.video.fx import fadein, fadeout
from moviepy.video.fx.resize import resize
from moviepy.video.fx.all import resize, crop
from backend.logging_config import setup_logging


logger = setup_logging(log_file='app.log')

def get_closest_file(folder, start_time, prefix, extension):
    """Find the closest matching file (image or audio) based on the scene number."""
    files = os.listdir(folder)

    file_numbers = []
    for f in files:
        match = re.search(rf"{prefix}_(\d+)\.{extension}$", f)
        if match:
            file_numbers.append(int(match.group(1)))  # Convert matched number to int

    if not file_numbers:
        logger.warning(f"No matching files found in {folder} for {prefix} with {extension} extension.")
        return None  # No matching files found

    # Find the closest scene number to the start_time
    closest_scene = min(file_numbers, key=lambda x: abs(x - start_time))
    
    return os.path.join(folder, f"{prefix}_{closest_scene}.{extension}")



def apply_ken_burns(image_clip):
    """Apply a random Ken Burns effect (zoom or pan)."""
    w, h = image_clip.size  # Get image width & height
    
    # Randomly select an effect
    effects = ["in", "out", "left", "right", "up", "down", None]  # `None` for no effect
    chosen_effect = random.choice(effects)
    
    zoom_factor = random.uniform(1.05, 1.2)  # Random zoom factor between 1.05x and 1.2x
    
    # Apply Zoom Effect
    if chosen_effect == "in":
        zoom_clip = resize(image_clip, lambda t: 1 + (zoom_factor - 1) * (t / image_clip.duration))
    elif chosen_effect == "out":
        zoom_clip = resize(image_clip, lambda t: zoom_factor - (zoom_factor - 1) * (t / image_clip.duration))
    else:
        zoom_clip = image_clip  # No zoom

    # Apply Pan Effect
    if chosen_effect == "left":
        pan_clip = crop(zoom_clip, x1=lambda t: (t / zoom_clip.duration) * w * 0.1, width=w, height=h)
    elif chosen_effect == "right":
        pan_clip = crop(zoom_clip, x1=lambda t: w * 0.1 - (t / zoom_clip.duration) * w * 0.1, width=w, height=h)
    elif chosen_effect == "up":
        pan_clip = crop(zoom_clip, y1=lambda t: (t / zoom_clip.duration) * h * 0.1, width=w, height=h)
    elif chosen_effect == "down":
        pan_clip = crop(zoom_clip, y1=lambda t: h * 0.1 - (t / zoom_clip.duration) * h * 0.1, width=w, height=h)
    else:
        pan_clip = zoom_clip  # No pan
    
    return pan_clip


def create_final_video(script_data, images_folder, voiceover_folder, bg_music_path, output_video_path):
    """Creates the final video using generated images, voiceovers, and background music."""

    clips = []  # List to store video clips

    for idx, scene in enumerate(script_data["scenes"]):
        timestamp = scene["timestamp"]
        start_time, end_time = map(lambda x: int(x.split(":")[1]), timestamp.split(" - "))
        duration = end_time - start_time
        img_path = os.path.join(images_folder, f"scene_{idx+1}.png")
        audio_path = os.path.join(voiceover_folder, f"scene_{idx+1}.mp3")

        if not os.path.exists(img_path):
            print(f"Warning: Missing image {img_path}, skipping scene.")
            continue

        if not os.path.exists(audio_path):
            print(f"Warning: Missing voiceover {audio_path}, skipping scene.")
            continue

        # Load the image and voiceover
        # img_clip = mp.ImageClip(img_path)
        img_clip = mp.ImageClip(img_path).set_duration(duration)
        img_clip = apply_ken_burns(img_clip)
        audio_clip = mp.AudioFileClip(audio_path)

        # Set duration of the image clip to match the audio length
        img_clip = img_clip.set_duration(audio_clip.duration).set_audio(audio_clip)

        # Apply transition effects based on script
        transition = scene.get("suggested_transition_effect", "fade-in").lower()
        if transition == "fade-in":
            img_clip = fadein.fadein(img_clip, 1)  # 1-second fade-in
        elif transition == "crossfade":
            img_clip = fadeout.fadeout(img_clip, 1).fx(fadein.fadein, 1)  # Smooth fade transition
        elif transition == "zoom out":
            img_clip = resize.resize(img_clip, lambda t: 1 + 0.05 * t)  # Zoom-out effect
        elif transition == "quick cuts":
            img_clip = fadeout.fadeout(img_clip, 0.5)  # Quick fade-out

        clips.append(img_clip)

    if not clips:
        raise ValueError("No valid video clips created. Check if images and audio exist.")

    # Merge all clips into a single video
    final_video = mp.concatenate_videoclips(clips, method="compose")

    # Add background music if available
    if os.path.exists(bg_music_path):
        bg_music = mp.AudioFileClip(bg_music_path).volumex(0.3)  # Reduce music volume
        final_audio = mp.CompositeAudioClip([final_video.audio, bg_music])
        final_video = final_video.set_audio(final_audio)

    # Export final video
    final_video.write_videofile(output_video_path, fps=24, codec="libx264", audio_codec="aac")
