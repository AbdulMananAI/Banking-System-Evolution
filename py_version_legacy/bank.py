"""
Banking System Project
----------------------
A banking system using OOP principles (Inheritance, Polymorphism)
and file & exceptions handling for data storage.

Author: [Abdul Manan]
Date: January 2026
"""

import random
import os
from datetime import date

# --- Utilities & Validation ---
class Validator:
    @staticmethod
    def validate_name(name):
        if not name.replace(" ", "").isalpha(): 
            raise ValueError("Name must contain alphabets only.")
        if len(name) < 3:
            raise ValueError("Name is too short.")
        return name

    @staticmethod
    def validate_digits(value, field_name, length=None):
        if not value.isdigit():
            raise ValueError(f"{field_name} must contain numbers only.")
        if length and len(value) != length:
            raise ValueError(f"{field_name} must be exactly {length} digits.")
        return value

# --- Custom Exceptions ---
class InsufficientFundsError(Exception):
    pass

# --- Account Models ---
class Account:
    """PARENT CLASS: Holds common features for all accounts"""
    def __init__(self, name, fname, cnic, phone, email, balance, pin, acc_type):
        self.acc_num = str(random.randint(10000, 99999))
        self.name = name
        self.fname = fname
        self.cnic = cnic
        self.phone = phone
        self.email = email
        self.balance = float(balance)
        self.pin = pin
        self.acc_type = acc_type
        
        # Tracking daily usage
        self.last_withdraw_date = str(date.today()) 
        self.daily_withdrawn_amount = 0.0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"[SUCCESS] Deposited Rs/-{amount}. New Balance: Rs/-{self.balance}")
        else:
            raise ValueError("Amount must be positive.")

    # POLYMORPHISM: This method is a placeholder. Children MUST replace it.
    def withdraw(self, amount):
        raise NotImplementedError("Subclasses must implement this method")

    def check_info(self):
        print("\n" + "="*35)
        print(f"   [{self.acc_type} Account]") 
        print(f"   Account #:       {self.acc_num}")
        print(f"   Name:            {self.name}")
        print(f"   Father Name:     {self.fname}")
        print(f"   CNIC:            {self.cnic}")
        print(f"   Balance:         Rs/-{self.balance}")
        print("="*35 + "\n")

    def to_file_string(self):
        return f"{self.acc_num},{self.name},{self.fname},{self.cnic},{self.phone},{self.email},{self.balance},{self.pin},{self.acc_type},{self.last_withdraw_date},{self.daily_withdrawn_amount}"


class SavingsAccount(Account):
    """CHILD 1: Restricted withdrawals, Daily Limits"""
    def __init__(self, name, fname, cnic, phone, email, balance, pin):
        super().__init__(name, fname, cnic, phone, email, balance, pin, "Savings")

    def withdraw(self, amount):
        DAILY_LIMIT = 50000.0

        # 1. Reset tracker if it's a new day
        current_date = str(date.today())
        if current_date != self.last_withdraw_date:
            self.daily_withdrawn_amount = 0.0
            self.last_withdraw_date = current_date

        # 2. Check Daily Limit
        if (self.daily_withdrawn_amount + amount) > DAILY_LIMIT:
            remaining = DAILY_LIMIT - self.daily_withdrawn_amount
            raise ValueError(f"Daily limit exceeded! Remaining today: {remaining}")

        # 3. Check Balance (Cannot go negative)
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient Balance in Savings Account.")

        # 4. Execute
        self.balance -= amount
        self.daily_withdrawn_amount += amount
        print(f"[SUCCESS] Withdrawn Rs/-{amount} from Savings. New Balance: {self.balance}")


class CurrentAccount(Account):
    """CHILD 2: Flexible withdrawals, Overdraft Allowed"""
    def __init__(self, name, fname, cnic, phone, email, balance, pin):
        super().__init__(name, fname, cnic, phone, email, balance, pin, "Current")
        self.overdraft_limit = 10000.0 

    def withdraw(self, amount):
        # Logic: Allow going negative up to overdraft limit
        total_available = self.balance + self.overdraft_limit
        
        if amount > total_available:
            raise InsufficientFundsError(f"Exceeds Balance + Overdraft Limit ({self.overdraft_limit})")
        
        self.balance -= amount
        print(f"[SUCCESS] Withdrawn Rs/-{amount} from Current Account.")
        
        if self.balance < 0:
            print(f"[WARNING]  NOTE: Overdraft used. You owe the bank Rs/-{abs(self.balance)}")

# --- Database Manager ---
class BankManager:
    def __init__(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(current_folder, "bank_db.txt")
        self.accounts = [] 
        self.load_data()

    def load_data(self):
        self.accounts = []
        if not os.path.exists(self.filename):
            print("[INFO]  No database found. Creating new one.")
            return

        with open(self.filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line: continue
                
                data = line.split(",")
                
                if len(data) >= 9:
                    acc_num, name, fname, cnic, phone, email = data[0:6]
                    balance = float(data[6])
                    pin = data[7]
                    acc_type = data[8]

                    # FACTORY LOGIC: Create custom object based on type
                    if acc_type == "Savings":
                        acc = SavingsAccount(name, fname, cnic, phone, email, balance, pin)
                    elif acc_type == "Current":
                        acc = CurrentAccount(name, fname, cnic, phone, email, balance, pin)
                    else:
                        acc = SavingsAccount(name, fname, cnic, phone, email, balance, pin)

                    # Restore data
                    acc.acc_num = acc_num
                    if len(data) == 11:
                        acc.last_withdraw_date = data[9]
                        acc.daily_withdrawn_amount = float(data[10])
                    
                    self.accounts.append(acc)

    def save_data(self):
        try:
            with open(self.filename, "w") as file:
                for acc in self.accounts:
                    file.write(acc.to_file_string() + "\n")
            print(" Data saved.")
        except Exception as e:
            print(f"[WARNING] Error saving data: {e}")

    def create_new_account(self):
        print("\n---  CREATING NEW ACCOUNT ---")
        try:
            name = Validator.validate_name(input("Enter Name: "))
            fname = Validator.validate_name(input("Enter Father Name: "))
            cnic = Validator.validate_digits(input("Enter CNIC (13 digits): "), "CNIC", 13)
            phone = Validator.validate_digits(input("Enter Phone (11 digits): "), "Phone", 11)
            email = input("Enter Email: ")
            
            print("\nSelect Account Type:")
            print("1. Savings (Daily Limit 50k)")
            print("2. Current (Overdraft Allowed 10k)")
            type_choice = input("Choice (1 or 2): ")

            bal = float(input("Initial Deposit: "))
            if bal < 500: raise ValueError("Minimum deposit is 500.")
            
            pin = Validator.validate_digits(input("Set 4-digit PIN: "), "PIN", 4)
            
            if type_choice == "1":
                new_acc = SavingsAccount(name, fname, cnic, phone, email, bal, pin)
            elif type_choice == "2":
                new_acc = CurrentAccount(name, fname, cnic, phone, email, bal, pin)
            else:
                raise ValueError("Invalid Account Type")

            self.accounts.append(new_acc)
            self.save_data()
            print(f"\n🎉 {new_acc.acc_type} Account Created! Number: {new_acc.acc_num}")
            
        except ValueError as e:
            print(f"\n[ERROR] REGISTRATION FAILED: {e}")

    def find_account(self, acc_num):
        for acc in self.accounts:
            if acc.acc_num == acc_num:
                return acc
        return None

# --- Main Application ---
if __name__ == "__main__":
    manager = BankManager()
    
    while True:
        print("\n" + "="*35)
        print("     PYTHON BANKING SYSTEM  ")
        print("="*35)
        print(" [1] Login (Deposit/Withdraw)")
        print(" [2] Create New Account")
        print(" [3] Admin Panel")
        print(" [0] Exit")
        
        choice = input("\n Enter Choice: ")
        
        if choice == "1":
            acc_num = input("Enter Account Number: ")
            user = manager.find_account(acc_num)
            
            if user:
                pin = input("Enter PIN: ")
                if user.pin == pin:
                    print(f"\n[SUCCESS] Welcome, {user.name}!")
                    while True:
                        print("\n   [1] Deposit  [2] Withdraw  [3] Check Info  [0] Logout")
                        sub = input("   Action: ")
                        if sub == "1":
                            try:
                                amt = float(input("   Amount: "))
                                user.deposit(amt)
                                manager.save_data()
                            except ValueError as e: print(f"   [ERROR] {e}")
                        elif sub == "2":
                            try:
                                amt = float(input("   Amount: "))
                                user.withdraw(amt) # POLYMORPHISM HAPPENS HERE
                                manager.save_data()
                            except Exception as e: print(f"   [ERROR] {e}")
                        elif sub == "3":
                            user.check_info()
                        elif sub == "0":
                            break
                else:
                    print("[ERROR] Wrong PIN!")
            else:
                print("[ERROR] Account not found.")

        elif choice == "2":
            manager.create_new_account()

        elif choice == "3":
            print("\n ADMIN ACCESS")
            pwd = input("Password: ")
            if pwd == "admin123":
                print(f"\n{'ACC #':<10} | {'TYPE':<10} | {'NAME':<15} | {'BALANCE':<10}")
                print("-" * 55)
                for acc in manager.accounts:
                    print(f"{acc.acc_num:<10} | {acc.acc_type:<10} | {acc.name:<15} | {acc.balance:<10}")
            else:
                print("[ERROR] Access Denied.")

        elif choice == "0":
            print("Goodbye! ")
            break