# merge_media.py

from moviepy.editor import VideoFileClip, AudioFileClip

def merge_video_audio(video_path, audio_path, output_path):
    """
    Merges a video and an audio file into one output video file.

    Parameters:
    - video_path: str, path to the input video file (e.g., "video.mp4")
    - audio_path: str, path to the input audio file (e.g., "audio.mp3")
    - output_path: str, path to the output video file (e.g., "output_video.mp4")
    
    Returns:
    None
    """
    
    # Load video and audio files
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Trim the video to match the audio length (optional)
    audio_duration = audio.duration
    video = video.subclip(0, audio_duration)

    # Set the audio of the video
    video = video.set_audio(audio)

    # Write the final video with the new audio
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
