import os, os.path, csv, shutil, uuid

EMPLOYEES = []
PAY_LOGFILE = 'paylog.txt'
EMPLOYEES_FILE = 'employees.csv'

#TODO add more info to receipt and timecard files

def load_employees():
    """
    Reads EMPLOYEES.csv by line, creating Employee objects initialized with their string attributes.
    Creates and assigns the appropriate classification instance for the employee as an attribute.
    Adds the Employee object to a global list of EMPLOYEES.
    """

    with open(EMPLOYEES_FILE, 'r', encoding="utf-8") as in_file:
        next(in_file) # skip header

        for line in in_file:
            line = line.strip().split(',')
            if len(line) == 22:
                # set emp_id, first_name, last_name, street, city, state, zipcode, classification, salary, commission, hourly, dob, ssn, start_date, account, routing_num, permission, title, dept, office_email, office_phone, active)
                emp = Employee(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19], line[20], line[21])

                class_id = int(line[7]) # salary = 1, Commissioned = 2, hourly = 3
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

def get_employee_list(inactive = False):
    empList = []
    for emp in EMPLOYEES:
        if inactive:
            empList.append([emp.first_name, emp.last_name, emp.emp_id, emp.active, emp.title, emp.dept, emp.office_email, emp.office_phone])
        # If not admin, only show active employees
        elif emp.active == 1:
            empList.append([emp.first_name, emp.last_name, emp.emp_id, emp.active, emp.title, emp.dept, emp.office_email, emp.office_phone])

    return empList

def get_employee_rows(inactive = False):
    empRow = []
    for emp in EMPLOYEES:
        emp_data = [
            emp.emp_id,
            emp.first_name,
            emp.last_name,
            emp.street,
            emp.city,
            emp.state,
            emp.zip,
            emp.classification,
            emp.salary,
            emp.commission,
            emp.hourly,
            emp.dob,
            "", # Don't export SSN
            emp.start_date,
            emp.account,
            emp.routing_num,
            emp.permissions,
            emp.title,
            emp.dept,
            emp.office_email,
            emp.office_phone,
            emp.active
        ]
        if inactive:
            empRow.append(emp_data)
        elif emp.active == 1:
            empRow.append(emp_data)

    return empRow
        
def add_employee(emp_id, first_name, last_name, street, city, state, zipcode, classification, salary, commission, hourly, dob, ssn, start_date, account, routing_num, permission, title, dept, office_email, office_phone):
    """
    Adds a new employee to the EMPLOYEES list.
    """
    if emp_id == None:
        emp_id = uuid.uuid4().hex
    emp = Employee(emp_id, first_name, last_name, street, city, state, zipcode, classification, salary, commission, hourly, dob, ssn, start_date, account, routing_num, permission, title, dept, office_email, office_phone, 1)
    EMPLOYEES.append(emp)

def edit_employee(emp_id, first_name, last_name, street, city, state, zipcode, classification, salary, commission, hourly, dob, ssn, start_date, account, routing_num, permission, title, dept, office_email, office_phone):
    """
    Edits an existing employee in the EMPLOYEES list.
    """
    emp = Employee(emp_id, first_name, last_name, street, city, state, zipcode, classification, salary, commission, hourly, dob, ssn, start_date, account, routing_num, permission, title, dept, office_email, office_phone)
    EMPLOYEES.append(emp)

def write_csv(file_name, inactive):
    fields = ["id","first_name","last_name","address","city","state","zip","classification","salary","commission","hourly","dob","ssn","start_date","account","routing_num","permissions","title","dept","office_email","office_phone","active"]
    rows = get_employee_rows(inactive)

    with open(file_name, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(fields)
        csvWriter.writerows(rows)
    return True

'''
def user_add_employee():
    """
    Prompts the user for employee information and adds the employee to the EMPLOYEES list.
    """
    emp_id = input('Enter employee ID: ')
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    street = input('Enter street: ')
    city = input('Enter city: ')
    state = input('Enter state: ')
    zipcode = input('Enter zipcode: ')
    add_employee(emp_id, first_name, last_name, street, city, state, zipcode)
'''

def find_employee_by_id(emp_id):
    """Returns the Employee object of a given ID."""
    for emp in EMPLOYEES:
        if emp.emp_id == emp_id:
            return emp
    return False


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
            if emp and emp.classification == 'Hourly':
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
            if emp:
                if len(line) > 1: # if the employee has receipt data
                    receipts = line[1:]

                    for receipt in receipts:
                        emp.classification.add_receipt(float(receipt))

def run_payroll():
    process_receipts()
    process_timecards()
    if os.path.exists(PAY_LOGFILE): # pay_log_file is a global variable holding ‘paylog.txt’
        os.remove(PAY_LOGFILE)
    for emp in EMPLOYEES:               # EMPLOYEES is the global list of Employee objects
        emp.issue_payment()             # issue_payment calls a method in the classification
                                        # object to compute the pay

def export_payroll(filename):
    run_payroll()

    # Save copy of payroll file; delete old file
    shutil.copyfile(PAY_LOGFILE, filename)
    if os.path.exists(PAY_LOGFILE):
        os.remove(PAY_LOGFILE)
                        


class Employee:
    def __init__(self, emp_id = 'N/A', first_name = 'N/A', last_name = 'N/A', street = 'N/A', city = 'N/A', state = 'N/A', zip = 'N/A', classification = 'N/A', salary = 'N/A', commission = 'N/A', hourly = 'N/A', dob = 'N/A', ssn = 'N/A', start_date = 'N/A', account = 'N/A', routing_num = 'N/A', permissions = 'N/A', title = 'N/A', dept = 'N/A', office_email = 'N/A', office_phone = 'N/A', active = 1):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.classification = classification
        self.salary = salary
        self.commission = commission
        self.hourly = hourly
        self.dob = dob
        self.ssn = ssn
        self.start_date = start_date
        self.account = account
        self.routing_num = routing_num
        self.permissions = permissions
        self.title = title
        self.dept = dept
        self.office_email = office_email
        self.office_phone = office_phone
        self.active = int(active)


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
        return str(self.classification)
    def get_classification(self):
        return self.classification
    def get_salary(self):
        return self.salary
    def get_commission(self):
        return self.commission
    def get_hourly(self):
        return self.hourly
    def get_dob(self):
        return self.dob
    def get_ssn(self):
        return self.ssn
    def get_start_date(self):
        return self.start_date
    def get_account(self):
        return self.account
    def get_routing_num(self):
        return self.routing_num
    def get_permissions(self):
        return int(self.permissions)
    def get_title(self):
        return self.title
    def get_dept(self):
        return self.dept
    def get_office_email(self):
        return self.office_email
    def get_office_phone(self):
        return self.office_phone
    def get_status(self):
        return self.active


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
    def set_class(self, classification):
        self.classification = classification
    def set_classification(self, classification):
        self.classification = classification
    def set_salary(self, salary):
        self.salary = salary
    def set_commission(self, commission):
        self.commission = commission
    def set_hourly(self, hourly):
        self.hourly = hourly
    def set_dob(self, dob):
        self.dob = dob
    def set_ssn(self, ssn):
        self.ssn = ssn
    def set_start_date(self, start_date):
        self.start_date = start_date
    def set_account(self, account):
        self.account = account
    def set_routing_num(self, routing_num):
        self.routing_num = routing_num
    def set_permissions(self, permissions):
        self.permissions = permissions
    def set_title(self, title):
        self.title = title
    def set_dept(self, dept):
        self.dept = dept
    def set_office_email(self, office_email):
        self.office_email = office_email
    def set_office_phone(self, office_phone):
        self.office_phone = office_phone
    def set_status(self, status):
        self.active = int(status) 

    def make_salaried(self, salary):
        """Changes employee classification to 'salaried' with the given salary."""
        self.classification = Salaried(salary)

    def make_commissioned(self, salary, commision_rate):
        """Changes employee classification to 'commissioned'
        with the given salary and commission rate."""
        self.classification = Commissioned(salary, commision_rate)

    def make_hourly(self, hourly_rate):
        """Changes employee classification to 'hourly' with the given hourly rate."""
        self.classification = Hourly(hourly_rate)

    def issue_payment(self):
        """Appends employee payment information to paylog.txt"""
        pay = self.classification.compute_pay()
        message = f'Mailing {pay:0.2f} to {self.first_name} {self.last_name} at '\
        f'{self.street} {self.city} {self.state} {self.zip}\n'

        with open('paylog.txt', 'a', encoding="utf-8") as out_file:
            out_file.write(message)
    
    def get_payment(self):
        return self.classification.compute_pay()

    def get_data(self):
        """Returns a list of all the employee's data."""
        #change classification to string
        if self.get_classification == 'Salary':
            self.classification = 1
        return [self.emp_id, self.first_name, self.last_name, self.street, self.city, self.state, self.zip, str(self.classification), self.salary, self.commission, self.hourly, self.dob, self.ssn, self.start_date, self.account, self.routing_num, self.permissions, self.title, self.dept, self.office_email, self.office_phone, self.active]


class Classification:
    def compute_pay(self):
        """Abstract method for computing pay."""

class Salaried(Classification):
    def __init__(self, salary):
        self.salary = salary

    def __str__(self):
        return 'Salary'

    def compute_pay(self): # override method
        """Returns the employee's salaried pay."""
        pay = self.salary / 24 # 24 pay periods per year
        return round(pay, 2)

class Commissioned(Salaried):
    def __init__(self, salary, commission_rate):
        super().__init__(salary)
        self.commission_rate = commission_rate / 100
        self._receipts = []
    
    def __str__(self):
        return 'Commission'


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

    def __str__(self):
        return 'Hourly'

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
    #process_timecards()
    #process_receipts()
    #run_payroll()

    # Save copy of payroll file; delete old file
    #shutil.copyfile(PAY_LOGFILE, 'paylog_old.csv')
    #if os.path.exists(PAY_LOGFILE):
        #os.remove(PAY_LOGFILE)

    # export_payroll()
'''
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
'''
if __name__ == '__main__':
    main()