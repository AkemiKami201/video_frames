import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import threading
from pydub import AudioSegment
import pyaudio
import numpy as np
import os
from video_to_frames import FrameCapture
from video_player_launcher import launch_video

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame")
        self.root.geometry("300x100")

        # Botón para seleccionar y abrir el archivo de video
        self.open_button = tk.Button(root, text="Select and play video", command=self.open_and_play_video)
        self.open_button.pack(pady=20)

    def open_and_play_video(self):
        # Selección del archivo
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")])
        if file_path:
            launch_video(file_path)  # Llama a la función para lanzar el video en el reproductor predeterminado
            FrameCapture(file_path) # extract frames of this file

# Setting up the main window
root = tk.Tk()
app = VideoPlayer(root)
root.protocol("WM_DELETE_WINDOW")
root.mainloop()
