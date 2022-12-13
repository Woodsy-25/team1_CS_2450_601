'''
Testing file for payroll.py
'''
import pytest
from payroll import Employee


def test_create_emp():
    '''
    Creates an employee
    '''
    emp = Employee(1212,"John", "Smith",'3 Drewry Junction', 'Springfield', 'Illinois', 62794, 2, 1000, 39, 47.92, '9/1/1997', '710-77-6316', '8/20/2001', 231260459,707473871,1,'Marketing Manager','Finance','G.Solesbury@gmail.com','780-523-0874', 1)
    assert emp.emp_id == 1212
    assert emp.first_name == "John"
    assert emp.last_name == "Smith"
    assert emp.street == '3 Drewry Junction'
    assert emp.city == 'Springfield'
    assert emp.state == 'Illinois'
    assert emp.zip == 62794
    assert emp.classification == 2
    assert emp.salary == 1000
    assert emp.commission == 39
    assert emp.hourly == 47.92
    assert emp.dob == '9/1/1997'
    assert emp.ssn == '710-77-6316'
    assert emp.start_date == '8/20/2001'
    assert emp.account == 231260459
    assert emp.routing_num == 707473871
    assert emp.permissions == 1
    assert emp.title == 'Marketing Manager'
    assert emp.dept == 'Finance'
    assert emp.office_email == 'G.Solesbury@gmail.com'
    assert emp.office_phone == '780-523-0874'
    assert emp.active == 1

def test_editing_emp():
    emp = Employee(1212,"John", "Smith",'3 Drewry Junction', 'Springfield', 'Illinois', 62794, 2, 1000, 39, 47.92, '9/1/1997', '710-77-6316', '8/20/2001', 231260459,707473871,1,'Marketing Manager','Finance','G.Solesbury@gmail.com','780-523-0874', 1)
    emp.first_name = "Jane"
    emp.last_name = "Doe"
    emp.street = '123 Main St'
    emp.city = 'Springfield'
    emp.state = 'Illinois'
    emp.zip = 62794
    emp.classification = 2
    emp.salary = 1000
    emp.commission = 39
    emp.hourly = 47.92
    emp.dob = '9/1/1997'

    assert emp.first_name == "Jane"
    assert emp.last_name == "Doe"
    assert emp.street == '123 Main St'
    assert emp.city == 'Springfield'
    assert emp.state == 'Illinois'
    assert emp.zip == 62794
    assert emp.classification == 2
    assert emp.salary == 1000
    assert emp.commission == 39
    assert emp.hourly == 47.92
    assert emp.dob == '9/1/1997'