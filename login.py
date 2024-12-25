'''
Gets table information
'''

import sqlite3
import getpass
from datetime import datetime
import os

db_path = "prj-sample.db"

def connect_db(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    connection.commit()
    return connection, cursor

def validate_email(email):
    if "@" in email and "." in email: 
        at_index = email.index("@") 
        dot_index = email.index(".", at_index) 
        # Check if there's at least one character before, between, and after 
        if at_index > 0 and dot_index > at_index + 1 and dot_index < len(email) - 1: 
            return True 
    return False

def login(connection, cursor):
    usr = input("User ID: ")
    password = getpass.getpass("Password: ")

    cursor.execute('''SELECT * FROM users WHERE usr = ? AND pwd = ?''', (usr, password))
    user = cursor.fetchone()

    if user:
        print(f"Welcome back, {user[1]}!")
        return usr
    else:
        print("Invalid user ID or password.")
        return None

def sign_up(connection, cursor):

    name = input("Name: ")
    email = input("Email: ")
    if not validate_email(email):
        print("Invalid email format. Email must contain '@' and '.'.")
        return
    phone = input("Phone: ")
    try:
        int(phone)
    except:
        print("Invalid phone number! Please only use numbers")
        return
    password = getpass.getpass("Password: ")
    
    cursor.execute('SELECT MAX(usr) FROM users;')
    last_usr = cursor.fetchone()[0]
    usr = (last_usr + 1) if last_usr else 1  # Assign a new user ID
    
    cursor.execute('''INSERT INTO users (usr, name, email, phone, pwd) VALUES (?, ?, ?, ?, ?);''', (usr, name, email, phone, password))
    connection.commit()
    print(f"Sign-up successful! Your User ID is {usr}.")
    return usr

def login_screen(connection, cursor):
    while True:
        print("\nWelcome! Choose an option:")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")
        choice = input("Enter choice (1-3): ")

        if choice == "1":
            user = login(connection, cursor)
            if user is not None:
                return user
        if choice == "2":
            user = sign_up(connection, cursor)
            return user
        elif choice == "3":
            print("Exiting program.")
            connection.close()
            exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    db_path = "prj-sample.db"
    connection, cursor = connect_db(db_path)
    login_screen(connection, cursor)


            
