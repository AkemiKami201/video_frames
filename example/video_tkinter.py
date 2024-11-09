'''
using cv2 and numpy to play video, but it's not good
so don't use this
'''

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

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame")
        self.root.geometry("1270x720")
        self.root.bind("<Configure>", self.resize_video)

        # Framework for controls
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        # Control buttons
        self.open_button = tk.Button(control_frame, text="Load video", command=self.open_file)
        self.open_button.grid(row=0, column=0, padx=5)

        self.play_pause_button = tk.Button(control_frame, text="Pause", command=self.toggle_play_pause, state="disabled")
        self.play_pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_video, state="disabled")
        self.stop_button.grid(row=0, column=2, padx=5)

        self.skip_button = tk.Button(control_frame, text="Skip Forward 10s", command=self.skip_forward, state="disabled")
        self.skip_button.grid(row=0, column=3, padx=5)

        # Label where the video is display
        self.label = tk.Label(self.root)
        self.label.pack(fill=tk.BOTH, expand=True)

        # Variables for video and audio
        self.cap = None
        self.stop = False
        self.paused = False
        self.video_thread = None
        self.audio_thread = None
        self.audio = None
        self.audio_stream = None
        self.frame_width = 640
        self.frame_height = 480
        
    def open_file(self):
        # select the file
        file_path = filedialog.askopenfilename(filetypes=[("Video File", "*.mp4 *.avi *.mov *.mkv")])
        if file_path:
            # Stop any current playback
            self.stop_video()
            self.cap = cv2.VideoCapture(file_path)
            self.audio = AudioSegment.from_file(file_path)
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.stop = False
            self.paused = False

            # Activate the control buttons
            self.play_pause_button.config(state="normal", text="Pause")
            self.stop_button.config(state="normal")
            self.skip_button.config(state="normal")
                        
            # Start the video, audio and frame capture threads
            self.video_thread = threading.Thread(target=self.play_video)
            self.audio_thread = threading.Thread(target=self.play_audio)
            self.frame_thread = threading.Thread(target=FrameCapture, args=(file_path,))
            self.video_thread.start()
            self.audio_thread.start()
            self.frame_thread.start()
            
    def play_video(self):
        while not self.stop and self.cap.isOpened():
            if self.paused:
                continue

            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame, (self.label.winfo_width(), self.label.winfo_height()))
            image = Image.fromarray(frame_resized)
            photo = ImageTk.PhotoImage(image)

            self.label.config(image=photo)
            self.label.image = photo
            self.label.after(1)

        self.cap.release()

    def play_audio(self):
        p = pyaudio.PyAudio()
        self.audio_stream = p.open(format=p.get_format_from_width(self.audio.sample_width),
                                   channels=self.audio.channels,
                                   rate=self.audio.frame_rate,
                                   output=True)
        
        # Convert audio to bytes and play
        audio_data = np.array(self.audio.get_array_of_samples())
        self.audio_stream.write(audio_data.tobytes())
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        p.terminate()
        
    def toggle_play_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.play_pause_button.config(text="Resume")
        else:
            self.play_pause_button.config(text="Pause")
            
    def stop_video(self):
        self.stop = True
        self.paused = False
        if self.cap:
            self.cap.release()
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

        self.play_pause_button.config(state="disabled", text="Pause")
        self.stop_button.config(state="disabled")
        self.skip_button.config(state="disabled")

    def skip_forward(self):
        if self.cap:
            # Get current position in milliseconds
            current_pos = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            # Fast forward 5 seconds
            self.cap.set(cv2.CAP_PROP_POS_MSEC, current_pos + 5000)

    def resize_video(self, event):
        # Function to update video size based on window size
        self.frame_width = event.width
        self.frame_height = event.height

    def on_closing(self):
        self.stop_video()
        self.root.destroy()

# Setting up the main window
root = tk.Tk()
app = VideoPlayer(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()