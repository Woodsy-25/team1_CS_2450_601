'''
This is the main program that curretly holds both the code from the employee project and also hold the code for the GUI.
'''

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, messagebox, filedialog
from payroll import *
from operator import itemgetter
import payroll
import tkinter as tk
from tktooltip import ToolTip
import sv_ttk
import re
import subprocess
import bcrypt

EMAIL_REGEX = "^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$"
PHONE_REGEX = "^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$"
ZIP_REGEX = "^[0-9]{5}(?:-[0-9]{4})?$"
DATE_REGEX = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"
NUMBER_REGEX = "^(?:-(?:[1-9](?:\\d{0,2}(?:,\\d{3})+|\\d*))|(?:0|(?:[1-9](?:\\d{0,2}(?:,\\d{3})+|\\d*))))(?:.\\d+|)$"

subprocess.Popen('pip install -r requirements.txt', shell=True)

#the payroll code
LARGE_FONT = ('Verdana', 20) # specify font and size
MEDIUM_FONT = ('Verdana', 15)
HINT_FONT = ("Ariel", "8", "italic")

USER_TYPE_EMPLOYEE = '1'
USER_TYPE_ADMIN = '2'
BTN_WIDTH = 12

class PayrollApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #size of the window
        tk.Tk.geometry(self, "850x700")
        self.minsize(800, 650)
        self.title('Employee Payroll')
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.employeeID = 0
        self.currentUser = None
        self.perms = USER_TYPE_EMPLOYEE
        self.previousPage = StartingPage
        self.currentPage = StartingPage
        self.frames = {}

        # Theming 
        self.color1 = "#fafafa"
        self.color2 = "#e7e7e7"
        self.color3 = "#5f5f5f"
        self.color4 = "#000000"

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
            self.color4 = "#ffffff"
        else:
            self.color1 = "#fafafa"
            self.color2 = "#e7e7e7"
            self.color3 = "#5f5f5f"
            self.color4 = "#000000"



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
            label.pack(**self.labelPack)
            if entry != None:
                entry.pack(**self.entryPack)
                label.config(**self.labelConfig)


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
        theme_button.pack(side = BOTTOM, pady=10)

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
        name = self.userName.get()
        pw = self.password.get()
        with open('encrypted.csv', 'r') as incsv:
            pass_list = []
            read_csv = csv.reader(incsv)
            for read in read_csv:
                pass_list.append(read)

            pw_b = pw.encode('utf-8')
            for user in pass_list:
                if user[0] == name:
                    pch = user[1].encode()
                    if bcrypt.checkpw(pw_b, pch): 
                        employeeID = user[2]
                        self.app.currentUser = payroll.find_employee_by_id(employeeID)
                        if user[3] == USER_TYPE_EMPLOYEE:
                            self.app.perms = USER_TYPE_EMPLOYEE
                            self.app.init_frame(EmployeePage)
                            self.app.show_frame(EmployeePage)
                        elif user[3] == USER_TYPE_ADMIN:
                            self.app.perms = USER_TYPE_ADMIN
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
        self.hint = ttk.Label(self, text="Hint: * Required Fields" , font=HINT_FONT)
        self.hint.pack(side="right", pady=(10,0), padx=(0,20))

        ToolTip(self.helpBtn, delay=1, msg='Help')

        '''
        -----------------MANAGE EMPLOYEE-----------------
        '''
        self.addColumns(self.manageEmpTab)
        self.addEntries()
        self.saveBtn = ttk.Button(self, text="Save", width=BTN_WIDTH, style="Accent.TButton", command=lambda: self.saveEmployee())
        self.cancelBtn = ttk.Button(self, text="Cancel", width=BTN_WIDTH, command=lambda: self.cancelEdit())

        ToolTip(self.saveBtn, delay=1, msg='Add Employee')

        '''
        -----------------SEARCH EMPLOYEES-----------------
        '''
        self.searchEmpTab.initializeTable()
        self.exportBtn = ttk.Button(self, text="Export CSV", width=BTN_WIDTH, command=lambda: self.exportCSV())


    def addColumns(self, parent):
        self.column1 = ttk.Frame(parent)
        self.column1.pack(pady=10, side="left", expand=1, fill="both")
        self.column2 = ttk.Frame(parent)
        self.column2.pack(pady=10, side="left", expand=1, fill="both")

    def addEntries(self):
        self.fNameLbl = ttk.Label(self.column1, text="First Name*")
        self.fName = ttk.Entry(self.column1)

        self.lNameLbl = ttk.Label(self.column1, text="Last Name*")
        self.lName = ttk.Entry(self.column1)

        self.streetLbl = ttk.Label(self.column1, text="Street*")
        self.street = ttk.Entry(self.column1)

        self.cityLbl = ttk.Label(self.column1, text="City*")
        self.city = ttk.Entry(self.column1)

        self.stateLbl = ttk.Label(self.column1, text="State*")
        self.state = ttk.Entry(self.column1)

        self.zipLbl = ttk.Label(self.column1, text="Zip Code*")
        self.zip = ttk.Entry(self.column1)

        self.dobLbl = ttk.Label(self.column1, text="Date of Birth*")
        self.dob = ttk.Entry(self.column1)

        self.emailLbl = ttk.Label(self.column1, text="Office Email*")
        self.email = ttk.Entry(self.column1)

        self.phoneLbl = ttk.Label(self.column1, text="Office Phone*")
        self.phone = ttk.Entry(self.column1)

        self.titleLbl = ttk.Label(self.column2, text="Title")
        self.title = ttk.Entry(self.column2)

        self.startDateLbl = ttk.Label(self.column2, text="Start Date*")
        self.startDate = ttk.Entry(self.column2)

        # Department Dropdown
        self.deptLbl = ttk.Label(self.column2, text="Department*")
        self.dept = StringVar()
        self.deptSelect = ttk.Combobox(self.column2, textvariable=self.dept)
        self.deptSelect['values'] = ['Engineering', 'Finance', 'HR', 'IT',  'Legal', 'Marketing', 'Operations',  'Sales']
        self.deptSelect.state(['readonly'])

        # Permissions Dropdown
        self.permsLbl = ttk.Label(self.column2, text="Permissions*")
        self.perms = StringVar()
        self.permSelect = ttk.Combobox(self.column2, textvariable=self.perms)
        self.permSelect['values'] = ['Admin', 'Employee']
        self.permSelect.state(['readonly'])

        # Classification Dropdown
        self.classificationLbl = ttk.Label(self.column2, text="Classification")
        self.classification = StringVar()
        self.classSelect = ttk.Combobox(self.column2, textvariable=self.classification)
        self.classSelect['values'] = ['Salary', 'Commission', 'Hourly']
        self.classSelect.state(['readonly'])
        self.classSelect.bind("<<ComboboxSelected>>", self.classSelected)

        self.amountLbl = ttk.Label(self.column2, text="Amount")
        self.amount = ttk.Entry(self.column2)

        # Commission Rate
        self.rateLbl = ttk.Label(self.column2, text="Commission Rate")
        self.rate = ttk.Entry(self.column2)

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
            self.startDateLbl: self.startDate,
            self.permsLbl: self.permSelect,
            self.deptLbl: self.deptSelect,
            self.classificationLbl: self.classSelect,
            self.amountLbl: self.amount
        }



    def changeTab(self, *args):
        tab = self.tabControl.index(self.tabControl.select())
        if tab == 0:
            self.hint.config(text="Hint: * Required Fields")
            self.exportBtn.pack_forget()
            self.cancelBtn.pack(**self.actionPack)
            self.saveBtn.pack(**self.actionPack)
        if tab == 1:
            self.hint.config(text="Hint: Inactive employees are marked in red")
            self.searchEmpTab.loadSearchData()
            self.cancelBtn.pack_forget()
            self.saveBtn.pack_forget()
            self.exportBtn.pack(**self.actionPack)

    def addEmployee(self):
        classification = self.classification.get()
        amount = self.amount.get()
        salary = commission = hourly = 0
        if classification == 'Salary':
            salary = amount
        elif classification == 'Commission':
            salary = amount
            commission = self.rate.get()
        elif classification == 'Hourly':
            hourly = amount
        if self.validateForm():
            payroll.add_employee(None, self.fName.get(), self.lName.get(), self.street.get(), self.city.get(), self.state.get(), self.zip.get(), self.classification.get(), salary, commission, hourly, self.dob.get(), None, self.startDate.get(), None, None, self.perms.get(), self.title.get(), self.dept.get(), self.email.get(), self.phone.get())
            messagebox.showinfo(message='Employee Added Successfully')

    def editEmployee(self, emp):
        self.action = 'EDIT'
        self.tabControl.tab(self.manageEmpTab, text='Edit Employee')
        self.editingEmp = emp

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

        # Set classification dropdown
        classification = emp.get_classification()
        amount = ""
        if isinstance(classification, payroll.Commissioned):
            classification = 1
            amount = emp.get_salary()
            rate = emp.get_commission()
            setEntry(self.rate, rate)
            self.amountLbl.config(text="Salary")
            self.rateLbl.config(**self.labelConfig)
            self.rateLbl.pack(**self.labelPack)
            self.rate.pack(**self.entryPack)
        elif isinstance(classification, payroll.Salaried):
            classification = 0
            amount = emp.get_salary()
        elif isinstance(classification, payroll.Hourly):
            classification = 2
            amount = emp.get_hourly()
        self.classSelect.current(classification)
        self.classSelected()
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

        self.tabControl.select(self.manageEmpTab) 


    def updateEmployee(self):
        if self.validateForm():
            emp = self.editingEmp

            classification = self.classification.get()
            amount = self.amount.get()
            if classification == 'Salary':
                emp.make_salaried(amount)
            elif classification == 'Commission':
                rate = self.rate.get()
                emp.make_commissioned(amount, rate)
            elif classification == 'Hourly':
                emp.make_hourly(amount)

            emp.set_first_name(self.fName.get())
            emp.set_last_name(self.lName.get())
            emp.set_street(self.street.get())
            emp.set_city(self.city.get())
            emp.set_state(self.state.get())
            emp.set_zip(self.zip.get())
            emp.set_dob(self.dob.get())
            emp.set_office_email(self.email.get())
            emp.set_office_phone(self.phone.get())
            emp.set_title(self.title.get())

            emp.set_start_date(self.startDate.get())
            emp.set_permissions(self.perms.get())
            emp.set_dept(self.dept.get())

            messagebox.showinfo(message='Employee Updated Successfully')
            self.action = 'NEW'
            self.tabControl.tab(self.manageEmpTab, text='Add Employee')
            ToolTip(self.saveBtn, delay=1, msg='Add Employee')

            self.tabControl.select(self.searchEmpTab)
            for entry in self.entries.values():
                entry.delete(0,END)

    def saveEmployee(self, event=None):
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
                self.action = 'NEW'
                self.tabControl.tab(self.manageEmpTab, text='Add Employee')
                self.tabControl.select(self.searchEmpTab)


    def validateForm(self):
        # Make sure all required entries are filled and valid
        valid = True
        self.requiredFields = [self.fName, self.lName, self.street, self.city, self.state, self.zip, self.dob, self.startDate, self.perms, self.dept, self.email, self.phone]
        for field in self.requiredFields:
            if (len(field.get()) < 1):
                messagebox.showerror("Invalid", "Please enter all required fields")
                return False

        # Validate Zip Code
        if not re.fullmatch(ZIP_REGEX, self.zip.get()):
            self.zip.config(foreground='red')
            messagebox.showerror("Invalid Zip Code", "Make sure it is formatted correctly.\n\n(Ex. 84602)")
            valid = False
        else:
            self.zip.config(foreground=self.app.color4)
        # Validate DOB
        if not re.fullmatch(DATE_REGEX, self.dob.get()):
            self.dob.config(foreground='red')
            messagebox.showerror("Invalid Date of Birth", "Make sure it is formatted correctly.\n\n(Ex. 1/24/2000)")
            valid = False
        else:
            self.dob.config(foreground=self.app.color4)
        # Validate Email
        if not re.fullmatch(EMAIL_REGEX, self.email.get()):
            self.email.config(foreground='red')
            messagebox.showerror("Invalid Email Address", "Make sure it is formatted correctly.\n\n(Ex. john.smith@example.com)")
            valid = False
        else:
            self.email.config(foreground=self.app.color4)
        # Validate Phone Number
        if not re.fullmatch(PHONE_REGEX, self.phone.get()):
            self.phone.config(foreground='red')
            messagebox.showerror("Invalid Phone Number", "Make sure it is formatted correctly.\n\n(Ex. 888-777-6666 or 8887776666)")
            valid = False
        else:
            self.phone.config(foreground=self.app.color4)
        # Validate Start Date
        if not re.fullmatch(DATE_REGEX, self.startDate.get()):
            self.startDate.config(foreground='red')
            messagebox.showerror("Invalid Start Date", "Make sure it is formatted correctly.\n\n(Ex. 1/24/2000)")
            valid = False
        else:
            self.startDate.config(foreground=self.app.color4) 
        # Validate Amount
        if not re.fullmatch(NUMBER_REGEX, self.amount.get()):
            self.amount.config(foreground='red')
            messagebox.showerror("Invalid Amount", "Make sure it is formatted correctly.\n\n(Ex. 250.00)")
            valid = False
        else:
            self.amount.config(foreground=self.app.color4)

        return valid

    def classSelected(self, event=None):
        if self.classification.get() == 'Commission':
            self.amountLbl.config(text="Salary")
            self.rateLbl.config(**self.labelConfig)
            self.rateLbl.pack(**self.labelPack)
            self.rate.pack(**self.entryPack)
        else:
            self.rateLbl.pack_forget()
            self.rate.pack_forget()
            self.amountLbl.config(text="Amount")

    def exportCSV(self):
        payroll.export_payroll()
        print('EXPORTING as payroll.csv')
        inactive = messagebox.askyesno('Exporting Active Employees', 'Would you like to export inactive employees as well?')
        initialName = 'export_all' if inactive else 'export_active_only'
        filename = filedialog.asksaveasfilename(initialfile=initialName, filetypes=[("CSV File", ".csv")], defaultextension=".csv")
        if (filename):
            payroll.write_csv(filename, inactive)


    def setBindings(self, controller):
        self.fName.focus()
        controller.bind("<Return>", self.saveEmployee)

'''
-----------------EMPLOYEE PAGE-----------------
'''

class EmployeePage(Page):
    def __init__(self, parent, controller):
        Page.__init__(self, parent, controller)
        self.pageTitle = ttk.Label(self, text="Employee Page", font=LARGE_FONT)
        self.pageTitle.pack(pady=10, padx=10)
        self.emp = self.app.currentUser

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

        ToolTip(self.editBtn, delay=1, msg='Edit Personal Information')
        ToolTip(self.saveBtn, delay=1, msg='Save Personal Information')

        self.cancelBtn = ttk.Button(self, text="Cancel", width=BTN_WIDTH, command=lambda: self.loadPersonalInfo())

        #put logout button on the bottom right
        self.logoutBtn = ttk.Button(self, text="Logout", width=BTN_WIDTH, command=lambda: self.logout())
        self.logoutBtn.pack(side="right", padx=10, pady=10)

        self.helpBtn = ttk.Button(self, text="?", width=2, command=lambda: controller.show_frame(HelpPage))
        self.helpBtn.pack(side="right", pady=10)
        ToolTip(self.helpBtn, delay=1, msg='Help')

        '''
        -----------------PROFILE TAB-----------------
        '''

        # inner padding not working so use blank label
        blankInfo = ttk.Label(infoColumn, text="")
        
        # Personal Info fields
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

        # Pay stub fields
        self.payClassLbl = ttk.Label(payStubColumn, text="Payment Classification")
        self.payClass = ttk.Entry(payStubColumn)

        self.amount1Lbl = ttk.Label(payStubColumn)
        self.amount1 = ttk.Entry(payStubColumn)

        self.amount2Lbl = ttk.Label(payStubColumn)
        self.amount2 = ttk.Entry(payStubColumn)

        self.payLbl = ttk.Label(payStubColumn, text="Payment Amount")
        self.pay = ttk.Entry(payStubColumn)

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
            self.payClassLbl: self.payClass,
            self.amount1Lbl: self.amount1
        }

        self.paymentInfo = [
            self.payClass,
            self.amount1,
            self.amount2,
            self.pay
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
            self.loadPaymentInfo()
            self.loadPersonalInfo()
        if tab == 1:
            self.searchEmpTab.loadSearchData()
            self.editBtn.pack_forget()
            self.cancelBtn.pack_forget()
            self.saveBtn.pack_forget()

    def loadPaymentInfo(self, *args):
        paymentClass = self.emp.get_class()
        setEntry(self.payClass, paymentClass)
        if paymentClass == 'Salary':
            self.amount1Lbl.config(text="Yearly Salary")
            setEntry(self.amount1, "$" + self.emp.get_salary())
        elif paymentClass == 'Commission':
            self.amount1Lbl.config(text="Salary")
            setEntry(self.amount1, "$" + self.emp.get_salary()) 
            self.amount2Lbl.config(text="Commission Rate")
            commission = self.emp.get_commission()
            setEntry(self.amount2, commission + "%")
            self.amount2Lbl.config(**self.labelConfig)
            self.amount2Lbl.pack(**self.labelPack)
            self.amount2.pack(**self.entryPack)
        elif paymentClass == 'Hourly':
            self.amount1Lbl.config(text="Hourly Rate")
            setEntry(self.amount1, "$" + self.emp.get_hourly() + " /hour")

        payment = self.emp.get_payment()
        setEntry(self.pay, "$" + str(payment))
        for item in self.paymentInfo:
            item.config(state=DISABLED)
        self.amount1Lbl.config(**self.labelConfig)
        self.payLbl.config(**self.labelConfig)
        self.payLbl.pack(**self.labelPack)
        self.pay.pack(**self.entryPack)

    def loadPersonalInfo(self, *args):
        setEntry(self.fName, self.emp.get_first_name())
        setEntry(self.lName, self.emp.get_last_name())
        setEntry(self.street, self.emp.get_street())
        setEntry(self.city, self.emp.get_city())
        setEntry(self.state, self.emp.get_state())
        setEntry(self.zip, self.emp.get_zip())
        setEntry(self.title, self.emp.get_title())

        
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
        if self.validateForm():
            for item in self.personalInfo:
                item.config(state=DISABLED)
                self.cancelBtn.pack_forget()
                self.saveBtn.pack_forget()
                self.editBtn.pack(**self.actionPack)
            
            self.emp.set_first_name(self.fName.get())
            self.emp.set_last_name(self.lName.get())
            self.emp.set_street(self.street.get())
            self.emp.set_city(self.city.get())
            self.emp.set_state(self.state.get())
            self.emp.set_zip(self.zip.get())
            self.emp.set_title(self.title.get())


    def validateForm(self):
        self.requiredFields = [self.fName, self.lName, self.street, self.city, self.state, self.zip]
        for field in self.requiredFields:
            if (len(field.get()) < 1):
                messagebox.showerror("Invalid", "Please enter all required fields")
                return False
        # Validate Zip Code
        if not re.fullmatch(ZIP_REGEX, self.zip.get()):
            self.zip.config(foreground='red')
            messagebox.showerror("Invalid Zip Code", "Make sure it is formatted correctly.\n\n(Ex. 84602)")
            return False
        else:
            self.zip.config(foreground=self.app.color4)
        return True

    def setBindings(self, controller):
        controller.unbind("<Return>")
        pass


class searchFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.app = controller
        self.showInactive = False

        style_tree = ttk.Style()
        style_tree.configure("t_style.Treeview", rowheight=25)
    
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

        # Active Only Toggle
        if self.app.perms == USER_TYPE_ADMIN:
            self.showInactive = True
            self.activeOnly = StringVar()
            toggle = ttk.Checkbutton(search_frame, text="Active Only", command=self.toggleActive, variable=self.activeOnly, onvalue='active', offvalue='inactive')
            toggle.pack(pady=(0,5), padx=(0,10), side='left', fill=X)
            ToolTip(toggle,delay=1, msg='Show/Hide\nInactive Employees')


        table_frame = tk.Frame(self)
        table_frame.pack(expand=1, fill=BOTH)

        self.tree = ttk.Treeview(table_frame, style="t_style.Treeview")
        self.tree.bind("<Double-1>", self.showEmpData)
        self.tree.place(relheight=1, relwidth=.96, x=10)

        scrollY = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side="right", fill="y")


    def initializeTable(self):
        if self.app.perms == USER_TYPE_ADMIN:
            self.columnHeaders = ["First Name", "Last Name", "ID", "Active", "Title", "Department", "Office Email", "Office Phone"]
            filterNames = ["First Name", "Last Name", "ID", "Office Email", "Office Phone", "Title", "Department"]
        else:
            self.columnHeaders = ["First Name", "Last Name", "ID", "Active", "Title", "Department"]
            filterNames = ["First Name", "Last Name", "Title", "Department"]
        self.clicked.set(str(self.columnHeaders[0]))
        self.filterDrop['values'] = filterNames

        self.tree["column"] = self.columnHeaders
        self.tree["show"] = "headings"

        # Set column headers
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            if not column in filterNames:
                # Hide ID column
                self.tree.column(column, minwidth=0, width=0, stretch=NO)
            elif column == "Office Email" or column == 'Title':
                self.tree.column(column, minwidth=50, width=150, stretch=YES)
            else:
                self.tree.column(column, minwidth=50, width=90, stretch=YES)

    def loadSearchData(self, event=None):
        # Clear Data
        empList = sorted(payroll.get_employee_list(self.showInactive), key=itemgetter(0))
        self.tree.delete(*self.tree.get_children())

        searchLen = len(self.searchBar.get())

        self.tree.tag_configure('odd_row', background=self.app.color1)
        self.tree.tag_configure('even_row', background=self.app.color2)
        self.tree.tag_configure('inactive', foreground='red')
        if searchLen == 0:
            self.insertRows(empList)
        else:
            s_key = self.columnHeaders.index(str(self.clicked.get()))
            s_list = []
            for row in empList:
                val = row[s_key]
                if self.searchBar.get().lower() == val[0:searchLen].lower():
                    s_list.append(row)
            s_list = sorted(s_list, key=itemgetter(s_key))
            self.insertRows(s_list)
        
    def insertRows(self, rows):
        count = 0
        for row in rows:
            if row[3]:
                status = "active"
            else:
                status = "inactive"
            if count % 2 == 0:
                self.tree.insert("", "end", values=row, tags=("even_row", status))
            else:
                self.tree.insert("", "end", values=row, tags=("odd_row", status))
            count += 1

    def showEmpData(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            return
        self.empWindow = Toplevel(self)
        self.empWindow.title("Employee Info")
        curItem = self.tree.focus()
        rowValues = self.tree.item(curItem)['values']
        fName = rowValues[0]
        lName = rowValues[1]
        empID = rowValues[2]
        self.empName = Label(self.empWindow, text=f"{fName} {lName}", font=MEDIUM_FONT)
        self.empName.pack()
        selectedEmp = payroll.find_employee_by_id(empID)

        if self.app.perms == USER_TYPE_ADMIN:
            ttk.Label(self.empWindow, text="Employee ID", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
            self.id = ttk.Entry(self.empWindow, width=35)
            self.id.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
            setEntry(self.id, empID)
            self.id.config(state=DISABLED)

        ttk.Label(self.empWindow, text="Title", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.title = ttk.Entry(self.empWindow, width=35)
        self.title.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(self.empWindow, text="Department", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.dept = ttk.Entry(self.empWindow, width=35)
        self.dept.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(self.empWindow, text="Office Email", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.email = ttk.Entry(self.empWindow, width=35)
        self.email.pack(pady=(0,5), padx=(10,5), expand=1, fill=X)
        ttk.Label(self.empWindow, text="Office Phone", font=("Arial", 8), foreground=self.app.color3).pack(anchor=W, padx=10, pady=(5,0))
        self.phone = ttk.Entry(self.empWindow, width=35)
        self.phone.pack(pady=(0,10), padx=(10,5), expand=1, fill=X)

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

        if self.app.perms == USER_TYPE_ADMIN:
            editBtn = ttk.Button(self.empWindow, text="Edit", width=BTN_WIDTH, style="Accent.TButton", command=lambda: self.editEmployee(selectedEmp))
            editBtn.pack(pady=(0,10), padx=10, side=LEFT)
            status = selectedEmp.get_status()
            if status == 0:
                self.empName.config(foreground='red')
                self.statusBtn = ttk.Button(self.empWindow, text="Activate", width=BTN_WIDTH, command=lambda: self.toggleStatus(selectedEmp))
            elif status == 1:
                self.empName.config(foreground=self.app.color4)
                self.statusBtn = ttk.Button(self.empWindow, text="Deactivate", width=BTN_WIDTH, command=lambda: self.toggleStatus(selectedEmp))

            self.statusBtn.pack(pady=(0,10), padx=10, side=RIGHT)
    
    def editEmployee(self, emp):
        self.master.master.editEmployee(emp)
        self.empWindow.destroy()

    def toggleStatus(self, emp):
        status = not emp.get_status()
        emp.set_status(status)
        if status:
            self.empName.config(foreground=self.app.color4)
            self.statusBtn.config(text="Deactivate")
        else:
            self.empName.config(foreground='red')
            self.statusBtn.config(text="Activate")
        self.loadSearchData()
    
    def toggleActive(self):
        if self.activeOnly.get() == 'active':
            self.showInactive = False
        else:
            self.showInactive = True
        self.loadSearchData()



def setEntry(entry, text):
    entry.delete(0,END)
    entry.insert(0,text)

def main():
    # Load employee payroll data from CSV
    payroll.load_employees()
    payroll.process_timecards()
    payroll.process_receipts()

    #open app
    app = PayrollApp()
    sv_ttk.set_theme('light')
    app.mainloop()
    #after app is closed, update the csv files with the EMPLOYEE list
    with open('employees.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        #todo: make this a function - emp has no get_data() method
        #skip the first line
        writer.writerow(['id','first_name','last_name','address','city','state','zip','classification','salary','commission','hourly','dob','ssn','start_date','account','routing_num','permissions','title','dept','office_email','office_phone','active'])
        for emp in payroll.EMPLOYEES:
            #write each employee to the csv file
            #change their classification back to an int
            #if the classification is set to salary, commission, or hourly, then set it to 0, 1, or 2 respectively
            emp_data = []
            for item in emp.get_data():
                if item == 'Salary':
                    emp_data.append(1)
                elif item == 'Commission':
                    emp_data.append(2)
                elif item == 'Hourly':
                    emp_data.append(3)
                else:
                    emp_data.append(item)
            writer.writerow(emp_data)

if __name__ == '__main__':
    main()