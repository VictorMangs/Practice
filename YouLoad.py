import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import messagebox
from pytube import YouTube

class mp4Load(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('This is how we do it!')
        self.geometry('300x300')
        self.resizable(False,False)

        self.videos = []
        self.videoBox = ScrolledText(self,)


    def Download(self,link):
        youtubeObject = YouTube(link,use_oauth=True)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        try:
            youtubeObject.download()
        except:
            print("An error has occurred")
        print("Download is completed successfully")


#link = input("Enter the YouTube video URL: ")

if __name__ == '__main__':
    app = mp4Load()
    app.mainloop()