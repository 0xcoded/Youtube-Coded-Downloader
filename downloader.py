import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox


def validar_url(url):
    youtube_domains = ["youtube.com", "youtu.be", "youtube-nocookie.com"]
    return any(domain in url for domain in youtube_domains)


def progreso_hook(downloaded, total, prefix=""):
    if total:
        percentage = (downloaded / total) * 100
        return f"{prefix}{percentage:.1f}%"
    return f"{prefix}Descargando..."


def descargar_video(url, only_audio, output_folder, progress_callback=None):
    if not output_folder:
        messagebox.showerror(title="ERROR", message="No seleccionaste carpeta")
        return False

    if not validar_url(url):
        messagebox.showerror(title="ERROR", message="URL inválida. Debe ser de YouTube.")
        return False

    opciones = {
        'outtmpl': f'{output_folder}/%(playlist_title)s/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': False,
        'ignoreerrors': True,
    }

    if only_audio:
        opciones.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })

    def progress_handler(d):
        if progress_callback and d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            progress_callback(progreso_hook(downloaded, total))

    opciones['progress_hooks'] = [progress_handler]

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            total_videos = 1
            if 'entries' in info:
                total_videos = len([e for e in info['entries'] if e])

            ydl.download([url])

        mensaje = f"Descarga completada: {total_videos} video(s)"
        if only_audio:
            mensaje += " (MP3)"
        messagebox.showinfo(title="INFO", message=mensaje)
        return True

    except yt_dlp.utils.DownloadError as e:
        messagebox.showerror(title="ERROR", message=f"Error al descargar: {e}")
    except yt_dlp.utils.ExtractorError as e:
        messagebox.showerror(title="ERROR", message=f"Error al extraer info: {e}")
    except Exception as e:
        messagebox.showerror(title="ERROR", message=f"Error inesperado: {e}")

    return False