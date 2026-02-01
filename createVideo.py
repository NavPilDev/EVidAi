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
    combined.write_videofile("output/result.mp4")


def audioToVideo(
    input_file, size, duration=None, fps=30, color=(0, 0, 0), output="color.mp4"
):
    if duration is None:
        duration = AudioFileClip(input_file).duration
    blank_video = ColorClip(size, color, duration=duration)
    audio_clip = CompositeAudioClip([AudioFileClip(input_file)])

    blank_video.audio = audio_clip

    return blank_video


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
        audioToVideo(input_file, size),
        VideoFileClip("Input/Outro.MOV").with_volume_scaled(0.8),
    ]
    generateVideo(clips)
