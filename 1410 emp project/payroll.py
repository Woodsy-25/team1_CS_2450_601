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
    def __init__(self, emp_id, first_name, last_name, street, city, state, zip, classification, pay_method, salary, commission, hourly, routing_num, account_num, office_phone, personal_phone, office_email, personal_email, dob, ssn, admin, title, dept, start, end, status, password):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.classification = classification
        self.pay_method = pay_method
        self.salary = salary
        self.commission = commission
        self.hourly = hourly
        self.routing_num = routing_num
        self.account_num = account_num
        self.office_phone = office_phone
        self.personal_phone = personal_phone
        self.office_email = office_email
        self.personal_email = personal_email
        self.dob = dob
        self.ssn = ssn
        self.admin = admin
        self.title = title
        self.dept = dept
        self.start = start
        self.end = end
        self.status = status
        self.password = password

    def get_id(self):
        return self.emp_id
    def get_first_name(self):
        return self.first_name
    def get_last_name(self):
        return self.last_name
    def get_street(self):
        return self.street
    def get_city(self):
        return self.city
    def get_state(self):
        return self.state
    def get_zip(self):
        return self.zip
    def get_class(self):
        return string(self.classification)
    def get_classification(self):
        return self.classification
    def get_salary(self):
        return self.salary
    def get_commission(self):
        return self.commission
    def get_hourly(self):
        return self.hourly
    def get_office_phone(self):
        return self.office_phone
    def get_personal_phone(self):
        return self.personal_phone
    def get_office_email(self):
        return self.office_email
    def get_personal_email(self):
        return self.personal_email
    def get_dob(self):
        return self.dob
    def get_ssn(self):
        return self.ssn
    def is_admin(self):
        return self.admin
    def get_title(self):
        return self.title
    def get_dept(self):
        return self.dept
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
    def get_status(self):
        return self.status
    def get_password(self):
        return self.password


    def set_id(self, emp_id):
        self.emp_id = emp_id
    def set_first_name(self, first_name):
        self.first_name = first_name
    def set_last_name(self, last_name):
        self.last_name = last_name
    def set_street(self, street):
        self.street = street
    def set_city(self, city):
        self.city = city
    def set_state(self, state):
        self.state = state
    def set_zip(self, zip):
        self.zip = zip


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

def main():
    load_employees()
    process_timecards()
    process_receipts()
    run_payroll()

    # Save copy of payroll file; delete old file
    shutil.copyfile(PAY_LOGFILE, 'paylog_old.txt')
    if os.path.exists(PAY_LOGFILE):
        os.remove(PAY_LOGFILE)

    # Change Issie Scholard to Salaried by changing the Employee object:
    emp = find_employee_by_id('51-4678119')
    emp.make_salaried(134386.51)
    emp.issue_payment()

    # Change Reynard,Lorenzin to Commissioned; add some receipts
    emp = find_employee_by_id('11-0469486')
    emp.make_commissioned(50005.50, 27)
    clas = emp.classification
    clas.add_receipt(1109.73)
    clas.add_receipt(746.10)
    emp.issue_payment()

    # Change Jed Netti to Hourly; add some hour entries
    emp = find_employee_by_id('68-9609244')
    emp.make_hourly(47)
    clas = emp.classification
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    clas.add_timecard(8.0)
    emp.issue_payment()

if __name__ == '__main__':
    main()
