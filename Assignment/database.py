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

# def register_user(username, password):
#     """Register a new user in the database."""
#     with open(DB_FILE, 'r') as f:
#         lines = f.readlines()
#         for line in lines[1:]:
#             user_id, user_name, user_password = line.strip().split(',')
#             if user_name == username:
#                 return False, "Username already exists!"
    
#     # Determine a unique new user id by finding the maximum existing id
#     new_id = 1
#     if len(lines) > 1:
#         try:
#             existing_ids = [int(line.strip().split(',')[0]) for line in lines[1:] if line.strip()]
#             if existing_ids:
#                 new_id = max(existing_ids) + 1
#         except Exception as e:
#             new_id = len(lines)
    
#     with open(DB_FILE, 'a') as f:
#         f.write(f"{new_id},{username},{password}\n")
#     return True, "Registration successful, logging in."

def register_user(username, password):
    with open(DB_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue  # Skip malformed lines
            _, user_name, _ = parts
            if user_name == username:
                return False, "Username already exists!"

    # Calculate new ID safely
    existing_ids = [int(parts[0]) for parts in (line.strip().split(',') for line in lines[1:])
                    if len(parts) == 3 and parts[0].isdigit()]
    new_id = max(existing_ids, default=0) + 1

    with open(DB_FILE, 'a') as f:
        f.write(f"{new_id},{username},{password}\n")
    return True, "Registration successful, logging in."



# def login_user(username, password):
#     """Check if the username/password combination exists."""
#     with open(DB_FILE, 'r') as f:
#         lines = f.readlines()
#         for line in lines[1:]:
#             user_id, user_name, user_password = line.strip().split(',')
#             if user_name == username and user_password == password:
#                 return (user_id, username)
#     return None

def login_user(username, password):
    with open(DB_FILE, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue  # Skip malformed lines
            user_id, user_name, user_password = parts
            if user_name == username and user_password == password:
                return (user_id, username)
    return None


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

def get_all_users():
    """Return a list of all users as dictionaries from the users.txt file."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        lines = f.readlines()
    if len(lines) < 2:
        return []
    header = lines[0].strip().split(',')
    users = []
    for line in lines[1:]:
        fields = line.strip().split(',')
        if len(fields) >= len(header):
            user = dict(zip(header, fields))
            users.append(user)
    return users

def remove_user(user_id):
    """Remove the user with the given user_id from the users.txt file."""
    if not os.path.exists(DB_FILE):
        return
    with open(DB_FILE, 'r') as f:
        lines = f.readlines()
    header = lines[0]
    new_lines = [header]
    for line in lines[1:]:
        fields = line.strip().split(',')
        if fields[0] != str(user_id):
            # Preserve the original newline if present.
            new_lines.append(line if line.endswith("\n") else line + "\n")
    with open(DB_FILE, 'w') as f:
        f.writelines(new_lines)



def addDengueReport(user_id, username, report_type, latitude, longitude, symptom=None, severity=None, hotspot_type=None):

    #For a 'Report person' type, provide symptom and severity.
    #For a 'Report Location' type, provide hotspot_type.

    REPORT_FILE = "dengue_reports.txt"
    
    # Create the report file with a header if it doesn't exist
    if not os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'w') as f:
            f.write("report_id,user_id,username,report_type,date,latitude,longitude,symptom,severity,hotspot_type\n")
    
    # Read all lines to determine the next report_id
    with open(REPORT_FILE, 'r') as f:
        lines = f.readlines()
    
    report_id = len(lines)  # header counts as first line; adjust if needed
    
    # Replace None with empty strings for fields not applicable to the report type
    symptom = symptom if symptom is not None else ""
    severity = severity if severity is not None else ""
    hotspot_type = hotspot_type if hotspot_type is not None else ""
    
    with open(REPORT_FILE, 'a') as f:
        f.write(f"{report_id},{user_id},{username},{report_type},{time.strftime('%Y-%m-%d')},{latitude},{longitude},{symptom},{severity},{hotspot_type}\n")

    return report_id


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

def remove_report(report_id):
    """
    Remove a dengue report with the specified report_id from the dengue_reports.txt file.
    """
    REPORT_FILE = "dengue_reports.txt"
    if not os.path.exists(REPORT_FILE):
        return

    with open(REPORT_FILE, "r") as f:
        lines = f.readlines()

    header = lines[0]
    new_lines = [header]
    for line in lines[1:]:
        # Assuming CSV fields: id,user_id,report_type,date,latitude,longitude
        fields = line.strip().split(',')
        if fields[0] != str(report_id):
            new_lines.append(line)

    with open(REPORT_FILE, "w") as f:
        f.writelines(new_lines)

import os

def update_report_image(report_id, image_filename):
    """
    Update the report with the specified report_id in the dengue_reports.txt file
    so that its 'image_filename' field is set to image_filename.
    """
    REPORT_FILE = "dengue_reports.txt"
    if not os.path.exists(REPORT_FILE):
        return

    # Read all lines from the file.
    with open(REPORT_FILE, "r") as f:
        lines = f.readlines()

    # Process the header.
    header = lines[0].strip().split(',')
    # If the header doesn't have "image_filename", add it.
    if "image_filename" not in header:
        header.append("image_filename")
        new_lines = [','.join(header) + "\n"]
        # Add an empty image_filename field for existing rows.
        for line in lines[1:]:
            new_lines.append(line.strip() + ",\n")
        lines = new_lines
    # Now, update the report row matching report_id.
    updated_lines = []
    for line in lines:
        # Leave the header unchanged.
        if line.startswith("id,"):
            updated_lines.append(line)
            continue
        fields = line.strip().split(',')
        if fields[0] == str(report_id):
            # Ensure the row has enough columns.
            if len(fields) < len(header):
                fields.extend([""] * (len(header) - len(fields)))
            # Update the last column (image_filename) with the new filename.
            fields[-1] = image_filename
            updated_lines.append(','.join(fields) + "\n")
        else:
            updated_lines.append(line)

    with open(REPORT_FILE, "w") as f:
        f.writelines(updated_lines)
