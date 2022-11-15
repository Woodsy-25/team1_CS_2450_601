'''
This is the main program that curretly holds both the code from the employee project and also hold the code for the GUI.
'''


import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, messagebox
from payroll import *
import pandas as pd
from operator import itemgetter
import payroll
import tkinter as tk
from idlelib.tooltip import Hovertip
import sv_ttk

#the payroll code
LARGE_FONT = ('Verdana', 20) # specify font and size
MEDIUM_FONT = ('Verdana', 15)
USER_TYPE_EMPLOYEE = '1'
USER_TYPE_ADMIN = '2'
BTN_WIDTH = 12

class PayrollApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #size of the window
        tk.Tk.geometry(self, "800x650")
        self.minsize(800, 650)
        self.title('Employee Payroll')
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.employeeID = 0
        self.currentUser = None
        self.previousPage = StartingPage
        self.currentPage = StartingPage
        self.frames = {}

        # Theming 
        self.color1 = "#fafafa"
        self.color2 = "#e7e7e7"
        self.color3 = "#5f5f5f"

        for page in (StartingPage, LoginPage, HelpPage):
            self.init_frame(page)   

        self.show_frame(StartingPage)

    def init_frame(self, page):
        frame = page(self.container, self)
        self.frames[page] = frame

    def show_frame(self, page):
        self.previousPage = self.currentPage
        self.currentPage = page
        self.clear_frames()
        frame = self.frames[page]
        frame.pack(side="top", fill=BOTH, expand=True)
        frame.pack_elements()
        frame.setBindings(self)

    def go_back(self):
        self.show_frame(self.previousPage)

    def clear_frames(self):
        for cont in self.frames:
            frame = self.frames[cont]
            frame.pack_forget()

    def toggleTheme(self):
        sv_ttk.toggle_theme()

        if sv_ttk.get_theme() == "dark":
            self.color1 = "#1c1c1c"
            self.color2 = "#2f2f2f"
            self.color3 = "#d4d4d4"
        else:
            self.color1 = "#fafafa"
            self.color2 = "#e7e7e7"
            self.color3 = "#5f5f5f"


class Page(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.parentPage = StartingPage
        self.show_toolbar = False
        self.entries = {}
        self.bottomButtons = []
        self.app = controller

        # Configs only work for tk. Use themes for ttk.
        # self.invalidEntryConfig = {'width':200}
        self.entryConfig = {'width': 50}
        

        self.labelPack = {'anchor' : W, 'padx' : 200}
        self.entryPack = {'pady' : (0,5), 'padx' : 200, 'fill' : X}
        self.buttonPack = {'pady' : 5}
        self.actionPack = {'side' : "left", 'pady' : 10, 'padx' : (10, 0)}


    def basicEntries(self, parent):
        self.fNameLbl = ttk.Label(parent, text="First Name")
        self.fName = ttk.Entry(parent, width=30)

        self.lNameLbl = ttk.Label(parent, text="Last Name")
        self.lName = ttk.Entry(parent, width=30)

        self.streetLbl = ttk.Label(parent, text="Street")
        self.street = ttk.Entry(parent, width=30)

        self.cityLbl = ttk.Label(parent, text="City")
        self.city = ttk.Entry(parent, width=30)

        self.stateLbl = ttk.Label(parent, text="State")
        self.state = ttk.Entry(parent, width=30)

        self.zipLbl = ttk.Label(parent, text="Zip Code")
        self.zip = ttk.Entry(parent)

        self.titleLbl = ttk.Label(parent, text="Title")
        self.title = ttk.Entry(parent)

        
    def setBindings(self, controller):
        pass

    def pack_elements(self):
        self.labelConfig = {'font':("Arial", 8), 'foreground': self.app.color3}
        self.pageTitle.pack(pady=10, padx=10)

        for label, entry in self.entries.items():
            label.config(**self.labelConfig)
            label.pack(**self.labelPack)

            if entry != None:
                entry.pack(**self.entryPack)

        for button in self.bottomButtons:
            button.pack(**self.buttonPack)
            button.config(width=BTN_WIDTH)

    def logout(self, *args):
        confirm = messagebox.askyesno('Confirm', 'Are you sure you want to log out?')
        if confirm:
            self.app.show_frame(StartingPage)


class StartingPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        self.pageTitle = ttk.Label(self, text="Welcome to the Payroll System", font=LARGE_FONT)

        self.loginBtn = ttk.Button(self, text="Login", command=lambda: self.showLogin())

        self.quitBtn = ttk.Button(self, text="Quit", command=quit)
        
        self.bottomButtons = [self.loginBtn, self.quitBtn]
        #toggle themes
        theme_button = ttk.Button(self, text="Toggle Theme", command=controller.toggleTheme)
        theme_button.pack(side = BOTTOM)

    def setBindings(self, controller):
        self.loginBtn.focus()
        controller.bind("<Return>", self.showLogin)

    def showLogin(self, *args):
        self.app.show_frame(LoginPage)


class HelpPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        self.parentPage
        self.pageTitle = ttk.Label(self, text="Help Page", font=LARGE_FONT)

        self.help = ttk.Label(self, text="(Helpful information will be displayed here)", font=MEDIUM_FONT)
        self.entries = {self.help: None}

        self.backBtn = ttk.Button(self, text="Back", command=lambda: controller.go_back())

        self.bottomButtons = [self.backBtn]



'''
-----------------LOGIN PAGE-----------------
'''

class LoginPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        self.parentPage = StartingPage
        self.pageTitle = ttk.Label(self, text="Login", font=LARGE_FONT)

        label1 = ttk.Label(self, text="Username")
        self.userName = ttk.Entry(self)
        
        label2 = ttk.Label(self, text="Password")
        self.password = ttk.Entry(self, show = "*")

        self.loginBtn = ttk.Button(self, text="Login", command=lambda: self.login())
        self.backBtn = ttk.Button(self, text="Back", command=lambda: controller.go_back())

        self.entries = {label1: self.userName, label2: self.password}
        self.bottomButtons = [self.loginBtn, self.backBtn]

    def setBindings(self, controller):
        self.userName.focus()
        controller.bind("<Return>", self.login)

    def login(self, *args):
        for login in logins:
            if self.userName.get() == login[0] and self.password.get() == login[1]:
                employeeID = login[2]
                self.app.currentUser = payroll.find_employee_by_id(employeeID)
                if login[3] == USER_TYPE_EMPLOYEE:
                    self.app.init_frame(EmployeePage)
                    self.app.show_frame(EmployeePage)
                elif login[3] == USER_TYPE_ADMIN:
                    self.app.init_frame(AdminPage)
                    self.app.show_frame(AdminPage)
                self.userName.delete(0,END)
                self.password.delete(0,END)
                return
        messagebox.showerror("Error", "Invalid username or password")

'''
-----------------ADMIN PAGE-----------------
'''

class AdminPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        self.pageTitle = ttk.Label(self, text="Admin Page", font=LARGE_FONT)
        self.pageTitle.pack(pady=10, padx=10)

        self.action = 'NEW'

        #add tabs to switch frames
        self.tabControl = ttk.Notebook(self)
        #add tabs with
        self.manageEmpTab = ttk.Frame(self.tabControl)
        self.editEmpTab = ttk.Frame(self.tabControl)
        self.searchEmpTab = searchFrame(self.tabControl, controller)

        #open add employee page
        self.tabControl.add(self.manageEmpTab, text='Add Employee')
        self.tabControl.add(self.searchEmpTab, text='Search Employees')
        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.bind('<<NotebookTabChanged>>', self.changeTab)

        self.labelPack = {'anchor' : W, 'padx' : 20}
        self.entryPack = {'pady' : (0,5), 'padx' : 20, 'fill' : X}

        #put logout button on the top right
        self.logoutBtn = ttk.Button(self, text="Logout", width=BTN_WIDTH, command=lambda: self.logout())
        self.logoutBtn.pack(side="right", padx=10, pady=10)

        self.helpBtn = ttk.Button(self, text="?", width=2, command=lambda: controller.show_frame(HelpPage))
        self.helpBtn.pack(side="right", pady=10)
        helpBtnTip = Hovertip(self.helpBtn,'Help')



        '''
        -----------------MANAGE EMPLOYEE-----------------
        '''
        self.addColumns(self.manageEmpTab)
        self.addEntries()
        self.saveBtn = ttk.Button(self, text="Save", width=BTN_WIDTH, style="Accent.TButton", command=lambda: self.saveEmployee())
        self.cancelBtn = ttk.Button(self, text="Cancel", width=BTN_WIDTH, command=lambda: self.cancelEdit())

        saveBtnTip = Hovertip(self.saveBtn,'Add Employee')

        '''
        -----------------SEARCH EMPLOYEES-----------------
        '''
        tableColumns = {"First Name":"first_name", "Last Name":"last_name", "ID":"id", "Office Email":"office_email", "Office Phone":"office_phone", "Title":"title", "Department":"dept"}
        self.searchEmpTab.setTableColumns(tableColumns)
        self.searchEmpTab.initializeTable()
        self.exportBtn = ttk.Button(self, text="Export CSV", width=BTN_WIDTH, command=lambda: self.exportCSV())


    def addColumns(self, parent):
        self.column1 = ttk.Frame(parent)
        self.column1.pack(pady=10, side="left", expand=1, fill="both")
        self.column2 = ttk.Frame(parent)
        self.column2.pack(pady=10, side="left", expand=1, fill="both")

    def addEntries(self):
        self.fNameLbl = ttk.Label(self.column1, text="First Name")
        self.fName = ttk.Entry(self.column1)

        self.lNameLbl = ttk.Label(self.column1, text="Last Name")
        self.lName = ttk.Entry(self.column1)

        self.streetLbl = ttk.Label(self.column1, text="Street")
        self.street = ttk.Entry(self.column1)

        self.cityLbl = ttk.Label(self.column1, text="City")
        self.city = ttk.Entry(self.column1)

        self.stateLbl = ttk.Label(self.column1, text="State")
        self.state = ttk.Entry(self.column1)

        self.zipLbl = ttk.Label(self.column1, text="Zip Code")
        self.zip = ttk.Entry(self.column1)

        self.titleLbl = ttk.Label(self.column2, text="Title")
        self.title = ttk.Entry(self.column2)

        self.dobLbl = ttk.Label(self.column1, text="Date of Birth")
        self.dob = ttk.Entry(self.column1)

        self.amountLbl = ttk.Label(self.column2, text="Amount")
        self.amount = ttk.Entry(self.column2)

        self.ssnLbl = ttk.Label(self.column2, text="SSN")
        self.ssn = ttk.Entry(self.column2)

        self.startDateLbl = ttk.Label(self.column2, text="Start Date")
        self.startDate = ttk.Entry(self.column2)

        self.accountLbl = ttk.Label(self.column2, text="Account Number")
        self.account = ttk.Entry(self.column2)

        self.routingLbl = ttk.Label(self.column2, text="Routing Number")
        self.routing = ttk.Entry(self.column2)

        self.emailLbl = ttk.Label(self.column1, text="Office Email")
        self.email = ttk.Entry(self.column1)

        self.phoneLbl = ttk.Label(self.column1, text="Office Phone")
        self.phone = ttk.Entry(self.column1)

        # Classification Dropdown
        self.classificationLbl = ttk.Label(self.column2, text="Classification")
        self.classification = StringVar()
        self.classSelect = ttk.Combobox(self.column2, textvariable=self.classification)
        self.classSelect['values'] = ['Salary', 'Commission', 'Hourly']
        self.classSelect.state(['readonly'])

        # Department Dropdown
        self.deptLbl = ttk.Label(self.column2, text="Department")
        self.dept = StringVar()
        self.deptSelect = ttk.Combobox(self.column2, textvariable=self.dept)
        self.deptSelect['values'] = ['Engineering', 'Finance', 'HR', 'IT',  'Legal', 'Marketing', 'Operations',  'Sales']
        self.deptSelect.state(['readonly'])

        # Permissions Dropdown
        self.permsLbl = ttk.Label(self.column2, text="Permissions")
        self.perms = StringVar()
        self.permSelect = ttk.Combobox(self.column2, textvariable=self.perms)
        self.permSelect['values'] = ['Admin', 'Employee']
        self.permSelect.state(['readonly'])

        self.entries = {
            self.fNameLbl: self.fName,
            self.lNameLbl: self.lName,
            self.streetLbl: self.street,
            self.cityLbl: self.city,
            self.stateLbl: self.state,
            self.zipLbl: self.zip,
            self.dobLbl: self.dob,
            self.emailLbl: self.email,
            self.phoneLbl: self.phone,
            self.titleLbl: self.title,
            self.ssnLbl: self.ssn,
            self.classificationLbl: self.classSelect,
            self.amountLbl: self.amount,
            self.startDateLbl: self.startDate,
            self.accountLbl: self.account,
            self.routingLbl: self.routing,
            self.permsLbl: self.permSelect,
            self.deptLbl: self.deptSelect
        }

    def changeTab(self, *args):
        tab = self.tabControl.index(self.tabControl.select())
        if tab == 0:
            self.exportBtn.pack_forget()
            self.cancelBtn.pack(**self.actionPack)
            self.saveBtn.pack(**self.actionPack)
        if tab == 1:
            self.searchEmpTab.loadSearchData()
            self.cancelBtn.pack_forget()
            self.saveBtn.pack_forget()
            self.exportBtn.pack(**self.actionPack)

    def addEmployee(self):
        if self.validateForm:
            payroll.add_employee(self.fName.get(), self.lName.get(), self.street.get(), self.city.get(), self.state.get(), self.zip.get(), self.classification.get(), self.amount.get(), self.dob.get(), self.ssn.get(), self.startDate.get(), self.account.get(), self.routing.get(), self.perms.get(), self.title.get(), self.dept.get(), self.email.get(), self.phone.get())

            messagebox.showinfo(message='Employee Added Successfully')

    def editEmployee(self, emp):
        self.action = 'EDIT'
        self.tabControl.tab(self.manageEmpTab, text='Edit Employee')

        setEntry(self.fName, emp.get_first_name())
        setEntry(self.lName, emp.get_last_name())
        setEntry(self.street, emp.get_street())
        setEntry(self.city, emp.get_city())
        setEntry(self.state, emp.get_state())
        setEntry(self.zip, emp.get_zip())
        setEntry(self.title, emp.get_title())
        setEntry(self.email, emp.get_office_email())
        setEntry(self.phone, emp.get_office_phone())
        setEntry(self.dob, emp.get_dob())
        setEntry(self.ssn, emp.get_ssn())

        # Set classification dropdown
        classification = emp.get_classification()
        amount = ""
        if isinstance(classification, payroll.Salaried):
            classification = 0
            amount = emp.get_salary()
        elif isinstance(classification, payroll.Commisioned):
            classification = 1
            amount = emp.get_commission()
        elif isinstance(classification, payroll.Hourly):
            classification = 2
            amount = emp.get_hourly()
        self.classSelect.current(classification)
        setEntry(self.amount, amount)

        # Set department dropdown
        dept = emp.get_dept()
        for i in range(0, len(self.deptSelect['values'])):
            if self.deptSelect['values'][i] == dept:
                self.deptSelect.current(i)

        # Set permissions dropdown
        perms = emp.get_permissions()
        if perms == '1':
            self.permSelect.current(1)
        elif perms == '2':
            self.permSelect.current(0)

        setEntry(self.startDate, emp.get_start_date())
        setEntry(self.account, emp.get_account())
        setEntry(self.routing, emp.get_routing_num())

        self.tabControl.select(self.manageEmpTab) 


    def updateEmployee(self):
        if self.validateForm():
            #TODO: Update employee
            messagebox.showinfo(message='Employee Updated Successfully')
            self.tabControl.tab(self.manageEmpTab, text='Add Employee')
            saveBtnTip = Hovertip(self.saveBtn,'Add Employee')

            self.tabControl.select(self.searchEmpTab)
            for entry in self.entries.values():
                entry.delete(0,END)

    def saveEmployee(self):
        if self.action == 'NEW':
            self.addEmployee()
        elif self.action == 'EDIT':
            self.updateEmployee()

    def cancelEdit(self):
        confirm = messagebox.askyesno('Are you sure?', 'Changes will be lost')
        if confirm:
            for entry in self.entries.values():
                entry.delete(0,END)

            if self.action == 'EDIT':
                self.tabControl.tab(self.manageEmpTab, text='Add Employee')
                self.tabControl.select(self.searchEmpTab)


    def validateForm(self):
        #TODO: make sure all required entries are filled and valid
        return True

    def exportCSV(self):
        print('EXPORTING')

    def setBindings(self, controller):
        self.fName.focus()
        # controller.bind("<Return>", self.login)

'''
-----------------EMPLOYEE PAGE-----------------
'''

class EmployeePage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        self.pageTitle = ttk.Label(self, text="Employee Page", font=LARGE_FONT)
        self.pageTitle.pack(pady=10, padx=10)

        #add tabs to switch frames
        self.tabControl = ttk.Notebook(self)
        #add tabs with
        profileTab = ttk.Frame(self.tabControl)
        self.searchEmpTab = searchFrame(self.tabControl, controller)
        self.tabControl.add(profileTab, text='Profile')
        self.tabControl.add(self.searchEmpTab, text='Directory')
        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.bind('<<NotebookTabChanged>>', self.changeTab)

        self.labelPack = {'anchor' : W, 'padx' : 20}
        self.entryPack = {'pady' : (0,5), 'padx' : 20, 'fill' : X}

        infoColumn = ttk.Labelframe(profileTab, text='Personal Information')
        infoColumn.pack(padx=10, pady=10, ipady=30, side="left", fill="both")

        payStubColumn = ttk.Labelframe(profileTab, text='Pay Stub')
        payStubColumn.pack(padx=10, pady=10, ipady=30, side="left", expand=1, fill="both")
        self.editBtn = ttk.Button(self, text="Edit", width=BTN_WIDTH, command=lambda: self.editPersonalInfo())
        self.saveBtn = ttk.Button(self, text="Save", width=BTN_WIDTH, style="Accent.TButton", command=lambda: self.savePersonalInfo())

        editBtnTip = Hovertip(self.editBtn,'Edit Personal Information')
        saveBtnTip = Hovertip(self.saveBtn,'Save Personal Information')

        self.cancelBtn = ttk.Button(self, text="Cancel", width=BTN_WIDTH, command=lambda: self.loadPersonalInfo())

        #put logout button on the bottom right
        self.logoutBtn = ttk.Button(self, text="Logout", width=BTN_WIDTH, command=lambda: self.logout())
        self.logoutBtn.pack(side="right", padx=10, pady=10)

        self.helpBtn = ttk.Button(self, text="?", width=2, command=lambda: controller.show_frame(HelpPage))
        self.helpBtn.pack(side="right", pady=10)
        helpBtnTip = Hovertip(self.helpBtn,'Help')

        # button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(AdminPage))
        # button1.pack()
        '''
        -----------------PROFILE TAB-----------------
        '''

        #inner padding not working so use blank label
        blankInfo = ttk.Label(infoColumn, text="")
        
        self.fNameLbl = ttk.Label(infoColumn, text="First Name")
        self.fName = ttk.Entry(infoColumn, width=30)

        self.lNameLbl = ttk.Label(infoColumn, text="Last Name")
        self.lName = ttk.Entry(infoColumn, width=30)

        self.streetLbl = ttk.Label(infoColumn, text="Street")
        self.street = ttk.Entry(infoColumn, width=30)

        self.cityLbl = ttk.Label(infoColumn, text="City")
        self.city = ttk.Entry(infoColumn, width=30)

        self.stateLbl = ttk.Label(infoColumn, text="State")
        self.state = ttk.Entry(infoColumn, width=30)

        self.zipLbl = ttk.Label(infoColumn, text="Zip Code")
        self.zip = ttk.Entry(infoColumn)

        self.titleLbl = ttk.Label(infoColumn, text="Title")
        self.title = ttk.Entry(infoColumn)
        
        blankPay = ttk.Label(payStubColumn, text="")

        #TODO: Put actual paystub info in here. Make them labels.
        self.payStubLbl = ttk.Label(payStubColumn, text="PayStub")
        self.payStub = ttk.Entry(payStubColumn, state=DISABLED)

        self.amountLbl = ttk.Label(payStubColumn, text="Amount")
        self.amount = ttk.Entry(payStubColumn, state=DISABLED)

        '''
        -----------------DIRECTORY TAB-----------------
        '''

        self.searchEmpTab.initializeTable()

        self.entries = {
            blankInfo: None,
            self.fNameLbl: self.fName,
            self.lNameLbl: self.lName,
            self.streetLbl: self.street,
            self.cityLbl: self.city,
            self.stateLbl: self.state,
            self.zipLbl: self.zip,
            self.titleLbl: self.title,
            blankPay: None,
            self.payStubLbl: self.payStub,
            self.amountLbl: self.amount
        }

        self.personalInfo = [
            self.fName,
            self.lName,
            self.street,
            self.city,
            self.state,
            self.zip,
            self.title
        ]

    def changeTab(self, *args):
        tab = self.tabControl.index(self.tabControl.select())
        if tab == 0:
            self.loadPersonalInfo()
        if tab == 1:
            self.searchEmpTab.loadSearchData()
            self.editBtn.pack_forget()
            self.cancelBtn.pack_forget()
            self.saveBtn.pack_forget()

    def loadPersonalInfo(self, *args):
        emp = self.app.currentUser
        setEntry(self.fName, emp.get_first_name())
        setEntry(self.lName, emp.get_last_name())
        setEntry(self.street, emp.get_street())
        setEntry(self.city, emp.get_city())
        setEntry(self.state, emp.get_state())
        setEntry(self.zip, emp.get_zip())
        setEntry(self.title, emp.get_title())
        for item in self.personalInfo:
            item.config(state=DISABLED) # or 'readonly'?

        self.editBtn.pack_forget()
        self.cancelBtn.pack_forget()
        self.saveBtn.pack_forget()
        self.editBtn.pack(**self.actionPack)


    def editPersonalInfo(self, *args):
        for item in self.personalInfo:
            item.config(state=NORMAL)
            self.editBtn.pack_forget()
            self.cancelBtn.pack(**self.actionPack)        
            self.saveBtn.pack(**self.actionPack)        
            
    def savePersonalInfo(self, *args):
        if (self.validateForm()):
            for item in self.personalInfo:
                item.config(state=DISABLED)
                self.cancelBtn.pack_forget()
                self.saveBtn.pack_forget()
                self.editBtn.pack(**self.actionPack)
            
            emp = self.app.currentUser
            emp.set_first_name(self.fName.get())
            emp.set_last_name(self.lName.get())
            emp.set_street(self.street.get())
            emp.set_city(self.city.get())
            emp.set_state(self.state.get())
            emp.set_zip(self.zip.get())
            emp.set_title(self.title.get())

    def validateForm(self):
        return True

    def setBindings(self, controller):
        # self.fName.focus()
        pass


class searchFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.app = controller

        self.parentPage = parent.master

        self.tableColumns = {"First Name":"first_name", "Last Name":"last_name", "ID":"id", "Office Email":"office_email", "Office Phone":"office_phone"}
        style_tree = ttk.Style()
        # style_tree.map("t_style.Treeview", background=[("selected", "green")])
        style_tree.configure("t_style.Treeview", rowheight=25)
        # style_tree.configure("t_style.Treeview.Heading",  font=('calibri', 16))
    
        #create a search bar
        search_frame = tk.Frame(self)
        search_frame.pack(fill=X)
        searchLbl = ttk.Label(search_frame, text="Search", font=("Arial", 8), foreground=self.app.color3)
        searchLbl.pack(anchor=W, padx= 10, pady=(5,0))
        self.searchBar = ttk.Entry(search_frame)
        self.searchBar.pack(pady=(0,5), padx=(10,5), side='left', expand=1, fill=X)
        self.searchBar.bind("<KeyRelease>", self.loadSearchData)

        # Search Filter Dropdown
        self.clicked = tk.StringVar()
        self.filterDrop = ttk.Combobox(search_frame, textvariable=self.clicked)
        self.filterDrop.pack(pady=(0,5), padx=(5,10), side='left', fill=X)
        self.filterDrop.state(['readonly'])

        table_frame = tk.Frame(self)
        table_frame.pack(expand=1, fill=BOTH)

        self.tree = ttk.Treeview(table_frame, style="t_style.Treeview")
        self.tree.bind("<Double-1>", self.showEmpData)
        # self.tree.bind("<<TreeviewSelect>>", self.showEmpData)
        self.tree.place(relheight=1, relwidth=.96, x=10)

        scrollY = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side="right", fill="y")


    def initializeTable(self):
        self.columnHeaders = list(self.tableColumns.keys())
        self.columnNames = list(self.tableColumns.values())
        self.clicked.set(str(self.columnHeaders[0]))
        self.filterDrop['values'] = self.columnHeaders

        csvData = pd.read_csv(payroll.EMPLOYEES_FILE)
        self.df = csvData.loc[:, self.columnNames]
        self.df = self.df.sort_values(by="first_name")
        self.tree["column"] = self.columnHeaders
        self.tree["show"] = "headings"

        # Set column headers
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            if column == 'ID':
                # Hide ID column
                self.tree.column(column, minwidth=0, width=0, stretch=NO)
            elif column == "Office Email":
                self.tree.column(column, minwidth=50, width=150, stretch=YES)
            else:
                self.tree.column(column, minwidth=50, width=100, stretch=YES)

    def setTableColumns(self, columns):
        self.tableColumns = columns

    def loadSearchData(self, event=None):
        # Clear Data
        self.tree.delete(*self.tree.get_children())

        le = len(self.searchBar.get())

        self.tree.tag_configure('odd_row', background=self.app.color1)
        self.tree.tag_configure('even_row', background=self.app.color2)
        if le == 0:
            df_rows = self.df.to_numpy().tolist()
            self.insertRows(df_rows)
        else:
            s_key = self.columnHeaders.index(str(self.clicked.get()))
            s_list = []
            df_rows = self.df.to_numpy().tolist()
            for row in df_rows:
                val = row[s_key]
                if self.searchBar.get().lower() == val[0:le].lower():
                    s_list.append(row)
            s_list = sorted(s_list, key=itemgetter(s_key))
            self.insertRows(s_list)
        
    def insertRows(self, rows):
        count = 0
        for row in rows:
            if count % 2 == 0:
                self.tree.insert("", "end", values=row, tags=("even_row",))
            else:
                self.tree.insert("", "end", values=row, tags=("odd_row",))
            count += 1

    def showEmpData(self, event):
        #TODO: Restructure this
        self.empWindow = Toplevel(self)
        self.empWindow.title("Employee Information")
        self.empWindow.geometry("300x350")
        curItem = self.tree.focus()
        rowValues = self.tree.item(curItem)['values']
        fName = rowValues[0]
        lName = rowValues[1]
        empID = rowValues[2]
        Label(self.empWindow, text =f"{fName} {lName}", font=MEDIUM_FONT).pack()

        selectedEmp = payroll.find_employee_by_id(empID)

            
        #TODO: Don't actually show this information. Just for testing.
        ttk.Label(self.empWindow, text="Title", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.title = ttk.Entry(self.empWindow)
        self.title.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(self.empWindow, text="Department", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.dept = ttk.Entry(self.empWindow)
        self.dept.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(self.empWindow, text="Office Email", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.email = ttk.Entry(self.empWindow)
        self.email.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(self.empWindow, text="Office Phone", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.phone = ttk.Entry(self.empWindow)
        self.phone.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)

        self.personalInfo = [
            self.title,
            self.dept,
            self.email,
            self.phone,
        ]

        setEntry(self.title, selectedEmp.get_title())
        setEntry(self.dept, selectedEmp.get_dept())
        setEntry(self.email, selectedEmp.get_office_email())
        setEntry(self.phone, selectedEmp.get_office_phone())

        for item in self.personalInfo:
            item.config(state=DISABLED) # or 'readonly'?

        if self.app.currentPage == AdminPage:
            editBtn = ttk.Button(self.empWindow, text="Edit", width=BTN_WIDTH, style="Accent.TButton", command=lambda: self.editEmployee(selectedEmp))
            editBtn.pack(pady = 10, padx=10)
            #TODO: Add option to deactivate employee
    
    def editEmployee(self, emp):
        self.parentPage.editEmployee(emp)
        self.empWindow.destroy()

def setEntry(entry, text):
    entry.delete(0,END)
    entry.insert(0,text)

#making a list from logins.csv
with open('logins.csv', 'r') as f:
    #skip the first line
    next(f)
    #make a list of lists
    logins = [line.strip().split(',') for line in f]


def main():
    # Load employee payroll data from CSV
    payroll.load_employees()
    payroll.process_timecards()
    payroll.process_receipts()
    payroll.run_payroll()

    #open app
    app = PayrollApp()
    sv_ttk.set_theme('light')
    app.mainloop()

    # # Save copy of payroll file; delete old file
    # shutil.copyfile(PAY_LOGFILE, 'paylog_old.txt')
    # if os.path.exists(PAY_LOGFILE):
    #     os.remove(PAY_LOGFILE)

    # # Change Issie Scholard to Salaried by changing the Employee object:
    # payroll = find_employee_by_id('51-4678119')
    # payroll.make_salaried(134386.51)
    # payroll.issue_payment()

    # # Change Reynard,Lorenzin to Commissioned; add some receipts
    # payroll = find_employee_by_id('11-0469486')
    # payroll.make_commissioned(50005.50, 27)
    # clas = payroll.classification
    # clas.add_receipt(1109.73)
    # clas.add_receipt(746.10)
    # payroll.issue_payment()

    # # Change Jed Netti to Hourly; add some hour entries
    # payroll = find_employee_by_id('68-9609244')
    # payroll.make_hourly(47)
    # clas = payroll.classification
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # payroll.issue_payment()

if __name__ == '__main__':
    main()