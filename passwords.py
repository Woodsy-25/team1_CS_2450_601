import bcrypt
import csv

def check_pass(name, pw):
    with open('encrypted.csv', 'r') as incsv:
        pass_list = []
        read_csv = csv.reader(incsv)
        for read in read_csv:
            pass_list.append(read)
        print(pass_list)

        pw_b = pw.encode('utf-8')
        t_name = False
        for user in pass_list:
            if user[0] == name:
                pch = user[1].encode()
                if bcrypt.checkpw(pw_b, pch):
                    t_name = True
        if t_name == True:
            print("Login Success!")
        else:
            print("Sorry wrong username or password")

def encrypt_file():
    pass_list = []
    salt = bcrypt.gensalt()
    with open('logins.csv', 'r') as incsv:
        csv_r = csv.reader(incsv)
        for lines in csv_r:
            pass_byte = lines[1].encode('utf-8')
            lines[1] = bcrypt.hashpw(pass_byte, salt)
            pass_list.append(lines)
    # print(pass_list)
    with open('encrypted.csv', 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        for row in pass_list:
            row[1] = row[1].decode()
            writer.writerow(row)

def main_test():
    encrypt_file()
    check_pass('admin', 'admin')    



if __name__ == "__main__":
    main_test()