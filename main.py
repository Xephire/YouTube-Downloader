"""
Copyright Gabriel Pery 2021
"""

from pytube import YouTube
import tkinter as tk
from threading import Thread
from tkinter import ttk
import os, sys, subprocess, getpass, logging


if not os.path.exists(os.getenv('LOCALAPPDATA') + '\\Programs\\YouTube Downloader\\errorlog.log'):
    os.makedirs(os.getenv('LOCALAPPDATA') + '\\Programs\\YouTube Downloader\\')
logging.basicConfig(filename=os.getenv('LOCALAPPDATA') + '\\Programs\\YouTube Downloader\\errorlog.log', level=logging.ERROR, force=True, format='%(asctime)s %(levelname)s %(name)s %(message)s')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def convertToMp3(name, mp4Path):
    username = getpass.getuser()

    mp3 = f'C:\\Users\\{username}\\Downloads\\{name}.mp3'
    
    CREATE_NO_WINDOW = 0x08000000
    subprocess.call(f'ffmpeg -i "{mp4Path}" -vn "{mp3}"', creationflags=CREATE_NO_WINDOW)

    
def downloadMP4(entry, warningLabel, successLabel):

    successLabel.pack_forget()
    warningLabel.pack_forget()

    url = entry.get()
    try:
        username = getpass.getuser()
        yt = YouTube(url)
        ys = yt.streams.get_highest_resolution()

        ys.download(f'C:\\Users\\{username}\\Downloads\\')
        successLabel.pack()
        entry.select_range(0, 'end')

    except Exception as e:
        logging.error(e)
        warningLabel.pack()
        
        
def downloadMP3(entry, warningLabel, successLabel):

    successLabel.pack_forget()
    warningLabel.pack_forget()

    url = entry.get()
    try:
        username = getpass.getuser()
        yt = YouTube(url)
        ys = yt.streams.get_audio_only()
        name = os.path.splitext(ys.default_filename)[0]

        ys.download(f'C:\\Users\\{username}\\AppData\\Local\\YoutubeDownloader\\temp\\')
        
        mp4Path = f'C:\\Users\\{username}\\AppData\\Local\\YoutubeDownloader\\temp\\{ys.default_filename}'
        
        convertToMp3(name, mp4Path)
        os.remove(mp4Path)
        successLabel.pack()
        entry.select_range(0, 'end')

    except Exception as e:
        logging.error(e)
        warningLabel.pack()
        

# threads


def startMP4Thread(entry, warningLabel, successLabel):
    mp4Thread = Thread(target = lambda : downloadMP4(entry, warningLabel, successLabel))
    mp4Thread.daemon = True
    mp4Thread.start()

def startMP3Thread(entry, warningLabel, successLabel):
    mp3Thread = Thread(target = lambda : downloadMP3(entry, warningLabel, successLabel))
    mp3Thread.daemon = True
    mp3Thread.start()


def gui():
    window = tk.Tk()

    window.title('YouTube Converter')
    window.geometry('500x165')

    iconPath = resource_path('icon.png')
    icon = tk.PhotoImage(file=iconPath)
    window.iconphoto(False, icon)
    
    window.configure(bg='white')

    label = tk.Label(text='Enter URL:', background='white', font='bebasneue')
    entry = tk.Entry(width='50',bg='light gray', font='bebasneue')

    warningLabel = tk.Label(text='There was an error converting the video', background='white', font='bebasneue')
    successLabel = tk.Label(text='Download successful', background='white', font='bebasneue')


    frame = ttk.Frame(window)
    frame.pack()

    mp4Button = tk.Button(
    text="Convert to MP4",
    width=13,
    height=2,
    bg="light gray",
    fg="black",
    font='bebasneue',
    command = lambda : startMP4Thread(entry, warningLabel, successLabel)
    )   

    mp3Button = tk.Button(
    text="Convert to MP3",
    width=13,
    height=2,
    bg="light gray",
    fg="black",
    font='bebasneue',
    command = lambda : startMP3Thread(entry, warningLabel, successLabel)
    )   


    label.pack()
    entry.pack()
    mp4Button.pack(side='bottom')
    mp3Button.pack(side='bottom')


    window.mainloop()

try:
    gui()
except Exception as e: 
    logging.error(e) # logs any errors that happen on startup
