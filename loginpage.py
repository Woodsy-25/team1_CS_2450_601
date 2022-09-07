from tkinter import *
from tkinter import ttk

#creating a login page
class LoginPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.lbl1 = Label(self, text="Username")
        self.lbl1.grid(row=0, column=0)
        self.lbl2 = Label(self, text="Password")
        self.lbl2.grid(row=1, column=0)
        self.txt1 = Entry(self)
        self.txt1.grid(row=0, column=1)
        self.txt2 = Entry(self, show="*")
        self.txt2.grid(row=1, column=1)
        self.btn1 = Button(self, text="Login", command=self.login)
        self.btn1.grid(row=2, column=0)
        self.btn2 = Button(self, text="Quit", command=self.quit)
        self.btn2.grid(row=2, column=1)

    def login(self):
        if self.txt1.get() == "admin" and self.txt2.get() == "admin":
            self.lbl3 = Label(self, text="Login Successful")
            self.lbl3.grid(row=3, column=0)
        else:
            self.lbl3 = Label(self, text="Login Failed")
            self.lbl3.grid(row=3, column=0)

root = Tk()
root.title("Login Page")
root.geometry("300x150")
app = LoginPage(master=root)
app.mainloop()