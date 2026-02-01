from moviepy import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    ColorClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
    ImageClip,
)
import os
import json
from datetime import datetime
from pexelsImageGen import getPhoto
# font_path = os.path.join("VideoMaterials", "fonts", "pjs.ttf")

# txt_clip = (
#     TextClip(font=font_path, text="Hello there!", font_size=20, color="white")
#     .with_duration(10)
#     .with_position("center")
# )


def generateVideo(clips):
    if not clips:
        raise ValueError("clips list cannot be empty")
    combined = concatenate_videoclips(clips)
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    combined.write_videofile(f"Output/result_{date}.mp4")


def audioToVideo(
    input_file,
    size,
    duration=None,
    fps=30,
    color=(0, 0, 0),
    output="color.mp4",
    segment=None,
):
    # Load audio file
    audio_file_clip = AudioFileClip(input_file)

    # Determine duration
    if segment is not None:
        duration = segment["end"] - segment["start"]
        image_clip = (
            ImageClip(getPhoto(segment["topic"])).with_duration(duration).with_fps(fps)
        )
        # Resize image to fit within size while maintaining aspect ratio
        # Calculate scaling factor to fit within target size
        target_width, target_height = size
        img_width, img_height = image_clip.size

        # Calculate scale to fit within target dimensions
        scale_w = target_width / img_width
        scale_h = target_height / img_height
        scale = min(scale_w, scale_h)  # Use smaller scale to fit within bounds

        # Resize maintaining aspect ratio
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        image_clip = image_clip.resized((new_width, new_height))

        # Center the image
        image_clip = image_clip.with_position(("center", "center"))

        # Create subclipped audio for this segment
        audio_clip = CompositeAudioClip(
            [audio_file_clip.subclipped(segment["start"], segment["end"])]
        )
        # Add audio to the image clip
        image_clip = image_clip.with_audio(audio_clip)

        # Return the clip
        return image_clip
    else:
        if duration is None:
            duration = audio_file_clip.duration
        # Use full audio
        audio_clip = CompositeAudioClip([audio_file_clip])
        # Create blank video (ColorClip doesn't accept fps parameter)
        video = ColorClip(size, color, duration=duration)
        # Set fps after creation
        video = video.with_fps(fps)
        video.audio = audio_clip
        return video


def generateEvidAiVideo(audio_file, output_keywords_file, size):
    with open(output_keywords_file, "r") as f:
        keywords_data = json.load(f)
    clips = []
    for i, segment in enumerate(keywords_data["segments_with_keywords"]):
        print(
            f"Processing Segment {i + 1} of {len(keywords_data['segments_with_keywords'])}"
        )
        clips.append(audioToVideo(audio_file, size, segment=segment))
    return generateVideo(clips)


# clip = VideoFileClip("Input/Parikrama.m4a").subclipped(0, 10).with_volume_scaled(0.8)

# final_video = CompositeVideoClip([clip, txt_clip])
# final_video.write_videofile("result.mp4")

# def createVideoFromKeywords(keywords_data):


if __name__ == "__main__":
    # TODO: Make Dimensions Configurable Later
    size = (1080, 1920)
    input_file = "Input/Parikrama.m4a"
    clips = [
        VideoFileClip("Input/Intro.MOV").with_volume_scaled(0.8),
        # generateEvidAiVideo(input_file, "Output/outputKWE.json", size),
        VideoFileClip("Input/Outro.MOV").with_volume_scaled(0.8),
    ]
    # generateVideo(clips)

    generateEvidAiVideo(input_file, "Output/outputKWE.json", size)
