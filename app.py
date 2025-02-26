import yt_dlp
import os
import tkinter as tk
from tkinter import messagebox

def audio_download(url, download_path="downloads"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'ffmpeg_location': r'C:.\bin',
        'format': 'bestaudio/best',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'noplaylist': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download():
    url = url_entry.get()
    if url:
        audio_download(url)
        messagebox.showinfo("Sucesso", "Download concluído!")
        url_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Atenção", "Insira uma URL.")

root = tk.Tk()
root.title("Youtube Audio Downloader")
root.geometry("400x200")

url_label = tk.Label(root, text="Insira a URL do video ou playlist:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

download_btn = tk.Button(root, text="Download", command=download)
download_btn.pack(pady=20)

root.mainloop()