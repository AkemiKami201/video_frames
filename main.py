import tkinter as tk
from tkinter import filedialog
from video_to_frames import FrameCapture
from video_player_launcher import launch_video

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame")
        self.root.geometry("300x100")

        # Button to select and open the video file
        self.open_button = tk.Button(root, text="Select and play video", command=self.open_and_play_video)
        self.open_button.pack(pady=20)

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
