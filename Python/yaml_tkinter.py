import pathlib
from tkinter import messagebox as mb

import yt_dlp as youtube_dl
import customtkinter as CTK
from customtkinter import *
from customtkinter import filedialog as fd

import yaml

###########################################################################################################################
###########################################################################################################################

class youTube(CTK.CTk):

    ###########################################################################################################################

    def __init__(self):
        super().__init__()

        CTK.set_appearance_mode('dark')
        CTK.set_default_color_theme('blue')

        #self.geometry("")
        self.title('Python youtube download app')

        self.yamlLabel = CTK.CTkLabel(self,text='Media Yaml file')
        self.yamlLabel.grid(row=0,column=0,sticky=NSEW)

        self.yamlString = CTK.StringVar(value=pathlib.Path.cwd() / 'Yaml' / 'test_yaml.yml')
        self.yaml = CTK.CTkEntry(self, textvariable=self.yamlString,state='disabled',width=300)
        self.yaml.grid(row=0,column=1,pady=12,padx=10,sticky=NSEW)

        self.yamlButton = CTK.CTkButton(self,text='Select file',text_color='red',command=lambda: self.fileLocation(self.yaml))
        self.yamlButton.grid(row=0,column=2,pady=12,padx=10,sticky=NSEW)

        self.pathLabel = CTK.CTkLabel(self,text='Output Path')
        self.pathLabel.grid(row=1,column=0,sticky=NSEW)

        self.outputPathString = CTK.StringVar(value=pathlib.Path.cwd())
        self.outputPath = CTK.CTkEntry(self, textvariable=self.outputPathString,state='disabled',width=300)
        self.outputPath.grid(row=1,column=1,pady=12,padx=10,sticky=NSEW)

        self.pathButton = CTK.CTkButton(self,text='Select file',text_color='red',command=lambda: self.getPath(self.outputPath))
        self.pathButton.grid(row=1,column=2,pady=12,padx=10,sticky=NSEW)

        self.processButton = CTK.CTkButton(self,text='Process',command = lambda:self.read())
        self.processButton.grid(row=2,column=1,sticky=NSEW,pady=(0,5))

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=0)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=0)

    ###########################################################################################################################

    def getPath(self,entry):
        path = fd.askdirectory()

        if path:
            entry.configure(state='normal')
            entry.delete(0,CTK.END)
            entry.insert(CTK.END,path)
            entry.configure(state='disabled')
        else:
            entry.configure(state='normal')
            entry.delete(0,CTK.END)
            entry.configure(state='disabled')

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

        if self.yaml.get()=='':
            mb.showerror(title='Error!',message='Yaml file not selected. Please select Yaml file before processing.')
            return       

        self.saveLoc = self.outputPathString.get().replace('\\','/')

        if len(self.yaml.get())==0:
            print('Epic fail')
        else:
            with open(self.yaml.get(),'r') as yf:
                data = yaml.safe_load(yf)

            for item in data['mp3']:
                if item:
                    if '.com' in item:
                        try:
                            self.download_ytvid_as_mp3(item)
                            # self.simpleMp3(item)
                        except:
                            print(item+' mp3 download failed')
            
            for item in data['mp4']:
                if item:
                    if '.com' in item:
                        try:
                            self.download_ytvid_as_mp4(item)
                        except:
                            print(item+' mp4 download failed')
            
        mb.showinfo(title='Alert',message="Download is completed successfully")
    
    def download_ytvid_as_mp3(self,video_url):
        video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
        filename = f"{video_info['title']}.mp3".replace('/',' ').replace('\"','').replace('#','')
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':self.saveLoc+'/'+filename,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        print("Download complete... {}".format(filename))

    ###########################################################################################################################

    def download_ytvid_as_mp4(self,link):
        with youtube_dl.YoutubeDL() as ydl:
            ydl.download([link])


        # try:
        #     youtubeObject = YouTube(link)
        #     youtubeObject = youtubeObject.streams.get_highest_resolution()
        
        #     youtubeObject.download()
        # except:
        #     mb.showerror(title='Alert',message="An error has occurred, trying authorization")

        #     youtubeObject = YouTube(link,use_oauth=True)
        #     youtubeObject = youtubeObject.streams.get_highest_resolution()
        
        #     youtubeObject.download()

   ###########################################################################################################################

    # def simpleMp3(self,url):
    #     # create a YouTube object
    #     yt = YouTube(url)

    #     # get the highest-quality audio stream
    #     audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

    #     # download the audio stream to a file
    #     audio_file = audio_stream.download()

    #     # convert the audio file to an MP3 file
    #     audio_clip = AudioFileClip(audio_file)
    #     mp3_file = os.path.splitext(audio_file)[0] + '.mp3'
    #     audio_clip.write_audiofile(mp3_file)

    #     # delete the original audio file
    #     audio_clip.close()
    #     os.remove(audio_file)

    #     print(f"Downloaded {yt.title} as an MP3 file: {mp3_file}")

if __name__ == '__main__':
    app = youTube()
    app.mainloop()