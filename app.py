import yt_dlp
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import threading

downloading = False

def audio_download(url, download_path="downloads"):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'ffmpeg_location': r'./bin',
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

def toggle_element(element, default_cursor):
    global downloading
    if isinstance(element, tk.Frame):
        element.config(cursor="watch" if downloading else default_cursor)
    else:
        state = "disabled" if downloading else "normal"
        cursor = "watch" if downloading else default_cursor
        element.config(state=state, cursor=cursor)

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
    toggle_element(main_frame, 'arrow')
    toggle_element(url_entry, 'xterm')
    toggle_element(download_btn, 'hand2')
    try:
        print("Iniciando download...")
        audio_download(url)
        print("Download concluído!")
        messagebox.showinfo("Sucesso", "Download concluído!")
    except Exception as e:
        print(f'Erro: {e}')
        messagebox.showerror("ERRO", f"{e}")

    url_entry.delete(0, tk.END)

    global downloading
    downloading = False
    toggle_element(main_frame, 'arrow')
    toggle_element(url_entry, 'xterm')
    toggle_element(download_btn, 'hand2')

bg = "#000"

root = tk.Tk()
root.title("Youtube Audio Downloader")
root.resizable(False, False)
root.config(bg=bg)

btn_font = font.Font(family="Roboto", size=14, weight="bold")
h1_font = font.Font(family="Roboto", size=18, weight="bold")
entry_font = font.Font(family="Roboto", size=12)

main_frame = tk.Frame(root, bg=bg)
main_frame.pack(pady=32, padx=32)

url_label = tk.Label(main_frame,
                     font=h1_font,
                     bg=bg,
                     fg="#fff",
                     text="Insira a URL do video ou playlist:"
                     )
url_label.pack(pady=(0,32))

url_entry = tk.Entry(main_frame,
                     bg="#252525",
                     fg="#fff",
                     borderwidth=2,
                     relief=tk.FLAT,
                     font=entry_font,
                     justify="center",
                     insertbackground="red",
                     selectbackground="red"
                    )
url_entry.pack(pady=(0,32), ipady=4, fill=tk.BOTH)

download_btn = tk.Button(main_frame,
                         bg="#ff2222",
                         fg="#000",
                         font=btn_font,
                         text="BAIXAR ÁUDIO",
                         command=download,
                         relief=tk.GROOVE
                         )
download_btn.pack()

root.mainloop()
