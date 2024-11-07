import subprocess
import platform
import os

def launch_video(video_path):
    """
    Abrir   un archivo de video con el reproductor de video predeterminado o uno específico.
    """
    try:
        # Determina el sistema operativo y ejecuta el archivo de video con el reproductor adecuado.
        if platform.system() == "Windows":
            os.startfile(video_path)  # Abre con el reproductor predeterminado en Windows
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", video_path])
        else:  # Linux
            subprocess.call(["xdg-open", video_path])  # Abre con el reproductor predeterminado en Linux
    except Exception as e:
        print(f"Error al abrir el archivo de video: {e}")
