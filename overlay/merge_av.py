from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.video.fx.all as vfx
from pathlib import Path
import os

def merge_video_audio(context):
    """
    Merges a video and an audio file into one output video file.

    Parameters:
    - video_path: str, path to the input video file (e.g., "video.mp4")
    - audio_path: str, path to the input audio file (e.g., "audio.mp3")
    - output_path: str, path to the output video file (e.g., "output_video.mp4")
    
    Returns:
    None
    """

    if not context.get('video_path') or not context.get('audio_path') or not context.get('request_id'):
        raise ValueError("Missing video_path or audio_path or request_id in context")
    
    video_path = context.get('video_path')
    audio_path = context.get('audio_path')
    
    # Load video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    audio_duration = audio.duration
    video_duration = video.duration
    speed_factor = video_duration / audio_duration
    video = video.fx(vfx.speedx, speed_factor)

    # Set the audio of the video
    video = video.set_audio(audio)

    Path("./output").mkdir(parents=True, exist_ok=True)
    final_video_path = f"./output/output_video_{context.get('request_id')}.mp4"
    
    # Write the final video with the new audio
    video.write_videofile(final_video_path, codec="libx264", audio_codec="aac")

    served_video_path = f"http://127.0.0.1:8080/output_video_{context.get('request_id')}.mp4"
    context['final_video_path'] = served_video_path
