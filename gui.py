import tkinter as tk
import os
import threading
from tkinter import filedialog, messagebox
import downloader

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
    SONIDOS_DISPONIBLES = os.path.exists("sonidos/descarga.wav") and os.path.exists("sonidos/terminado.wav")
except ImportError:
    PYGAME_AVAILABLE = False
    SONIDOS_DISPONIBLES = False


class Gui:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Code Downloader")
        self.parent.geometry("600x300")
        self.parent.resizable(False, False)
        self.parent.configure(bg="#333333")

        # Icono
        if os.name == "nt":
            self.parent.iconbitmap("interfaz/youtube.ico")
        else:
            self.parent.iconphoto(False, tk.PhotoImage(file="interfaz/youtube.png"))

        # Título principal
        self.title = tk.Label(
            self.parent,
            text="Code Downloader",
            font=("nunito", 24),
            fg="#FF3737",
            bg="#333333",
            padx=30,
            pady=30,
        )
        self.title.place(x=120, y=0)

        # Texto URL
        self.title_url = tk.Label(
            self.parent,
            text="Ingrese la URL (video o playlist):",
            font=("nunito", 16),
            fg="#FF6666",
            bg="#333333",
            padx=30
        )
        self.title_url.place(x=75, y=110)

        # Input URL
        self.url_entry = tk.Entry(
            self.parent,
            font=("nunito", 16),
            fg="#000000",
            bg="#FFFFFF",
            width=30
        )
        self.url_entry.place(x=110, y=150)

        # Botón MP4
        self.download_button_mp4 = tk.Button(
            self.parent,
            text="Descargar MP4",
            font=("nunito", 16),
            fg="#FFFFFF",
            bg="#555555",
            command=self.download_mp4
        )
        self.download_button_mp4.place(x=15, y=225)

        # Botón MP3
        self.download_button_mp3 = tk.Button(
            self.parent,
            text="Descargar MP3",
            font=("nunito", 16),
            fg="#FFFFFF",
            bg="#555555",
            command=self.download_mp3
        )
        self.download_button_mp3.place(x=230, y=225)

        # Botón salir
        self.exit_button = tk.Button(
            self.parent,
            text="Salir",
            font=("nunito", 16),
            fg="#FFFFFF",
            bg="#555555",
            command=self.parent.quit,
            width=10
        )
        # Barra de progreso
        self.progress_label = tk.Label(
            self.parent,
            text="",
            font=("nunito", 10),
            fg="#FF6666",
            bg="#333333"
        )
        self.progress_label.place(x=110, y=190)

        self.progress_bar = tk.Canvas(
            self.parent,
            width=380,
            height=15,
            bg="#222222",
            highlightthickness=0
        )
        self.progress_bar.place(x=110, y=205)
        self.progress_rect = None

        self.exit_button.place(x=450, y=225)

    # -------------------------
    # FUNCIONES
    # -------------------------

    def download_mp3(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Introduce una URL")
            return

        folder = self.select_directory()
        if not folder:
            return

        self._iniciar_descarga(url, True, folder)

    def _iniciar_descarga(self, url, only_audio, folder):
        messagebox.showinfo("INFO", "Iniciando descarga...")
        self._reset_progress()

        def progress_callback(progreso):
            self.progress_label.config(text=progreso)
            self._actualizar_barra(progreso)

        def hilo_descarga():
            downloader.descargar_video(url, only_audio, folder, progress_callback)
            if PYGAME_AVAILABLE and SONIDOS_DISPONIBLES:
                try:
                    pygame.mixer.music.load("sonidos/terminado.wav")
                    pygame.mixer.music.play()
                except:
                    pass
            self.progress_label.after(0, lambda: self.progress_label.config(text="Completado"))

        thread = threading.Thread(target=hilo_descarga, daemon=True)
        thread.start()

    def _reset_progress(self):
        self.progress_bar.delete("all")
        self.progress_label.config(text="")

    def _actualizar_barra(self, progreso):
        if "%" in progreso:
            pct = float(progreso.replace("%", ""))
            x = (pct / 100) * 380
            self.progress_bar.delete("all")
            self.progress_bar.create_rectangle(0, 0, x, 15, fill="#FF3737", width=0)

    def download_mp4(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Introduce una URL")
            return

        folder = self.select_directory()
        if not folder:
            return

        self._iniciar_descarga(url, False, folder)

    def select_directory(self):
        folder = filedialog.askdirectory(title="Selecciona carpeta de descarga")
        return folder if folder else None
