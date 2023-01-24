import tkinter as tk
import random

class TopLevel(tk.Tk):
    def __init__(self,parent):
        super().__init__(parent)

        #Window attributes
        self.geometry('300x300')
        self.title('Take you\'re best guess')
        self.resizable(False,False)

        self.guessEntry = tk.Entry()
        self.guessEntry.place(relx=.5,rely=.5)


class TkinterMain(tk.Tk):
    def __init__(self):
        #Needed for object oriented tkinter (Prevents infinite recursion)
        super().__init__()

        #Window attributes
        self.geometry('320x100')
        self.title('Setup Page')
        self.resizable(False,False)

        #Welcome String
        self.welcome = ''


        #Name Label
        self.nameLabel = tk.Label(self,text = 'Welcome! Enter you\'re name:')
        self.nameLabel.place(rely=.25,x=0)

        #Name Entry
        self.nameEntry = tk.Entry(self)
        self.nameEntry.place(rely=.25,x=175)


        #Processing button
        self.button = tk.Button(text='Play',command = lambda:self.basicFunction())
        self.button.place(rely = .7,relx = .5)

    def basicFunction(self):
        self.welcome = 'Welcome to a guessing game '+str(self.nameEntry.get())+'!'
        self.printLabel = tk.Label(text='Welcome to a guessing game '+str(self.nameEntry.get())+'!')
        self.printLabel.place(relx=0,rely=.5)



    def numberGeneration(self):
        diff = input('On a scale of easy-1 to impossible-4, what level difficulty do you want? ')
        diff = self.integer(diff)

        while type(diff)!=int or diff>4:
            diff = input('Press 1 for easy, 2 for medium, 3 for hard, and 4 for impossible: ')
            diff = self.integer(diff)

        lo = random.randint(1,5**diff)
        up = random.randint(6**diff,13**diff)
        number = random.randint(lo,up)

        hint = 3*diff

    def integer(self,num):
        try: 
            return int(num)
        except:
            print("Integer please!")

    def check(self,guess,num):
        if guess>num:
            print("Too High!")
            return False
        elif guess<num:
            print("Too Low!")
            return False
        else:
            return True

    def guessing(self,number,low,high,hint):
        while ans == False and hint>0:
            print("Hint: The number is between " + str(low) + " and " + str(high) + " .")
            guess = input('Try again! You have ' + str(hint) + ' more trie(s).'  + ' What do you think the number is? ')
            guess = self.integer(guess)
            ans = self.check(guess,number)

        hint-=1


        if ans == True:
            print('That\'s it! You guessed right!')
        else:
            print('No!!! It was actually ' + str(number) + '. Better luck next time!' )



app = TkinterMain()
app.mainloop()

