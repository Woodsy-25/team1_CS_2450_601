import random
emps = []

with open ('employees.csv', 'r', encoding="utf-8") as in_file:
    for line in in_file:
        
        line = line.strip().split(',')
        emps.append(line)

def rando_dob():
    year = random.randint(1970, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{month}-{day}-{year}'

def rando_ssn():
    ssn = ''
    for i in range(9):
        ssn += str(random.randint(0, 9))
        #formatting
        if i == 2 or i == 4:
            ssn += '-'
    return ssn

def rando_start_date():
    year = random.randint(2000, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f'{month}-{day}-{year}'

def rando_bank_account():
    bank_account = ''
    #between 8 and 12 digits
    for i in range(random.randint(8, 12)):
        bank_account += str(random.randint(0, 9))

    return bank_account

def rando_routing_number():
    routing_number = ''
    for i in range(9):
        routing_number += str(random.randint(0, 9))

    return routing_number

#email will be first initial + last name + @gmail.com
def email_generator(first_name, last_name):
    first_initial = first_name[0]
    email = first_initial + '.' + last_name + '@gmail.com'
    return email

def rando_phone_number():
    phone_number = ''
    for i in range(10):
        phone_number += str(random.randint(0, 9))
        #formatting
        if i == 2 or i == 5:
            phone_number += '-'
    return phone_number

def permissions_generator():
    permissions = ''
    #give either a 1 or a 2 with a 90 percent chance of a 1
    if random.randint(1, 10) <= 9:
        permissions += '1'
    else:
        permissions += '2'
    return permissions

depts = ['Sales', 'Marketing', 'IT', 'HR', 'Finance', 'Engineering', 'Operations', 'Legal']
sales = ['Sales Associate', 'Sales Manager']
Marketing = ['Marketing Associate', 'Marketing Manager']
IT = ['IT Associate', 'IT Manager']
HR = ['HR Associate', 'HR Manager']
Finance = ['Finance Associate', 'Finance Manager']
Engineering = ['Engineering Associate', 'Engineering Manager']
Operations = ['Operations Associate', 'Operations Manager']
Legal = ['Legal Associate', 'Legal Manager']
def rando_dept_title():
    dept = random.choice(depts)
    title = ''
    #decide if the employee is an associate or manager but 90% of the time they are an associate
    if dept == 'Sales':
        if random.randint(1, 10) <= 9:
            title = 'Sales Associate'
        else:
            title = 'Sales Manager'
    elif dept == 'Marketing':
        if random.randint(1, 10) <= 9:
            title = 'Marketing Associate'
        else:
            title = 'Marketing Manager'
    elif dept == 'IT':
        if random.randint(1, 10) <= 9:
            title = 'IT Associate'
        else:
            title = 'IT Manager'
    elif dept == 'HR':
        if random.randint(1, 10) <= 9:
            title = 'HR Associate'
        else:
            title = 'HR Manager'
    elif dept == 'Finance':
        if random.randint(1, 10) <= 9:
            title = 'Finance Associate'
        else:
            title = 'Finance Manager'
    elif dept == 'Engineering':
        if random.randint(1, 10) <= 9:
            title = 'Engineering Associate'
        else:
            title = 'Engineering Manager'
    elif dept == 'Operations':
        if random.randint(1, 10) <= 9:
            title = 'Operations Associate'
        else:
            title = 'Operations Manager'
    elif dept == 'Legal':
        if random.randint(1, 10) <= 9:
            title = 'Legal Associate'
        else:
            title = 'Legal Manager'
    return [dept, title]

for emp in emps:
    emp[11] = rando_dob()
    emp[12] = rando_ssn()
    emp[13] = rando_start_date()
    emp[14] = rando_bank_account()
    emp[15] = rando_routing_number()
    emp[16] = permissions_generator()
    #add title and dept
    emp[17] = rando_dept_title()[1]
    emp[18] = rando_dept_title()[0]
    #add email
    emp[19] = email_generator(emp[1], emp[2])
    #add phone number
    emp[20] = rando_phone_number()
    print(emp)

#create a new csv file with the columns (id,first_name,last_name,address,city,state,zip,classification,salary,commission,hourly,dob,ssn,start_date,account,routing_num,permissions,title,dept,office_email,office_phone)
with open ('employees_with_info.csv', 'w', encoding="utf-8") as out_file:
    for emp in emps:
        out_file.write(','.join(emp) + '\n')