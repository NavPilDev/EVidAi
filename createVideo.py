from moviepy import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
    ImageClip,
)
import json
from datetime import datetime
from pexelsImageGen import getPhoto
from PIL import Image


# -------------------------
# Video Concatenation
# -------------------------
def generateVideo(clips):
    if not clips:
        raise ValueError("clips list cannot be empty")

    combined = concatenate_videoclips(clips, method="compose")
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    combined.write_videofile(
        f"Output/result_{date}.mp4",
        codec="libx264",
        preset="ultrafast",
        threads=8,
        fps=30,
    )


# -------------------------
# Audio → Video Segment
# -------------------------
def audioToVideo(
    input_file,
    size,
    fps=30,
    color=(0, 0, 0),
    segment=None,
):
    audio_file_clip = AudioFileClip(input_file)

    if segment is None:
        raise ValueError("segment is required")

    duration = segment["end"] - segment["start"]
    image_path = getPhoto(segment["topic"])

    # ---- Bake background + centered image using PIL ----
    with Image.open(image_path).convert("RGB") as img:
        img_width, img_height = img.size
        bg_width, bg_height = size

        scale = min(bg_width / img_width, bg_height / img_height)
        new_size = (int(img_width * scale), int(img_height * scale))
        img = img.resize(new_size, Image.LANCZOS)

        # Create background
        background = Image.new("RGB", size, color)

        # Center position
        x = (bg_width - new_size[0]) // 2
        y = (bg_height - new_size[1]) // 2

        background.paste(img, (x, y))

        baked_path = image_path.replace(".jpeg", "_baked.jpeg")
        background.save(baked_path, quality=95)

    # ---- ONE flat ImageClip (fast) ----
    video = ImageClip(baked_path).with_duration(duration).with_fps(fps)

    video.audio = audio_file_clip.subclipped(segment["start"], segment["end"])

    return video


# -------------------------
# Keyword-driven generation
# -------------------------
def generateEvidAiVideo(audio_file, output_keywords_file, size):
    with open(output_keywords_file, "r") as f:
        keywords_data = json.load(f)

    clips = []
    segments = keywords_data["segments_with_keywords"]

    for i, segment in enumerate(segments):
        print(f"Processing Segment {i + 1} of {len(segments)}")
        clips.append(audioToVideo(audio_file, size, segment=segment))

    return clips


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    size = (1080, 1920)
    input_file = "Input/Parikrama.m4a"

    clips = [
        VideoFileClip("Input/Intro.MOV").with_volume_scaled(0.8),
        *generateEvidAiVideo(input_file, "Output/outputKWE.json", size),
        VideoFileClip("Input/Outro.MOV").with_volume_scaled(0.8),
    ]

    generateVideo(clips)
