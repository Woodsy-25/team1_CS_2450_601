'''
This is the main program that curretly holds both the code from the employee project and also hold the code for the GUI.
'''


import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from emp import *

import sv_ttk
import os

#the payroll code
LARGE_FONT = ('Verdana', 20) # specify font and size
USER_TYPE_EMPLOYEE = '1'
USER_TYPE_ADMIN = '2'

class PayrollApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #size of the window
        tk.Tk.geometry(self, "800x650")
        self.minsize(800, 650)
        self.title('Employee Payroll')
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for f in (StartingPage, AdminPage, EmployeePage, LoginPage):
            frame = f(container, self)
            self.frames[f] = frame
            # frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartingPage)

    def show_frame(self, cont):
        self.clear_frames()
        frame = self.frames[cont]
        frame.pack(side="top", fill=BOTH, expand=True)
        frame.pack_elements()
        frame.setBindings(self)

    def clear_frames(self):
        for cont in self.frames:
            frame = self.frames[cont]
            frame.pack_forget()


class Page():
    def __init__(self, controller):
        self.parentPage = StartingPage
        self.show_toolbar = False
        self.entries = []
        self.bottomButtons = []
        self.controller = controller

        # Configs only work for tk. Use themes for ttk.
        # self.invalidEntryConfig = {'width':200}
        self.entryConfig = {'width': 50}
        self.buttonConfig = {'width':20}

        self.labelPack = {'anchor' : W, 'padx' : 150}
        self.entryPack = {'pady' : (0,5), 'padx' : 150, 'fill' : X}
        self.buttonPack = {'pady' : 5}
        self.actionPack = {'side' : "left", 'pady' : 10, 'padx' : 10}

    def setBindings(self, controller):
        pass

    def goBack(self):
        app.show_frame(self.parentPage)

    def pack_elements(self):
        self.pageTitle.pack(pady=10, padx=10)

        for entry in self.entries:
            label = entry[0]
            label.pack(**self.labelPack)

            if (len(entry) == 2):
                item = entry[1]
                item.pack(**self.entryPack)
                # item.config(**self.entryConfig)

        for button in self.bottomButtons:
            button.pack(**self.buttonPack)
            button.config(**self.buttonConfig)


class StartingPage(Page, ttk.Frame):
    def __init__(self, parent, controller):
        Page.__init__(self, controller)
        ttk.Frame.__init__(self, parent)

        self.pageTitle = ttk.Label(self, text="Welcome to the Payroll System", font=LARGE_FONT)
        #make it top center
        # self.pageTitle.pack(pady=10, padx=10)
        self.loginBtn = ttk.Button(self, text="Login", command=lambda: controller.show_frame(LoginPage))

        self.quitBtn = ttk.Button(self, text="Quit", command=quit)
        
        self.bottomButtons = [self.loginBtn, self.quitBtn]
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

class LoginPage(Page, ttk.Frame):
    def __init__(self, parent, controller):
        Page.__init__(self, controller)
        ttk.Frame.__init__(self, parent)

        self.parentPage = StartingPage

        self.pageTitle = ttk.Label(self, text="Login", font=LARGE_FONT)

        label1 = ttk.Label(self, text="Username")
        self.userName = ttk.Entry(self)
        
        label2 = ttk.Label(self, text="Password")
        self.password = ttk.Entry(self, show = "*")

        self.loginBtn = ttk.Button(self, text="Login", command=lambda: self.login(controller))
        self.backBtn = ttk.Button(self, text="Back", command=lambda: self.goBack())

        self.entries = [(label1, self.userName), (label2, self.password)]
        self.bottomButtons = [self.loginBtn, self.backBtn]

    def setBindings(self, controller):
        self.userName.focus()
        controller.bind("<Return>", self.login)

    def login(self, controller):
        for login in logins:
            if self.userName.get() == login[0] and self.password.get() == login[1]:
                if login[3] == USER_TYPE_EMPLOYEE:
                    app.show_frame(EmployeePage)
                elif login[3] == USER_TYPE_ADMIN:
                    app.show_frame(AdminPage)
                return
        messagebox.showerror("Error", "Invalid username or password")

'''
-----------------ADMIN PAGE-----------------
'''

class AdminPage(Page, ttk.Frame):
    def __init__(self, parent, controller):
        Page.__init__(self, controller)
        ttk.Frame.__init__(self, parent)

        self.pageTitle = ttk.Label(self, text="Admin Page", font=LARGE_FONT)
        self.pageTitle.pack(pady=10, padx=10)

        #add tabs to switch frames
        self.tabControl = ttk.Notebook(self)
        #add tabs with
        addEmpTab = ttk.Frame(self.tabControl)
        viewEmpTab = ttk.Frame(self.tabControl)

        #open add employee page
        self.tabControl.add(addEmpTab, text='Add Employee')
        self.tabControl.add(viewEmpTab, text='View Employee')
        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.bind('<<NotebookTabChanged>>', self.changeTab)

        self.labelPack = {'anchor' : W, 'padx' : 20}
        self.entryPack = {'pady' : (0,5), 'padx' : 20, 'fill' : X}

        column1 = ttk.Frame(addEmpTab)
        column1.pack(pady=10, side="left", expand=1, fill="both")
        column2 = ttk.Frame(addEmpTab)
        column2.pack(pady=10, side="left", expand=1, fill="both")

        '''
        -----------------ADD EMPLOYEE-----------------
        '''

        fNameLbl = ttk.Label(column1, text="First Name")
        self.fName = ttk.Entry(column1)

        lNameLbl = ttk.Label(column1, text="Last Name")
        self.lName = ttk.Entry(column1)

        streetLbl = ttk.Label(column1, text="Street")
        self.street = ttk.Entry(column1)

        cityLbl = ttk.Label(column1, text="City")
        self.city = ttk.Entry(column1)

        stateLbl = ttk.Label(column1, text="State")
        self.state = ttk.Entry(column1)

        zipLbl = ttk.Label(column1, text="Zip Code")
        self.zip = ttk.Entry(column1)

        titleLbl = ttk.Label(column2, text="Title")
        self.title = ttk.Entry(column2)

        amountLbl = ttk.Label(column2, text="Amount")
        self.amount = ttk.Entry(column2)

        # salaryLbl = ttk.Label(column2, text="Salary")
        # self.salary = ttk.Entry(column2)

        # commissionLbl = ttk.Label(column2, text="Commission")
        # self.commission = ttk.Entry(column2)

        # hourlyLbl = ttk.Label(column2, text="Hourly")
        # self.hourly = ttk.Entry(column2)

        dobLbl = ttk.Label(column1, text="Date of Birth")
        self.dob = ttk.Entry(column1)

        startDateLbl = ttk.Label(column2, text="Start Date")
        self.startDate = ttk.Entry(column2)

        accountLbl = ttk.Label(column2, text="Account Number")
        self.account = ttk.Entry(column2)

        routingLbl = ttk.Label(column2, text="Routing Number")
        self.routing = ttk.Entry(column2)

        permsLbl = ttk.Label(column2, text="Permissions")
        self.perms = ttk.Entry(column2)

        deptLbl = ttk.Label(column2, text="Department")
        self.dept = ttk.Entry(column2)

        emailLbl = ttk.Label(column1, text="Office Email")
        self.email = ttk.Entry(column1)

        phoneLbl = ttk.Label(column1, text="Office Phone")
        self.phone = ttk.Entry(column1)

        self.addEmpBtn = ttk.Button(self, text="Add Employee", style="Accent.TButton")
        
        # Classification Dropdown
        classificationLbl = ttk.Label(column2, text="Classification")
        self.classification = StringVar()
        self.classSelect = ttk.Combobox(column2, textvariable=self.classification)
        self.classSelect['values'] = ['Salary', 'Commission', 'Hourly']
        self.classSelect.state(['readonly'])

        # Department Dropdown
        deptLbl = ttk.Label(column2, text="Department")
        self.dept = StringVar()
        self.deptSelect = ttk.Combobox(column2, textvariable=self.dept)
        self.deptSelect['values'] = ['Accounting', 'Development', 'Sales', 'Customer Service']
        self.deptSelect.state(['readonly'])
        
        #option menu for classification(salaried, hourly, commisioned)
        # label7 = ttk.Label(column2, text="Classification")
        # self.classification = ttk.Entry(column2)

        '''
        -----------------VIEW EMPLOYEE-----------------
        '''
        #create a search bar
        searchLbl = ttk.Label(viewEmpTab, text="Search")
        self.search = ttk.Entry(viewEmpTab)

        self.entries = [
            (fNameLbl, self.fName),
            (lNameLbl, self.lName),
            (streetLbl, self.street),
            (cityLbl, self.city),
            (stateLbl, self.state),
            (zipLbl, self.zip),
            (dobLbl, self.dob),
            (emailLbl, self.email),
            (phoneLbl, self.phone),
            (titleLbl, self.title),
            (classificationLbl, self.classSelect),
            (amountLbl, self.amount),
            # (salaryLbl, self.salary),
            # (commissionLbl, self.commission),
            # (hourlyLbl, self.hourly),
            (startDateLbl, self.startDate),
            (accountLbl, self.account),
            (routingLbl, self.routing),
            (permsLbl, self.perms),
            (deptLbl, self.deptSelect),
            (searchLbl, self.search)
        ]

        #put logout button on the top right
        self.logoutBtn = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(StartingPage))
        self.logoutBtn.pack(side="right", padx=10, pady=10)

    def changeTab(self, *args):
        tab = self.tabControl.index(self.tabControl.select())
        if tab == 0:
            self.addEmpBtn.pack(**self.actionPack)
        if tab == 1:
            self.addEmpBtn.pack_forget()

    def setBindings(self, controller):
        self.fName.focus()
        # controller.bind("<Return>", self.login)

    def getForm(self):
        add_employee(1, self.fName.get(), self.lName.get(), self.street.get(), self.city.get(), self.state.get(), self.zip.get())
        print(EMPLOYEES)

'''
-----------------EMPLOYEE PAGE-----------------
'''

class EmployeePage(Page, ttk.Frame):
    def __init__(self, parent, controller):
        Page.__init__(self, controller)
        ttk.Frame.__init__(self, parent)
        self.pageTitle = ttk.Label(self, text="Employee Page", font=LARGE_FONT)
        self.pageTitle.pack(pady=10, padx=10)

        saveIcon = PhotoImage(file = os.path.join(os.path.dirname(__file__), 'icons', 'save.png'))
        # editIcon = PhotoImage(file = "path_of_file")


        #add tabs to switch frames
        self.tabControl = ttk.Notebook(self)
        #add tabs with
        profileTab = ttk.Frame(self.tabControl)
        directoryTab = ttk.Frame(self.tabControl)
        self.tabControl.add(profileTab, text='Profile')
        self.tabControl.add(directoryTab, text='Directory')
        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.bind('<<NotebookTabChanged>>', self.changeTab)

        self.labelPack = {'anchor' : W, 'padx' : 20}
        self.entryPack = {'pady' : (0,5), 'padx' : 20, 'fill' : X}

        infoColumn = ttk.Labelframe(profileTab, text='Personal Information')
        infoColumn.pack(padx=10, pady=10, ipady=30, side="left", fill="both")

        payStubColumn = ttk.Labelframe(profileTab, text='Pay Stub')
        payStubColumn.pack(padx=10, pady=10, ipady=30, side="left", expand=1, fill="both")
        self.saveBtn = ttk.Button(self, text="Save", style="Accent.TButton", image=saveIcon)

        #put logout button on the top right
        self.logoutBtn = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(StartingPage))
        self.logoutBtn.pack(side="right", padx=10, pady=10)

        # button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(AdminPage))
        # button1.pack()
        '''
        -----------------PROFILE TAB-----------------
        '''

        #inner padding not working so use blank label
        blankInfo = ttk.Label(infoColumn, text="")
        
        fNameLbl = ttk.Label(infoColumn, text="First Name")
        self.fName = ttk.Entry(infoColumn, width=30)

        lNameLbl = ttk.Label(infoColumn, text="Last Name")
        self.lName = ttk.Entry(infoColumn, width=30)

        streetLbl = ttk.Label(infoColumn, text="Street")
        self.street = ttk.Entry(infoColumn, width=30)

        cityLbl = ttk.Label(infoColumn, text="City")
        self.city = ttk.Entry(infoColumn, width=30)

        stateLbl = ttk.Label(infoColumn, text="State")
        self.state = ttk.Entry(infoColumn, width=30)

        zipLbl = ttk.Label(infoColumn, text="Zip Code")
        self.zip = ttk.Entry(infoColumn)

        titleLbl = ttk.Label(infoColumn, text="Title")
        self.title = ttk.Entry(infoColumn)
        
        blankPay = ttk.Label(payStubColumn, text="")

        payStubLbl = ttk.Label(payStubColumn, text="PayStub")
        self.payStub = ttk.Entry(payStubColumn)

        amountLbl = ttk.Label(payStubColumn, text="Amount")
        self.amount = ttk.Entry(payStubColumn)


        self.entries = [
            (blankInfo,),
            (fNameLbl, self.fName),
            (lNameLbl, self.lName),
            (streetLbl, self.street),
            (cityLbl, self.city),
            (stateLbl, self.state),
            (zipLbl, self.zip),
            (titleLbl, self.title),
            (blankPay,),
            (payStubLbl, self.payStub),
            (amountLbl, self.amount)
        ]


    def changeTab(self, *args):
        tab = self.tabControl.index(self.tabControl.select())
        if tab == 0:
            self.saveBtn.pack(**self.actionPack)
        if tab == 1:
            self.saveBtn.pack_forget()

    def setBindings(self, controller):
        self.fName.focus()

    def getForm(self):
        add_employee(1, self.fName.get(), self.lName.get(), self.street.get(), self.city.get(), self.state.get(), self.zip.get())
        print(EMPLOYEES)

'''
class AddEmployeePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Add Employee", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
    
        label1 = ttk.Label(self, text="First Name")
        label1.pack()

        entry1 = ttk.Entry(self)
        entry1.pack()

        label2 = ttk.Label(self, text="Last Name")
        label2.pack()

        entry2 = ttk.Entry(self)
        entry2.pack()

        label3 = ttk.Label(self, text="Address")
        label3.pack()

        entry3 = ttk.Entry(self)
        entry3.pack()

        label4 = ttk.Label(self, text="City")
        label4.pack()

        entry4 = ttk.Entry(self)
        entry4.pack()

        label5 = ttk.Label(self, text="State")
        label5.pack()

        entry5 = ttk.Entry(self)
        entry5.pack()

        label6 = ttk.Label(self, text="Zipcode")
        label6.pack()

        entry6 = ttk.Entry(self)
        entry6.pack()

        #option menu for classification(salaried, hourly, commisioned)
        label7 = ttk.Label(self, text="Classification")
        label7.pack()

        entry7 = ttk.Entry(self)
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