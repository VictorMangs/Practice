import pathlib
from tkinter import messagebox as mb

import customtkinter as CTK
import yaml
from customtkinter import *
from customtkinter import filedialog as fd


class youTube(CTK.CTk):

    ###########################################################################################################################

    def __init__(self):
        super().__init__()

        CTK.set_appearance_mode('dark')
        CTK.set_default_color_theme('blue')

        self.geometry('700x100')
        self.title('Youtube mp3/mp4 downloader')

        self.yamlLabel = CTK.CTkLabel(self,text='Media Yaml file')
        self.yamlLabel.grid(row=0,column=0,sticky=NSEW)

        self.yamlString = CTK.StringVar(value=pathlib.Path.cwd() / 'testYaml.yml')
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

    def create(self):
        teaspoons = {'tablespoons':1/3,'cups':1/48,'pint':1/96,'quart':1/192,'gallon':1/768}
        tablespoon = {'teaspoons':3,'cups':1/16,'pint':1/32,'quart':1/64,'gallon':1/256}
        cup = {'teaspoons':48,'tablespoons':16,'pint':1/2,'quart':1/4,'gallon':1/16}
        pint = {'teaspoons':96,'tablespoons':32,'cup':2,'quart':1/2,'gallon':1/8}
        quart = {'teaspoons':192,'tablespoons':64,'cup':4,'pint':2,'gallon':1/4}
        gallon = {'teaspoons':768,'tablespoons':256,'cup':16,'pint':8,'quart':4}

        pass

if __name__ == '__main__':
    app = youTube()
    app.mainloop()