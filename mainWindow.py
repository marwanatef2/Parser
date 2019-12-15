from tkinter import *
from todo import *

class MainWindow:

    def __init__(self):
        self.master = Tk()

        self.frametext = Frame(self.master)
        self.frametext.pack()

        self.scroll = Scrollbar(self.frametext)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.textbox = Text(self.frametext,font=2, width=50, height=25)
        self.textbox.pack()
        self.textbox.config(yscrollcommand=self.scroll.set)

        self.runButton = Button(self.master, text="Run", width=7, command=self.getInputLines)
        self.exitButton = Button(self.master, text="Exit", width=7, command=self.master.quit)

        self.exitButton.pack(side=RIGHT, pady=5, padx=5)
        self.runButton.pack(side=RIGHT, pady=5, padx=5)

        self.master.mainloop()


    def getInputLines(self):
        inputtext = self.textbox.get("1.0", END)
        inputtext = inputtext.strip().splitlines()
        while('' in inputtext):
            inputtext.remove('')
        self.toDo(inputtext)

    toDo = to_do


mainwindow = MainWindow()




