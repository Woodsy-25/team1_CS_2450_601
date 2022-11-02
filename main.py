'''
This is the main program that curretly holds both the code from the employee project and also hold the code for the GUI.
'''


import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

import sv_ttk


#the payroll code
largefont = ('Verdana', 20) # specify font and size

class PayrollApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #size of the window
        tk.Tk.geometry(self, "500x500")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for f in (StartingPage, AdminPage, EmployeePage, LoginPage):
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartingPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome to the Payroll System", font=largefont)
        #make it top center
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Login", command=lambda: controller.show_frame(LoginPage))
        button1.pack(pady=10)

        button2 = ttk.Button(self, text="Quit", command=quit)
        button2.pack()

        #toggle themes
        theme_button = ttk.Button(self, text="Toggle Theme", command=sv_ttk.toggle_theme)
        theme_button.pack(side = BOTTOM)
        

def login(entry1, entry2):
        if entry1 == "admin" and entry2 == "admin":
            #opening admin page
            app.show_frame(AdminPage)
        elif entry1 == "user" and entry2 == "user":
            #opening user page
            app.show_frame(EmployeePage)
        else:
            messagebox.showerror("Error", "Invalid username or password")

'''
-----------------LOGIN PAGE-----------------
'''

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Login", font=largefont)
        label.pack(pady=10, padx=10)

        label1 = tk.Label(self, text="Username")
        label1.pack()

        entry1 = tk.Entry(self)
        entry1.pack()

        label2 = tk.Label(self, text="Password")
        label2.pack()

        entry2 = tk.Entry(self, show = "*")
        entry2.pack()

        #check if username and password are correct
        button1 = ttk.Button(self, text="Login", command=lambda: login(entry1.get(), entry2.get()))
        button1.pack()
        

        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartingPage))
        button2.pack()

'''
-----------------ADMIN PAGE-----------------
'''

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Admin Page", font=largefont)
        label.pack(pady=10, padx=10)
        #add tabs to switch frames
        tabControl = ttk.Notebook(self)
        #add tabs with
        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        #open add employee page
        tabControl.add(tab1, text='Add Employee')
        tabControl.add(tab2, text='View Employee')
        tabControl.pack(expand=1, fill="both")

        '''
        -----------------ADD EMPLOYEE-----------------
        '''
   
        first_name_label = tk.Label(tab1, text="First Name")
        first_name_label.pack()

        first_name_entry = tk.Entry(tab1)
        first_name_entry.pack()

        label2 = tk.Label(tab1, text="Last Name")
        label2.pack()

        entry2 = tk.Entry(tab1)
        entry2.pack()

        label3 = tk.Label(tab1, text="Street")
        label3.pack()

        entry3 = tk.Entry(tab1)
        entry3.pack()

        label4 = tk.Label(tab1, text="City")
        label4.pack()

        entry4 = tk.Entry(tab1)
        entry4.pack()

        label5 = tk.Label(tab1, text="State")
        label5.pack()

        entry5 = tk.Entry(tab1)
        entry5.pack()

        label6 = tk.Label(tab1, text="Zipcode")
        label6.pack()

        entry6 = tk.Entry(tab1)
        entry6.pack()

        #option menu for classification(salaried, hourly, commisioned)
        label7 = tk.Label(tab1, text="Classification")
        label7.pack()

        entry7 = tk.Entry(tab1)
        entry7.pack()

        #will run command to add employee to database
        button1 = ttk.Button(tab1, text="Enter")
        button1.pack()


        '''
        -----------------VIEW EMPLOYEE-----------------
        '''
        #create a search bar
        label8 = tk.Label(tab2, text="Search")
        label8.pack()

        entry8 = tk.Entry(tab2)
        entry8.pack()


        #put logout button on the top right
        button1 = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(StartingPage))
        button1.pack(side="right")
'''
-----------------EMPLOYEE PAGE-----------------
'''

class EmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Employee Page", font=largefont)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(AdminPage))
        button1.pack()


'''
class AddEmployeePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Add Employee", font=largefont)
        label.pack(pady=10, padx=10)
    
        label1 = tk.Label(self, text="First Name")
        label1.pack()

        entry1 = tk.Entry(self)
        entry1.pack()

        label2 = tk.Label(self, text="Last Name")
        label2.pack()

        entry2 = tk.Entry(self)
        entry2.pack()

        label3 = tk.Label(self, text="Address")
        label3.pack()

        entry3 = tk.Entry(self)
        entry3.pack()

        label4 = tk.Label(self, text="City")
        label4.pack()

        entry4 = tk.Entry(self)
        entry4.pack()

        label5 = tk.Label(self, text="State")
        label5.pack()

        entry5 = tk.Entry(self)
        entry5.pack()

        label6 = tk.Label(self, text="Zipcode")
        label6.pack()

        entry6 = tk.Entry(self)
        entry6.pack()

        #option menu for classification(salaried, hourly, commisioned)
        label7 = tk.Label(self, text="Classification")
        label7.pack()

        entry7 = tk.Entry(self)
        entry7.pack()

        button1 = ttk.Button(self, text="Add Employee", command=lambda: controller.show_frame(AdminPage))
        button1.pack()

        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(AdminPage))
        button2.pack()
'''

#making a list from logins.csv
with open('logins.csv', 'r') as f:
    #skip the first line
    next(f)
    #make a list of lists
    logins = [line.strip().split(',') for line in f]


#open app
app = PayrollApp()
sv_ttk.set_theme('light')
app.mainloop()