'''
This is the main program that curretly holds both the code from the employee project and also hold the code for the GUI.
'''


import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, messagebox
from emp import *
import pandas as pd
from operator import itemgetter
import payroll

import sv_ttk
import os

#the payroll code
LARGE_FONT = ('Verdana', 20) # specify font and size
MEDIUM_FONT = ('Verdana', 15)
USER_TYPE_EMPLOYEE = '1'
USER_TYPE_ADMIN = '2'

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
        self.frames = {}

        # Theming
        self.color1 = "#fafafa"
        self.color2 = "#e7e7e7"
        self.color3 = "#5f5f5f"

        # for f in (StartingPage, AdminPage, EmployeePage, LoginPage):
        #     frame = f(container, self)
        #     self.frames[f] = frame
        self.init_frame(StartingPage)
        self.init_frame(LoginPage)

        self.show_frame(StartingPage)

    def init_frame(self, page):
        frame = page(self.container, self)
        self.frames[page] = frame

    def show_frame(self, page):
        self.clear_frames()
        frame = self.frames[page]
        frame.pack(side="top", fill=BOTH, expand=True)
        frame.pack_elements()
        frame.setBindings(self)

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
        self.entries = []
        self.bottomButtons = []
        self.app = controller

        # Configs only work for tk. Use themes for ttk.
        # self.invalidEntryConfig = {'width':200}
        self.entryConfig = {'width': 50}
        self.btnWidth = 12

        self.labelPack = {'anchor' : W, 'padx' : 200}
        self.entryPack = {'pady' : (0,5), 'padx' : 200, 'fill' : X}
        self.buttonPack = {'pady' : 5}
        self.actionPack = {'side' : "left", 'pady' : 10, 'padx' : 10}

    def basicEntries(self, parent):
        fNameLbl = ttk.Label(parent, text="First Name")
        self.fName = ttk.Entry(parent, width=30)

        lNameLbl = ttk.Label(parent, text="Last Name")
        self.lName = ttk.Entry(parent, width=30)

        streetLbl = ttk.Label(parent, text="Street")
        self.street = ttk.Entry(parent, width=30)

        cityLbl = ttk.Label(parent, text="City")
        self.city = ttk.Entry(parent, width=30)

        stateLbl = ttk.Label(parent, text="State")
        self.state = ttk.Entry(parent, width=30)

        zipLbl = ttk.Label(parent, text="Zip Code")
        self.zip = ttk.Entry(parent)

        titleLbl = ttk.Label(parent, text="Title")
        self.title = ttk.Entry(parent)

        
    def setBindings(self, controller):
        pass

    def goBack(self):
        # app.show_frame(self.parentPage)
        pass

    def pack_elements(self):
        self.labelConfig = {'font':("Arial", 8), 'foreground': self.app.color3}
        self.pageTitle.pack(pady=10, padx=10)

        for entry in self.entries:
            label = entry[0]
            label.config(**self.labelConfig)
            label.pack(**self.labelPack)

            if (len(entry) == 2):
                item = entry[1]
                item.pack(**self.entryPack)

        for button in self.bottomButtons:
            button.pack(**self.buttonPack)
            button.config(width=self.btnWidth)


class StartingPage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)

        self.pageTitle = ttk.Label(self, text="Welcome to the Payroll System", font=LARGE_FONT)
        #make it top center
        # self.pageTitle.pack(pady=10, padx=10)
        self.loginBtn = ttk.Button(self, text="Login", command=lambda: controller.show_frame(LoginPage))

        self.quitBtn = ttk.Button(self, text="Quit", command=quit)
        
        self.bottomButtons = [self.loginBtn, self.quitBtn]
        #toggle themes
        theme_button = ttk.Button(self, text="Toggle Theme", command=controller.toggleTheme)
        theme_button.pack(side = BOTTOM)

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
        self.backBtn = ttk.Button(self, text="Back", command=lambda: self.goBack())

        self.entries = [(label1, self.userName), (label2, self.password)]
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

        #add tabs to switch frames
        self.tabControl = ttk.Notebook(self)
        #add tabs with
        addEmpTab = ttk.Frame(self.tabControl)
        self.searchEmpTab = searchFrame(self.tabControl, controller)

        #open add employee page
        self.tabControl.add(addEmpTab, text='Add Employee')
        self.tabControl.add(self.searchEmpTab, text='View Employee')
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

        dobLbl = ttk.Label(column1, text="Date of Birth")
        self.dob = ttk.Entry(column1)

        amountLbl = ttk.Label(column2, text="Amount")
        self.amount = ttk.Entry(column2)

        ssnLbl = ttk.Label(column2, text="SSN")
        self.ssn = ttk.Entry(column2)

        startDateLbl = ttk.Label(column2, text="Start Date")
        self.startDate = ttk.Entry(column2)

        accountLbl = ttk.Label(column2, text="Account Number")
        self.account = ttk.Entry(column2)

        routingLbl = ttk.Label(column2, text="Routing Number")
        self.routing = ttk.Entry(column2)

        permsLbl = ttk.Label(column2, text="Permissions")
        self.perms = ttk.Entry(column2)

        emailLbl = ttk.Label(column1, text="Office Email")
        self.email = ttk.Entry(column1)

        phoneLbl = ttk.Label(column1, text="Office Phone")
        self.phone = ttk.Entry(column1)

        self.addEmpBtn = ttk.Button(self, text="Add Employee", width=self.btnWidth, style="Accent.TButton", command=lambda: self.addEmployee())


        #put logout button on the top right
        self.logoutBtn = ttk.Button(self, text="Logout", width=self.btnWidth, command=lambda: controller.show_frame(StartingPage))
        self.logoutBtn.pack(side="right", padx=10, pady=10)

        self.exportBtn = ttk.Button(self, text="Export CSV", width=self.btnWidth, command=lambda: self.exportCSV())

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
        

        '''
        -----------------VIEW EMPLOYEE-----------------
        '''
        tableColumns = {"First Name":"first_name", "Last Name":"last_name", "ID":"id", "Office Email":"office_email", "Office Phone":"office_phone", "Title":"title", "Department":"dept"}
        self.searchEmpTab.setTableColumns(tableColumns)
        self.searchEmpTab.initializeTable()

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
            (ssnLbl, self.ssn),
            (classificationLbl, self.classSelect),
            (amountLbl, self.amount),
            (startDateLbl, self.startDate),
            (accountLbl, self.account),
            (routingLbl, self.routing),
            (permsLbl, self.perms),
            (deptLbl, self.deptSelect)
        ]

    def changeTab(self, *args):
        tab = self.tabControl.index(self.tabControl.select())
        if tab == 0:
            self.exportBtn.pack_forget()
            self.addEmpBtn.pack(**self.actionPack)
        if tab == 1:
            self.searchEmpTab.loadSearchData()
            self.addEmpBtn.pack_forget()
            self.exportBtn.pack(**self.actionPack)

    def addEmployee(self):
        if self.validateForm:
            payroll.add_employee(self.fName.get(), self.lName.get(), self.street.get(), self.city.get(), self.state.get(), self.zip.get(), self.classification.get(), self.amount.get(), self.dob.get(), self.ssn.get(), self.startDate.get(), self.account.get(), self.routing.get(), self.perms.get(), self.title.get(), self.dept.get(), self.email.get(), self.phone.get())

            messagebox.showinfo(message='Employee Added Successfully')


    def editEmployee(self, *args):
        emp = self.app.currentUser
        setEntry(self.fName, emp.get_first_name())
        setEntry(self.lName, emp.get_last_name())
        setEntry(self.street, emp.get_street())
        setEntry(self.city, emp.get_city())
        setEntry(self.state, emp.get_state())
        setEntry(self.zip, emp.get_zip())
        setEntry(self.title, emp.get_title())
        setEntry(self.email, emp.get_office_email())
        setEntry(self.phone, emp.get_office_phone())
        setEntry(self.ssn, emp.get_ssn())

        classification = emp.get_classification()
        setEntry(self.classSelect, classification)

        if classification == 'Salary':
            amount = emp.get_salary()
        elif classification == 'Commission':
            amount = emp.get_commission()
        elif classification == 'Hourly':
            amount = emp.get_hourly()

        setEntry(self.amount, amount)

        setEntry(self.startDate, emp.get_start_date())
        setEntry(self.account, emp.get_account())
        setEntry(self.routing, emp.get_routing_num())
        setEntry(self.perms, emp.get_permissions())
        setEntry(self.dept, emp.get_dept())


    def saveEmployee(self):
        pass

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
        self.editBtn = ttk.Button(self, text="Edit", width=self.btnWidth, command=lambda: self.editPersonalInfo())
        self.saveBtn = ttk.Button(self, text="Save", width=self.btnWidth, style="Accent.TButton", command=lambda: self.savePersonalInfo())

        #put logout button on the bottom right
        self.logoutBtn = ttk.Button(self, text="Logout", width=self.btnWidth, command=lambda: controller.show_frame(StartingPage))
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

        #TODO: Put actually paystub info in here.
        payStubLbl = ttk.Label(payStubColumn, text="PayStub")
        self.payStub = ttk.Entry(payStubColumn)

        amountLbl = ttk.Label(payStubColumn, text="Amount")
        self.amount = ttk.Entry(payStubColumn)

        '''
        -----------------DIRECTORY TAB-----------------
        '''

        self.searchEmpTab.initializeTable()

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
            self.editBtn.pack(**self.actionPack)
        if tab == 1:
            self.searchEmpTab.loadSearchData()
            self.editBtn.pack_forget()
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

    def editPersonalInfo(self, *args):
        for item in self.personalInfo:
            item.config(state=NORMAL)
            self.editBtn.pack_forget()
            self.saveBtn.pack(**self.actionPack)
            
    def savePersonalInfo(self, *args):
        if (self.validateForm()):
            for item in self.personalInfo:
                item.config(state=DISABLED)
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
        # print(df_rows)
        
    def insertRows(self, rows):
        # print(rows)
        count = 0
        for row in rows:
            if count % 2 == 0:
                self.tree.insert("", "end", values=row, tags=("even_row",))
            else:
                self.tree.insert("", "end", values=row, tags=("odd_row",))
            count += 1

    def showEmpData(self, event):
        #TODO: Restructure this
        empWindow = Toplevel(self)
        empWindow.title("Employee Information")
        empWindow.geometry("300x350")
        curItem = self.tree.focus()
        rowValues = self.tree.item(curItem)['values']
        fName = rowValues[0]
        lName = rowValues[1]
        empID = rowValues[2]
        Label(empWindow, text =f"{fName} {lName}", font=MEDIUM_FONT).pack()

        selectedEmp = payroll.find_employee_by_id(empID)

        #TODO: Don't actually show this information. Just for testing.
        ttk.Label(empWindow, text="Street", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.street = ttk.Entry(empWindow)
        self.street.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(empWindow, text="City", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.city = ttk.Entry(empWindow)
        self.city.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(empWindow, text="State", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.state = ttk.Entry(empWindow)
        self.state.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(empWindow, text="Zip Code", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.zip = ttk.Entry(empWindow)
        self.zip.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(empWindow, text="Title", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.title = ttk.Entry(empWindow)
        self.title.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)

        self.personalInfo = [
            self.street,
            self.city,
            self.state,
            self.zip,
            self.title
        ]

        setEntry(self.street, selectedEmp.get_street())
        setEntry(self.city, selectedEmp.get_city())
        setEntry(self.state, selectedEmp.get_state())
        setEntry(self.zip, selectedEmp.get_zip())
        setEntry(self.title, selectedEmp.get_title())
        for item in self.personalInfo:
            item.config(state=DISABLED) # or 'readonly'?


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
    # emp = find_employee_by_id('51-4678119')
    # emp.make_salaried(134386.51)
    # emp.issue_payment()

    # # Change Reynard,Lorenzin to Commissioned; add some receipts
    # emp = find_employee_by_id('11-0469486')
    # emp.make_commissioned(50005.50, 27)
    # clas = emp.classification
    # clas.add_receipt(1109.73)
    # clas.add_receipt(746.10)
    # emp.issue_payment()

    # # Change Jed Netti to Hourly; add some hour entries
    # emp = find_employee_by_id('68-9609244')
    # emp.make_hourly(47)
    # clas = emp.classification
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # emp.issue_payment()

if __name__ == '__main__':
    main()