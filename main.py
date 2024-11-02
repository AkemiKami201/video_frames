import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import threading
from pydub import AudioSegment
import pyaudio
import numpy as np
from video_to_frames import FrameCapture

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de Video")
        self.root.geometry("1270x720")
        self.root.bind("<Configure>", self.resize_video)

        # Frame para los controles
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        # Botones de control
        self.open_button = tk.Button(control_frame, text="Abrir Video", command=self.open_file)
        self.open_button.grid(row=0, column=0, padx=5)

        self.play_pause_button = tk.Button(control_frame, text="Pausar", command=self.toggle_play_pause, state="disabled")
        self.play_pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(control_frame, text="Finalizar", command=self.stop_video, state="disabled")
        self.stop_button.grid(row=0, column=2, padx=5)

        self.skip_button = tk.Button(control_frame, text="Adelantar 10s", command=self.skip_forward, state="disabled")
        self.skip_button.grid(row=0, column=3, padx=5)
        
        self.button_frame = tk.Button(control_frame, text="Crear Frames", command=FrameCapture, state="disabled")
        self.button_frame.grid(row=0, column=4, padx=5)

        # Label donde se muestra el video
        self.label = tk.Label(self.root)
        self.label.pack(fill=tk.BOTH, expand=True)

        # Variables para el video y audio
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
        # Selección del archivo
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")])
        if file_path:
            # Detener cualquier reproducción actual
            self.stop_video()
            self.cap = cv2.VideoCapture(file_path)
            self.audio = AudioSegment.from_file(file_path)
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.stop = False
            self.paused = False

            # Activar los botones de control
            self.play_pause_button.config(state="normal", text="Pausar")
            self.stop_button.config(state="normal")
            self.skip_button.config(state="normal")
            self.button_frame.config(state="normal")

            # Iniciar los hilos de video y audio
            self.video_thread = threading.Thread(target=self.play_video)
            self.audio_thread = threading.Thread(target=self.play_audio)
            self.video_thread.start()
            self.audio_thread.start()

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
            self.label.after(3)

        self.cap.release()

    def play_audio(self):
        p = pyaudio.PyAudio()
        self.audio_stream = p.open(format=p.get_format_from_width(self.audio.sample_width),
                                   channels=self.audio.channels,
                                   rate=self.audio.frame_rate,
                                   output=True)
        
        # Convertir audio a bytes y reproducir
        audio_data = np.array(self.audio.get_array_of_samples())
        self.audio_stream.write(audio_data.tobytes())
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        p.terminate()
        
    def toggle_play_pause(self):
        # 
        self.paused = not self.paused
        if self.paused:
            self.play_pause_button.config(text="Reanudar")
        else:
            self.play_pause_button.config(text="Pausar")
            
    def stop_video(self):
        self.stop = True
        self.paused = False
        if self.cap:
            self.cap.release()
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

        self.play_pause_button.config(state="disabled", text="Pausar")
        self.stop_button.config(state="disabled")
        self.skip_button.config(state="disabled")
        self.button_frame.config(state="active")

    def skip_forward(self):
        if self.cap:
            current_pos = self.cap.get(cv2.CAP_PROP_POS_MSEC)  # Obtener posición actual en milisegundos
            self.cap.set(cv2.CAP_PROP_POS_MSEC, current_pos + 10000)  # Adelantar 10 segundos

    def resize_video(self, event):
        # Función para actualizar el tamaño del video en función del tamaño de la ventana
        self.frame_width = event.width
        self.frame_height = event.height

    def on_closing(self):
        self.stop_video()
        self.root.destroy()

# Configurar la ventana principal
root = tk.Tk()
app = VideoPlayer(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()