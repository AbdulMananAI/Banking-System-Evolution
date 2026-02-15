#include <iostream>
#include <fstream>
#include <string>
using namespace std;

const int WITHDRAW_LIMIT = 300000;

string Acc_num[100];
string Acc_name[100];
string Acc_surname[100];
float Acc_balance[100];
int Acc_password[100];
int totalAccounts = 0;

void saveData() {
    ofstream file("bank_data.txt");
    for (int i = 0; i < totalAccounts; i++) {
        file << Acc_num[i] << " " << Acc_name[i] << " " << Acc_surname[i] << " " << Acc_balance[i] << " " << Acc_password[i] << endl;
    }
    file.close();
}

void loadData() {
    ifstream file("bank_data.txt");
    if (!file) return;
    totalAccounts = 0;
    while (file >> Acc_num[totalAccounts] >> Acc_name[totalAccounts] >> Acc_surname[totalAccounts] >> Acc_balance[totalAccounts] >> Acc_password[totalAccounts]) {
        totalAccounts++;
    }
    file.close();
}

int findAccount(string cnic) {
    for (int i = 0; i < totalAccounts; i++) {
        if (Acc_num[i] == cnic) {
            return i;
        }
    }
    return -1;
}

bool login(string cnic) {
    int index = findAccount(cnic);
    if (index == -1) {
        cout << "Account not found! Please create an account or re-enter correct credentials." << endl;
        return false;
    }
    int password;
    cout << "Enter your 4-digit password: ";
    cin >> password;
    if (password == Acc_password[index]) {
        cout << "Login successful!" << endl;
        cout << "Welcome Back, " << Acc_name[index] << " " << Acc_surname[index] << endl;
        cout << "Your account number is: " << Acc_num[index] << endl;
        cout << "Your current balance is: " << Acc_balance[index] << endl;
        return true;
    } else {
        cout << "Incorrect password! Please create an account or re-enter correct credentials." << endl;
        return false;
    }
}

void accountCreation() {
    if (totalAccounts >= 100) {
        cout << "Cannot create more accounts, limit reached!" << endl;
        return;
    }
    string name, surname, cnic, phone_number;
    cout << "Enter your Name (without spaces): ";
    cin >> name;
    cout << "Enter your Surname (without spaces): ";
    cin >> surname;
    cout << "Enter your CNIC (without spaces): ";
    cin >> cnic;
    cout << "Enter your Phone number (without spaces): ";
    cin >> phone_number;
    int password, confirm_password;

    while (true) {
        cout << "Enter your 4-digit Password: ";
        cin >> password;
        cout << "Confirm Password: ";
        cin >> confirm_password;
        if (password >= 1000 && password <= 9999) {
            if (password == confirm_password) {
                Acc_num[totalAccounts] = cnic;
                Acc_name[totalAccounts] = name;
                Acc_surname[totalAccounts] = surname;
                Acc_balance[totalAccounts] = 0.0;
                Acc_password[totalAccounts] = password;
                totalAccounts++;
                saveData();
                cout << "Your account is created successfully!" << endl;
                break;
            } else {
                cout << "Passwords do not match!" << endl;
            }
        } else {
            cout << "Invalid password! It must be a 4-digit number." << endl;
        }
    }
}

void performTransaction(int option, int index, float &balance, float &currentBalance) {
    if (option == 1) {
        int amount;
        cout << "Enter amount to deposit: ";
        cin >> amount;
        if (amount > 0) {
            balance += amount;
            Acc_balance[index] = balance;
            currentBalance = balance;
            saveData();
            cout << "Deposit successful!" << endl;
            cout << "Remaining Balance: " << currentBalance << endl;
        } else {
            cout << "Invalid amount!" << endl;
        }
    } else if (option == 2) {
        int amount;
        cout << "Enter amount to withdraw: ";
        cin >> amount;
        if (amount > 0 && amount <= WITHDRAW_LIMIT) {
            if (amount <= balance) {
                balance -= amount;
                Acc_balance[index] = balance;
                currentBalance = balance;
                saveData();
                cout << "Withdrawal successful!" << endl;
                cout << "Remaining Balance: " << currentBalance << endl;
            } else {
                cout << "Not enough balance!" << endl;
            }
        } else {
            cout << "Amount exceeds withdrawal limit of " << WITHDRAW_LIMIT << "!" << endl;
        }
    } else if (option == 3) {
        cout << "Current Balance: " << currentBalance << endl;
    }
}

void showMainMenu() {
    system("cls");
    cout << "********************************************************************************" << endl;
    cout << "                  WELCOME TO BANK MANAGEMENT SYSTEM" << endl;
    cout << "********************************************************************************" << endl;
    cout << "1. LOGIN TO YOUR ACCOUNT" << endl;
    cout << "2. CREATE A NEW ACCOUNT" << endl;
    cout << "3. EXIT PROGRAM" << endl;
    cout << "Enter your choice: ";
}

int main() {
    loadData();
    while (true) {
        showMainMenu();
        int choice;
        cin >> choice;

        if (choice == 1) {
            string cnicInput;
            cout << "Enter your CNIC: ";
            cin >> cnicInput;
            if (login(cnicInput)) {
                int index = findAccount(cnicInput);
                float balance = Acc_balance[index];
                float currentBalance = balance;

                while (true) {
                    cout << "\n**********************************************************************************" << endl;
                    cout << "\n                                     SUB MENU                                     " << endl;
                    cout << "\n**********************************************************************************" << endl;
                    cout << "1. Deposit Money" << endl;
                    cout << "2. Withdraw Money" << endl;
                    cout << "3. Check Balance" << endl;
                    cout << "4. Exit" << endl;
                    cout << "Enter your option (1-4): ";
                    int option;
                    cin >> option;

                    if (option >= 1 && option <= 3) {
                        performTransaction(option, index, balance, currentBalance);
                    } else if (option == 4) {
                        cout << "Thank you for using the system!" << endl;
                        break;
                    } else {
                        cout << "Invalid choice! Please enter 1-4." << endl;
                    }
                }
            }
        } else if (choice == 2) {
            accountCreation();
        } else if (choice == 3) {
            cout << "Thank you for using Bank Management System!" << endl;
            break;
        } else {
            cout << "Invalid choice! Please enter 1-3." << endl;
        }
    }
    return 0;
}

/*
CODE PURPOSE:
This is a basic console-based Bank Management System using C++.
It allows users to Create Accounts, Login, Deposit, Withdraw, and Check Balance.
It uses file handling (bank_data.txt) to save data so it isn't lost when the program closes.

LIMITATIONS:
1. Fixed Array Size: It can only store up to 100 accounts (Acc_num[100]).
2. No Encryption: Passwords and data are stored in plain text in the file.
3. No Space Support: Names cannot contain spaces (e.g., "Abdul Manan" will break the file reading).
4. Single User: Only one user can access the file at a time; not suitable for real-world banking.
*/
