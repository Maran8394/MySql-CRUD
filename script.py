import psycopg2

class Signin():
    def __init__(self):
        self.con = psycopg2.connect(
            database = "atm",
            user="postgres",
            password='msword',
            host = "127.0.0.1", port = "5432"
        )
        self.cursor = self.con.cursor()
        choice = int(input("1.LOGIN\n2.REGISTER\n"))
        if choice == 1:
            self.login()
            
        else:
            x, y = self.register()
            self.login(x,y)
            
        
    def register(self):
        acc_no = int(input('Enter your account number: '))
        pin_number = int(input("Enter pin number: "))
        self.cursor.execute(f"INSERT INTO account(account_number,pin_number) VALUES({acc_no},{pin_number})")
        self.con.commit()
        print("Succesfully registerd....")
        return [acc_no,pin_number]

    def login(self):
        acc_no = int(input('Enter your account number: '))
        pin_number = int(input("Enter pin number: "))
        self.cursor.execute(F"SELECT EXISTS(SELECT account_number, pin_number, total_amount FROM account WHERE account_number={acc_no} AND pin_number={pin_number});")
        r = self.cursor.fetchone()
        if False in r:
            print("Incorrect credintials")
            return
        else:
            self.operation(acc_no, pin_number)

    def operation(self,acc_no, pin_number):
        choice = int(input("1.Debit\n2.Deposit\n3.View Balance\n"))
        if choice == 1:
            self.cursor.execute(F"SELECT total_amount FROM account WHERE account_number={acc_no} AND pin_number={pin_number};")
            bal = self.cursor.fetchone()
            debit_amount = int(input("Enter how much want to debit: "))
            if debit_amount > bal[0]:
                print("You dont have that much amount\n please enter less than your current balance\nyour balance is",bal[0])
                self.operation(acc_no,pin_number)
            else:
                current_bal = bal[0] - debit_amount
                self.cursor.execute(F"UPDATE account SET total_amount={current_bal} WHERE account_number={acc_no} AND pin_number={pin_number};")
                print("Amount debited...")
        if choice == 2:
            self.cursor.execute(F"SELECT total_amount FROM account WHERE account_number={acc_no} AND pin_number={pin_number};")
            bal = self.cursor.fetchone()
            deposit_amount = int(input("Enter how much want to deposit: "))
            current_bal = bal[0] + deposit_amount
            self.cursor.execute(F"UPDATE account SET total_amount={current_bal} WHERE account_number={acc_no} AND pin_number={pin_number};")
            print("successfully deposited...")
        else:
            self.cursor.execute(F"SELECT total_amount FROM account WHERE account_number={acc_no} AND pin_number={pin_number};")
            bal = self.cursor.fetchone()
            print("Your balance is ",bal[0])
            
# print("Welcome")
# acc_no = int(input("Enter your Account Number "))
# pin_number = int(input("Enter Your Pin number "))

Signin()