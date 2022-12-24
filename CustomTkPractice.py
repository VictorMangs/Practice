import customtkinter as CTK
import youtube_dl
from pytube import YouTube
import yaml
from customtkinter import filedialog as fd
import os
from customtkinter import *


class youTube(CTK.CTk):
    
    def __init__(self):
        super().__init__()

        CTK.set_appearance_mode('dark')
        CTK.set_default_color_theme('blue')

        self.geometry('580x125')
        self.title('Python youtube download app')

        ##############################################################################################################
        self.mp3String = CTK.StringVar(value='Yaml file location')
        
        self.mp3 = CTK.CTkEntry(self, textvariable=self.mp3String,state='disabled',width=300)
        self.mp3.grid(row=0,column=1,pady=12,padx=10)
        
        self.mp3Button = CTK.CTkButton(self,text='Select file',text_color='red',state='disabled',command=lambda: self.fileLocation(self.mp3))
        self.mp3Button.grid(row=0,column=2,pady=12,padx=10)

        self.checkbox_mp3 = CTK.CTkCheckBox(self,text='mp3',width=40,onvalue=1,offvalue=0,command=lambda: self.enableButton('mp3'))
        self.checkbox_mp3.grid(row=0,column=0,pady=12,padx=10)

        ##############################################################################################################

        self.mp4String = CTK.StringVar(value='Yaml file location')
        self.mp4 = CTK.CTkEntry(self, textvariable=self.mp4String,state='disabled',width=300)
        self.mp4.grid(row=1,column=1,pady=12,padx=10)

        self.mp4Button = CTK.CTkButton(self,text='Select file',text_color='red',state='disabled',command=lambda: self.fileLocation(self.mp4))
        self.mp4Button.grid(row=1,column=2,pady=12,padx=10)

        self.checkbox_mp4 = CTK.CTkCheckBox(self,text='mp4',width=40,onvalue=1,offvalue=0,command=lambda: self.enableButton('mp4'))
        self.checkbox_mp4.grid(row=1,column=0,pady=12,padx=10)

        ##############################################################################################################

    def enableButton(self,widget):
        if widget == 'mp4':

            if self.checkbox_mp4.get()==0:
                self.mp4.configure(state='normal')
                self.mp4.delete(0,END)
                self.mp4.configure(state='disabled')

                self.mp4Button.configure(state='disabled')

            elif self.checkbox_mp4.get()==1:
                self.mp4Button.configure(state='normal')

        elif widget == 'mp3':

            if self.checkbox_mp3.get()==0:

                self.mp3.configure(state='normal')
                self.mp3.delete(0,END)
                self.mp3.configure(state='disabled')

                self.mp3Button.configure(state='disabled')

            elif self.checkbox_mp3.get()==1:
                
                self.mp3Button.configure(state='normal')


    def fileLocation(self,entry):
        file = fd.askopenfile(filetypes=(('yaml files', '*.yml'),('All files', '*.*')))

        entry.configure(state='normal')
        entry.delete(0,CTK.END)
        entry.insert(CTK.END,file.name)
        entry.configure(state='disabled')


    def read(self):
        #with open(self.entry1String.get(),'r') as yf:
        #    try:
        #        for data in yf
        pass

        '''
        label =CTK.CTkLabel(self,text='Login:',text_color='red')
        label.pack(pady=12,padx=10)

        entry1 = CTK.CTkEntry(self, placeholder_text='Username')
        entry1.pack(pady=12,padx=10)

        entry2 = CTK.CTkEntry(self, placeholder_text='Password',show="$")
        entry2.pack(pady=12,padx=10)

        button = CTK.CTkButton(self,text ='login')
        button.pack(pady=12,padx=10)

        checkbox = CTK.CTkCheckBox(self,text='Remember Me')
        checkbox.pack(pady=12,padx=10)
        '''



if __name__ == '__main__':
    app = youTube()
    app.mainloop()