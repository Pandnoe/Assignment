# import sqlite3

# DB_NAME = "users.db"

# def init_db():
#     """Initialize the database and create the users table if it doesn't exist."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         )
#     """)
#     c.execute('''CREATE TABLE IF NOT EXISTS dengue_reports (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER,
#                     description TEXT,
#                     report_type TEXT,
#                     date TEXT,
#                     FOREIGN KEY (user_id) REFERENCES users(id))''')
#     conn.commit()
#     conn.close()

# def register_user(username, password):
#     """Register a new user in the database."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     try:
#         c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         conn.close()
#         return True, "Registration successful."
#     except sqlite3.IntegrityError:
#         conn.close()
#         return False, "Username already exists!"

# def login_user(username, password):
#     """Check if the username/password combination exists."""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
#     user = c.fetchone()
#     conn.close()
#     return user

# def change_password(username, new_password):
#     """Change password for user"""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
#     conn.commit()
#     conn.close()
#     return True

# def addDengueReport(user_id, description, report_type):
#     """Add Dengue report for user"""
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("INSERT INTO dengue_reports (user_id, description, report_type, date) VALUES (?, ?, ?, CURRENT_DATE)", (user_id, description,report_type))
#     conn.commit()
#     conn.close()

# def showDengueReports():
#     conn = sqlite3.connect(DB_NAME)
#     c = conn.cursor()
#     c.execute("SELECT * FROM dengue_reports")
#     reports = c.fetchall()
#     conn.close()
#     for report in reports:
#         print(report)


import os
import time
from convert_data import convertData


DB_FILE = "users.txt"

def init_db():
    """Initialize the database by creating the users file if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            f.write("id,username,password\n")

def register_user(username, password):
    """Register a new user in the database."""
    with open(DB_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            user_id, user_name, user_password = line.strip().split(',')
            if user_name == username:
                return False, "Username already exists!"
    
    user_id = len(lines)
    with open(DB_FILE, 'a') as f:
        f.write(f"{user_id},{username},{password}\n")
    return True, "Registration successful, logging in."

def login_user(username, password):
    """Check if the username/password combination exists."""
    with open(DB_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            user_id, user_name, user_password = line.strip().split(',')
            if user_name == username and user_password == password:
                return (user_id, username)
    return None

# def change_password(username, new_password):
#     """Change password for user"""
#     lines = []
#     with open(DB_FILE, 'r') as f:
#         lines = f.readlines()
    
#     with open(DB_FILE, 'w') as f:
#         for line in lines:
#             user_id, user_name, user_password = line.strip().split(',')
#             if user_name == username:
#                 f.write(f"{user_id},{username},{new_password}\n")
#             else:
#                 f.write(line)
#     return True

def change_password(username, new_password):
    """Change password for user only if the new password is different from the current one."""
    lines = []
    with open(DB_FILE, 'r') as f:
        lines = f.readlines()
    
    # The first line is the header
    header = lines[0]
    data_lines = lines[1:]
    
    old_password = None
    for line in data_lines:
        user_id, user_name, user_password = line.strip().split(',')
        if user_name == username:
            old_password = user_password
            break

    # If the new password is the same as the current password, do not update
    if old_password is not None and new_password == old_password:
        return False

    # Write the updated data back to the file
    with open(DB_FILE, 'w') as f:
        f.write(header)
        for line in data_lines:
            user_id, user_name, user_password = line.strip().split(',')
            if user_name == username:
                f.write(f"{user_id},{username},{new_password}\n")
            else:
                f.write(line + "\n")
    return True


def addDengueReport(user_id, description, report_type, latitude, longitude):
    """Add Dengue report for user"""
    # This function will need a separate text file for dengue reports
    REPORT_FILE = "dengue_reports.txt"
    if not os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'w') as f:
            f.write("id,user_id,description,report_type,date,latitude,longitude\n")
    
    with open(REPORT_FILE, 'r') as f:
        lines = f.readlines()
    
    report_id = len(lines)
    with open(REPORT_FILE, 'a') as f:
        f.write(f"{report_id},{user_id},{description},{report_type},{time.strftime('%Y-%m-%d')},{latitude},{longitude} \n")

def showDengueReports():
    REPORT_FILE = "dengue_reports.txt"
    if not os.path.exists(REPORT_FILE):
        print("No reports found.")
        return
    
    with open(REPORT_FILE, 'r') as f:
        lines = f.readlines()
    
    if len(lines) < 2:
        return
    header = lines[0].strip().split(',')
    data = []

    for line in lines[1:]:
        values = line.strip().split(',')
        row = dict(zip(header,values))
        data.append(row)  
        
    return data
