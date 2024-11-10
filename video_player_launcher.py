import subprocess
import platform
import os

def launch_video(video_path):
    """
    Open a video file with the default or specific video player.
    """
    try:
        # Determine the operating system and run the video file with the appropriate player.
        if platform.system() == "Windows":
            os.startfile(video_path)  # Open with default player in Windows
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", video_path])
        else:  # Linux
            subprocess.call(["mpv", video_path])  # Open with default (xdg-open) player on Linux
    except Exception as e:
        print(f"Error al abrir el archivo de video: {e}")
