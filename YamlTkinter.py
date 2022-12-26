import customtkinter as CTK
import youtube_dl
from pytube import YouTube
import yaml
from customtkinter import filedialog as fd
import os
from customtkinter import *
from tkinter import messagebox as mb

###########################################################################################################################
###########################################################################################################################

class youTube(CTK.CTk):

    ###########################################################################################################################

    def __init__(self):
        super().__init__()

        CTK.set_appearance_mode('dark')
        CTK.set_default_color_theme('blue')

        self.geometry('600x100')
        self.title('Python youtube download app')

        self.yamlLabel = CTK.CTkLabel(self,text='Media Yaml file')
        self.yamlLabel.grid(row=0,column=0,sticky=NSEW)

        self.yamlString = CTK.StringVar(value='')
        self.yaml = CTK.CTkEntry(self, textvariable=self.yamlString,state='disabled',width=300)
        self.yaml.grid(row=0,column=1,pady=12,padx=10,sticky=NSEW)

        self.yamlButton = CTK.CTkButton(self,text='Select file',text_color='red',command=lambda: self.fileLocation(self.yaml))
        self.yamlButton.grid(row=0,column=2,pady=12,padx=10,sticky=NSEW)

        self.processButton = CTK.CTkButton(self,text='Process',command = lambda:self.read())
        self.processButton.grid(row=1,column=1,sticky=NSEW,pady=(0,5))

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.columnconfigure(0,weight=0)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=0)

    ###########################################################################################################################

    def fileLocation(self,entry):
        file = fd.askopenfile(filetypes=(('yaml files', '*.yml'),('All files', '*.*')))
        if file:
            entry.configure(state='normal')
            entry.delete(0,CTK.END)
            entry.insert(CTK.END,file.name)
            entry.configure(state='disabled')
        else:
            entry.configure(state='normal')
            entry.delete(0,CTK.END)
            entry.configure(state='disabled')

    ###########################################################################################################################

    def read(self):
        if len(self.yaml.get())==0:
            print('Epic fail')
        else:
            with open(self.yaml.get(),'r') as yf:
                data = yaml.safe_load(yf)
                
            for mp3 in data['mp3'].split(' '):
                if '.com' in mp3:
                    self.download_ytvid_as_mp3(mp3)
            
            for mp4  in data['mp4'].split(' '):
                if '.com' in mp4:
                    self.download_ytvid_as_mp4(mp4)
            
        mb.showinfo(title='Alert',message="Download is completed successfully")
    
    def download_ytvid_as_mp3(self,video_url):
        video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
        filename = f"{video_info['title']}.mp3"
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        print("Download complete... {}".format(filename))

    ###########################################################################################################################

    def download_ytvid_as_mp4(self,link):
        try:
            youtubeObject = YouTube(link)
            youtubeObject = youtubeObject.streams.get_highest_resolution()
        
            youtubeObject.download()
        except:
            mb.showerror(title='Alert',message="An error has occurred, trying authorization")

            youtubeObject = YouTube(link,use_oauth=True)
            youtubeObject = youtubeObject.streams.get_highest_resolution()
        
            youtubeObject.download()





if __name__ == '__main__':
    app = youTube()
    app.mainloop()