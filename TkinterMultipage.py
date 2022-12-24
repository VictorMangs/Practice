from logging import root
import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        self.pagenum = 1
        page1()


class page1(tk.Tk):
    def __init__(self):
        page = tk.Frame(self)
        page.grid()
        tk.Label(page, text = 'This is page 1').grid(row = 0)
        tk.Button(page, text = 'To page 2', command = self.changepage(self.pagenum)).grid(row = 1)

    def page2(self):
        page = tk.Frame(self)
        page.grid()
        tk.Label(page, text = 'This is page 2').grid(row = 0)
        tk.Button(page, text = 'To page 1', command = self.changepage(self.pagenum)).grid(row = 1)

    def changepage(self,pagenum):

        for widget in self.winfo_children():
            widget.destroy()
        if pagenum == 1:
            self.page2()
            self.pagenum = 2
        else:
            self.page1()
            self.pagenum = 1


app = Window()
app.mainloop()