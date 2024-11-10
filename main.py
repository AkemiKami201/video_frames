"""
-| 
-| Code by Akemi201
-| 
"""

import tkinter as tk
from tkinter import filedialog
from video_to_frames import FrameCapture
import customtkinter
from video_player_launcher import launch_video

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame")
        self.root.geometry("500x220")
        self.root.configure(bg="#f59ee5")

        # Button to select and open the video file
        Button_select = customtkinter.CTkButton(
            master=self.root,
            text="Select and play video",
            font=("undefined", 15),
            text_color="#ffffff",
            hover=True,
            hover_color="none",
            height=40,
            width=100,
            border_width=2,
            corner_radius=7,
            border_color="#750000",
            bg_color="#ffffff",
            fg_color="#7c66ea",
            command=self.open_and_play_video,
            )
        Button_select.pack(pady=20)
        
        # labels
        Label_text1 = customtkinter.CTkLabel(
            master=self.root,
            text="It will automatically extract frames from the video",
            font=("Comic Sans MS", 16),
            text_color="#000000",
            height=10,
            width=400,
            corner_radius=7,
            bg_color="#f59ee5",
            fg_color="#f59ee5",
            )
        Label_text1.pack(pady=20)
        
        Label_text2 = customtkinter.CTkLabel(
            master=self.root,
            text="Careful if the video is long",
            font=("Comic Sans MS", 15),
            text_color="#000000",
            height=10,
            width=198,
            corner_radius=7,
            bg_color="#f59ee5",
            fg_color="#f59ee5",
            )
        Label_text2.pack(pady=20)
        
    def open_and_play_video(self):
        # Selecting the file
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")])
        if file_path:
            launch_video(file_path)  # Call the function to launch the video in the default player
            FrameCapture(file_path) # extract frames of this file

# Setting up the main window
root = tk.Tk()
app = VideoPlayer(root)
root.protocol("WM_DELETE_WINDOW")
root.mainloop()
