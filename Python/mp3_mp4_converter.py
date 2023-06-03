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
        self.yamlFile = self.yaml.get()

        if self.yamlFile=='':
            mb.showerror(title='Error!',message='Yaml file not selected. Please select Yaml file before processing.')
            return       

        self.saveLocation = self.outputPathString.get().replace('\\','/')

        if len(self.yamlFile)==0:
            print('No yaml input. Trying default path.')
            self.yamlFile = pathlib.Path.cwd() / 'Yaml' / 'test_yaml.yml'
    
        with open(self.yamlFile,'r') as yf:
            self.data = yaml.safe_load(yf)
        
        for media_type in self.data:
            for link in self.data[media_type]:
                if link and (media_type=='mp3'):
                    try:
                        self.download_ytvid_as_mp3(link)
                    except:
                        print(link+' mp3 download failed')
                elif link and (media_type=='mp4'):
                    try:
                        self.download_ytvid_as_mp4(link)
                    except:
                        print(link+' mp4 download failed')
                        
    
        self.cleanup()
        mb.showinfo(title='Alert',message="Download is completed successfully")
    
    ###########################################################################################################################

    def download_ytvid_as_mp3(self,video_url):
        video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
        filename = f"{video_info['title']}.mp3".replace('/',' ').replace('\"','').replace('#','')
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':self.saveLocation+'/'+filename,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        print("Download complete... {}".format(filename))

    ###########################################################################################################################

    def download_ytvid_as_mp4(self,link):
        with youtube_dl.YoutubeDL() as ydl:
            ydl.download([link])

    ###########################################################################################################################

    def cleanup(self):
        self.data['mp3'] = [None for i in range(len(self.data['mp3']))]
        self.data['mp4'] = [None for i in range(len(self.data['mp4']))]

        yaml.SafeDumper.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
        )

        with open('./Yaml/test_yaml.yml',mode='w') as f:
                yaml.safe_dump(self.data, f,default_flow_style=False)

if __name__ == '__main__':
    app = youTube()
    app.mainloop()