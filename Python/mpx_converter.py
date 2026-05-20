from pathlib import Path
from tkinter import messagebox as mb

import yt_dlp as youtube_dl
import customtkinter as CTK
from customtkinter import filedialog as fd

import yaml

# Media type constants
MP3 = 'mp3'
MP4 = 'mp4'

###########################################################################################################################
###########################################################################################################################

class YouTube(CTK.CTk):

    ###########################################################################################################################

    def __init__(self):
        super().__init__()

        CTK.set_appearance_mode('dark')
        CTK.set_default_color_theme('blue')

        #self.geometry("")
        self.title('Python youtube download app')

        self.yamlLabel = CTK.CTkLabel(self,text='Media Yaml file')
        self.yamlLabel.grid(row=0,column=0,sticky=CTK.NSEW)

        self.yamlString = CTK.StringVar(value=str(Path(__file__).parent.parent / 'yaml' / 'mpx.yml'))
        self.yaml = CTK.CTkEntry(self, textvariable=self.yamlString,state='disabled',width=300)
        self.yaml.grid(row=0,column=1,pady=12,padx=10,sticky=CTK.NSEW)

        self.yamlButton = CTK.CTkButton(self,text='Select file',text_color='red',command=lambda: self.fileLocation(self.yaml))
        self.yamlButton.grid(row=0,column=2,pady=12,padx=10,sticky=CTK.NSEW)

        self.pathLabel = CTK.CTkLabel(self,text='Output Path')
        self.pathLabel.grid(row=1,column=0,sticky=CTK.NSEW)

        self.outputPathString = CTK.StringVar(value=str(Path.cwd()))
        self.outputPath = CTK.CTkEntry(self, textvariable=self.outputPathString,state='disabled',width=300)
        self.outputPath.grid(row=1,column=1,pady=12,padx=10,sticky=CTK.NSEW)

        self.pathButton = CTK.CTkButton(self,text='Select file',text_color='red',command=lambda: self.getPath(self.outputPath))
        self.pathButton.grid(row=1,column=2,pady=12,padx=10,sticky=CTK.NSEW)

        self.processButton = CTK.CTkButton(self,text='Process',command = lambda:self.read())
        self.processButton.grid(row=2,column=1,sticky=CTK.NSEW,pady=(0,5))

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
# C:\Users\Victor2021\Pictures\
    def read(self, output_path=None):
        self.yamlFile = self.yaml.get()

        if self.yamlFile=='':
            mb.showerror(title='Error!',message='Yaml file not selected. Please select Yaml file before processing.')
            return       
        if output_path:
            self.saveLocation = output_path
        else:
            self.saveLocation = Path(self.outputPathString.get())

        if not self.saveLocation.exists():
            print(f"Output path does not exist: {self.saveLocation}")
            return

        with open(self.yamlFile,'r') as yf:
            self.data = yaml.safe_load(yf)
        
        for media_type in self.data:
            for link in self.data[media_type]:
                if link and (media_type == MP3):
                    try:
                        self.download_ytvid_as_mp3(link)
                    except Exception as e:
                        print(f"{link} mp3 download failed: {e}")
                elif link and (media_type == MP4):
                    try:
                        self.download_ytvid_as_mp4(link)
                    except Exception as e:
                        print(f"{link} mp4 download failed: {e}")
                        
    
        self.cleanup()
        mb.showinfo(title='Alert',message="Download is completed successfully")
    
    ###########################################################################################################################

    def download_ytvid_as_mp3(self,video_url):
        video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
        filename = f"{video_info['title']}.mp3".replace('/',' ').replace('\"','').replace('#','')
        output_path = str(Path(self.saveLocation) / filename)
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':output_path,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        print("Download complete... {}".format(filename))

    ###########################################################################################################################

    def download_ytvid_as_mp4(self,link):
        options = {
        'format': 'bestvideo+bestaudio/best', # Select best quality video and audio, then merge
        'merge_output_format': 'mp4',        # Merge into an MP4 file
        # 'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'), # Output template
        'noplaylist': True,                   # Ensure only single video is downloaded if a playlist URL is provided
        # 'progress_hooks': [my_hook],          # Add a progress hook (optional)
        'external_downloader': 'ffmpeg',      # Specify ffmpeg as external downloader for merging
        'external_downloader_args': ['-loglevel', 'panic'] # Optional: suppress ffmpeg output
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([link])

    ###########################################################################################################################

    def cleanup(self):
        self.data[MP3] = [None for i in range(len(self.data[MP3]))]
        self.data[MP4] = [None for i in range(len(self.data[MP4]))]

        yaml.SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
        )

        with open(self.yamlFile,mode='w') as f:
                yaml.safe_dump(self.data, f,default_flow_style=False)

if __name__ == '__main__':
    app = YouTube()
    app.read()