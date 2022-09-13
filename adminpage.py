#after login, the admin page should be displayed

from tkinter import *
from tkinter import ttk

class AdminPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.lbl1 = Label(self, text="Admin Page")
        self.lbl1.grid(row=0, column=0)
        self.btn1 = Button(self, text="Quit", command=self.quit)
        self.btn1.grid(row=1, column=0)

root = Tk()
root.title("Admin Page")
root.geometry("300x150")
app = AdminPage(master=root)
app.mainloop()