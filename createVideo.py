from moviepy import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    ColorClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)
import os
import json
from datetime import datetime
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
        # Create subclipped audio for this segment
        audio_clip = CompositeAudioClip(
            [audio_file_clip.subclipped(segment["start"], segment["end"])]
        )
    else:
        if duration is None:
            duration = audio_file_clip.duration
        # Use full audio
        audio_clip = CompositeAudioClip([audio_file_clip])

    # Create blank video (ColorClip doesn't accept fps parameter)
    blank_video = ColorClip(size, color, duration=duration)
    # Set fps after creation
    blank_video = blank_video.with_fps(fps)

    blank_video.audio = audio_clip

    return blank_video


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
