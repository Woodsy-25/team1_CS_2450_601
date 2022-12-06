'''
Testing file for payroll.py
'''

from payroll import Employee
import pytest

def create_employee():
    '''
    Creates an employee
    '''
    emp = payroll.Employee("John", "Smith", 1000)
    assert emp.first_name == "John"
    assert emp.last_name == "Smith"
    assert emp.salary == 1000