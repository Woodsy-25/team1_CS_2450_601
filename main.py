import tkinter as tk
from tkinter import *
from tkinter import ttk


#the payroll code
import os, os.path, shutil

EMPLOYEES = []
PAY_LOGFILE = 'paylog.txt'

def load_employees():
    """
    Reads EMPLOYEES.csv by line, creating Employee objects initialized with their string attributes.
    Creates and assigns the appropriate classification instance for the employee as an attribute.
    Adds the Employee object to a global list of EMPLOYEES.
    """

    with open('EMPLOYEES.csv', 'r', encoding="utf-8") as in_file:
        next(in_file) # skip header

        for line in in_file:
            line = line.strip().split(',')

            # set emp_id, first_name, last_name, address, city, state, zipcode
            emp = Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6], None)

            class_id = int(line[7]) # salary = 1, commisioned = 2, hourly = 3
            salary = float(line[8])
            commission_rate = float(line[9])
            hourly_rate = float(line[10])

            # set classification
            if class_id == 1:
                emp.make_salaried(salary)
            elif class_id == 2:
                emp.make_commissioned(salary, commission_rate)
            elif class_id == 3:
                emp.make_hourly(hourly_rate)

            EMPLOYEES.append(emp)

def add_employee(emp_id, first_name, last_name, address, city, state, zipcode):
    """
    Adds a new employee to the EMPLOYEES list.
    """
    emp = Employee(emp_id, first_name, last_name, address, city, state, zipcode, None)
    EMPLOYEES.append(emp)

def user_add_employee():
    """
    Prompts the user for employee information and adds the employee to the EMPLOYEES list.
    """
    emp_id = input('Enter employee ID: ')
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    address = input('Enter address: ')
    city = input('Enter city: ')
    state = input('Enter state: ')
    zipcode = input('Enter zipcode: ')
    add_employee(emp_id, first_name, last_name, address, city, state, zipcode)

user_add_employee

def find_employee_by_id(emp_id):
    """Returns the Employee object of a given ID."""
    for emp in EMPLOYEES:
        if emp.emp_id == emp_id:
            return emp

def process_timecards():
    """
    Reads timecards.csv and adds each hourly record to a list
    in each 'Hourly' employee's classification object.
    """

    with open('timecards.csv', 'r', encoding="utf-8") as in_file:
        for line in in_file:
            line = line.strip().split(',')
            emp_id = line[0]
            emp = find_employee_by_id(emp_id)

            if len(line) > 1: # if the employee has timecard data
                timecards = line[1:]

                for timecard in timecards:
                    emp.classification.add_timecard(float(timecard))

def process_receipts():
    """
    Reads receipts.csv and adds each receipt to a list
    in each 'Commissioned' employee's classification object.
    """

    with open('receipts.csv', 'r', encoding="utf-8") as in_file:
        for line in in_file:
            line = line.strip().split(',')
            emp_id = line[0]
            emp = find_employee_by_id(emp_id)

            if len(line) > 1: # if the employee has receipt data
                receipts = line[1:]

                for receipt in receipts:
                    emp.classification.add_receipt(float(receipt))

def run_payroll():
    if os.path.exists(PAY_LOGFILE): # pay_log_file is a global variable holding ‘paylog.txt’
        os.remove(PAY_LOGFILE)
    for emp in EMPLOYEES:               # EMPLOYEES is the global list of Employee objects
        emp.issue_payment()             # issue_payment calls a method in the classification
                                        # object to compute the pay

class Employee:
    def __init__(self, emp_id, first_name, last_name, address, city, state, zipcode, classification):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.classification = classification

    def make_salaried(self, salary):
        """Changes employee classification to 'salaried' with the given salary."""
        self.classification = Salaried(salary)

    def make_commissioned(self, salary, commision_rate):
        """Changes employee classification to 'commissioned'
        with the given salary and commission rate."""
        self.classification = Commisioned(salary, commision_rate)

    def make_hourly(self, hourly_rate):
        """Changes employee classification to 'hourly' with the given hourly rate."""
        self.classification = Hourly(hourly_rate)

    def issue_payment(self):
        """Appends employee payment information to paylog.txt"""
        pay = self.classification.compute_pay()
        message = f'Mailing {pay:0.2f} to {self.first_name} {self.last_name} at '\
        f'{self.address} {self.city} {self.state} {self.zipcode}\n'

        with open('paylog.txt', 'a', encoding="utf-8") as out_file:
            out_file.write(message)

class Classification:
    def compute_pay(self):
        """Abstract method for computing pay."""

class Salaried(Classification):
    def __init__(self, salary):
        self.salary = salary

    def compute_pay(self): # override method
        """Returns the employee's salaried pay."""
        pay = self.salary / 24 # 24 pay periods per year

        return round(pay, 2)

class Commisioned(Salaried):
    def __init__(self, salary, commission_rate):
        super().__init__(salary)
        self.commission_rate = commission_rate / 100
        self._receipts = []

    def compute_pay(self): # override method
        """Returns the employee's salaried pay plus commission."""
        pay = self.salary / 24 # 24 pay periods per year
        comm = self.commission_rate * sum(self._receipts)
        self._receipts.clear()

        return round(pay + comm, 2)

    def add_receipt(self, receipt):
        """Adds a receipt to a private list."""
        self._receipts.append(receipt)

class Hourly(Classification):
    def __init__(self, hourly_rate):
        self.hourly_rate = hourly_rate
        self._timecards = []

    def compute_pay(self): # override method
        """Returns the employee's hourly pay."""
        pay = self.hourly_rate * sum(self._timecards)
        self._timecards.clear()

        return round(pay, 2)

    def add_timecard(self, timecard):
        """Adds a timecard to a private list."""
        self._timecards.append(timecard)

largefont = ('Verdana', 20) # specify font and size

class PayrollApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for f in (StartingPage, LoginPage, AdminPage):
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
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Login", command=lambda: controller.show_frame(LoginPage))
        button1.pack()

        button2 = ttk.Button(self, text="Quit", command=quit)
        button2.pack()

def login(entry1, entry2):
        if entry1 == "admin" and entry2 == "admin":
            return True
        else:
            return False
            messagebox.showerror("Error", "Invalid username or password")

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

        entry2 = tk.Entry(self)
        entry2.pack()

        #only allow admin to login
        button1 = ttk.Button(self, text="Login", command=lambda: controller.show_frame(AdminPage))
        button1.pack()

        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartingPage))
        button2.pack()

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Admin Page", font=largefont)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Run Payroll", command=run_payroll)
        button1.pack()

        button2 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(LoginPage))
        button2.pack()




#making a list from logins.csv
with open('logins.csv', 'r') as f:
    #skip the first line
    next(f)
    #make a list of lists
    logins = [line.strip().split(',') for line in f]

#open app
app = PayrollApp()
app.mainloop()