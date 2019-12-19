from myparser import Parser
from mytoken import Token, availableTokens
from tkinter import messagebox
from tkinter import *
from error import *

class MainWindow:

    def __init__(self):
        self.master = Tk()

        self.frametext = Frame(self.master)
        self.frametext.pack()

        self.label = Label(self.frametext, text="Input Text", font=2)
        self.label.pack(fill=X, pady=5)

        self.scroll = Scrollbar(self.frametext)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.textbox = Text(self.frametext,font=2, width=50, height=25)
        self.textbox.pack()
        self.textbox.config(yscrollcommand=self.scroll.set)

        self.runButton = Button(self.master, text="Run", width=7, font=2, command=self.getInputLines)
        self.exitButton = Button(self.master, text="Exit", width=7, font=2, command=self.master.quit)

        self.exitButton.pack(side=RIGHT, pady=5, padx=5)
        self.runButton.pack(side=RIGHT, pady=5, padx=5)

        self.master.mainloop()


    def getInputLines(self):
        inputtext = self.textbox.get("1.0", END)
        inputtext = inputtext.strip().splitlines()
        while('' in inputtext):
            inputtext.remove('')
        self.tokenslist = self.tokenize(inputtext)
        parser = Parser(self.tokenslist)
        try:
            parser.parse()
        except ExpectingIdentifier:
            # print("Expecting Identifier!")
            messagebox.showerror("Error", "Expecting Identifier")
        except ExpectingThen:
            messagebox.showerror("Error", "Expecting 'then'")
        except ExpectingEnd:
            messagebox.showerror("Error", "Expecting 'end' or 'else'")
        except ExpectingUntil:
            messagebox.showerror("Error", "Expecting 'until'")
        except ExpectingAssign:
            messagebox.showerror("Error", "Expecting ':='")
        except ExpectingNumorId:
            messagebox.showerror("Error", "Expecting Number, Identifier or '('")
        except ExpectingRightBracket:
            messagebox.showerror("Error", "Expecting ')'")
            
        
        # self.statements_found = parser.parse()
        # for stmt in self.statements_found:
        #     print(stmt)

    def tokenize(self, inputlines):
        tokenlist = list()
        for line in inputlines:
            #    xyz   ,        id
            linelist = line.split(",")
            #    [          xyz      ,       id]
            newtoken = Token(linelist[0].replace(" ", ""), linelist[1].replace(" ", ""))
            # {xyz,id}
            # newtoken.value, newtoken.type
            tokenlist.append(newtoken)
            # tokenlist[0].value
        return tokenlist


mainwindow = MainWindow()




