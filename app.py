import yt_dlp
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import io
import sys
import threading

class RedirectText(io.StringIO):
    def __init__(self, text_widget):
        self.text_widget = text_widget
    
    def write(self, string):
        self.text_widget.config(state=tk.NORMAL)  # Permite a edição temporária
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)  # Desativa a edição novamente


downloading = False

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
    global downloading
    if downloading:
        messagebox.showwarning("Atenção", "Um download já está em andamento.")
        return
    url = url_entry.get()
    if url:
        downloading = True
        thread = threading.Thread(target=download_audio_thread, args=(url,))
        thread.start()
    else:
        messagebox.showwarning("Atenção", "Insira uma URL.")

def download_audio_thread(url):
    print("Iniciando download...")
    audio_download(url)
    print("Download concluído!")
    messagebox.showinfo("Sucesso", "Download concluído!")
    url_entry.delete(0, tk.END)
    global downloading
    downloading = False

root = tk.Tk()
root.title("Youtube Audio Downloader")
root.geometry("400x400")
root.resizable(False, False)

custom_font = font.Font(family="Arial", size=10)

url_label = tk.Label(root, font=custom_font, text="Insira a URL do video ou playlist:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

download_btn = tk.Button(root, font=custom_font, text="Download", command=download)
download_btn.pack(pady=20)

text_area = tk.Text(root, font=custom_font, bg="#000000", fg="white", wrap=tk.WORD)
text_area.config(state=tk.DISABLED)
text_area.pack(expand=True, fill=tk.BOTH)

redirected_output = RedirectText(text_area)
sys.stdout = redirected_output

root.mainloop()

sys.stdout = sys.__stdout__