import os
import time
import gspread
from google.oauth2.service_account import Credentials

# Define the API scopes required for read and write operations.
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Load your service account credentials.
#SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON', 'service_account.json')
#creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPE)

gc = gspread.authorize(creds)

# Get the Google Sheet IDs from environment variables.
USERS_SHEET_ID = os.environ.get("USERS_SHEET_ID", "1nyNOU4znrMNXdYwWoo2yKX9Qx7j81madJzMKaBM-UYU")
REPORTS_SHEET_ID = os.environ.get("REPORTS_SHEET_ID", "1Iem_WqJFyIy6xOAwODCy5MuCge1w_kwyFT2h9pf_jYk")

# Open the first worksheet from each Google Sheet.
users_sheet = gc.open_by_key(USERS_SHEET_ID).sheet1
reports_sheet = gc.open_by_key(REPORTS_SHEET_ID).sheet1

def init_db():
    """
    Initialize the Google Sheets "database" by ensuring each sheet has the correct headers.
    If the header row does not match, the sheet is cleared and the headers are set.
    """
    # Expected headers for the users sheet.
    users_headers = ["id", "username", "password"]
    current_users_headers = users_sheet.row_values(1)
    if current_users_headers != users_headers:
        users_sheet.clear()
        users_sheet.append_row(users_headers)
    
    # Expected headers for the dengue reports sheet.
    reports_headers = [
        "report_id", "user_id", "username", "report_type", "date",
        "latitude", "longitude", "symptom", "severity", "hotspot_type", "image_filename"
    ]
    current_reports_headers = reports_sheet.row_values(1)
    if current_reports_headers != reports_headers:
        reports_sheet.clear()
        reports_sheet.append_row(reports_headers)

def get_next_user_id():
    """
    Calculate the next available user id by reading the current rows in the users sheet.
    """
    users = users_sheet.get_all_values()
    if len(users) < 2:
        return 1
    # Extract numeric IDs from the first column (skipping the header).
    ids = [int(row[0]) for row in users[1:] if row[0].isdigit()]
    return max(ids) + 1 if ids else 1

def register_user(username, password):
    """
    Register a new user in the users sheet.
    Returns a tuple (success: bool, message: str).
    """
    users = users_sheet.get_all_values()
    for row in users[1:]:
        if row[1] == username:
            return False, "Username already exists!"
    new_id = get_next_user_id()
    users_sheet.append_row([new_id, username, password])
    return True, "Registration successful, logging in."

def login_user(username, password):
    """
    Check if the username/password combination exists in the users sheet.
    Returns a tuple (user_id, username) if found, otherwise None.
    """
    users = users_sheet.get_all_values()
    for row in users[1:]:
        if row[1] == username and row[2] == password:
            return (row[0], username)
    return None

def change_password(username, new_password):
    """
    Change the password for a user if the new password differs from the current one.
    Returns True if the password was changed, otherwise False.
    """
    users = users_sheet.get_all_values()
    for i, row in enumerate(users[1:], start=2):  # Data starts on row 2 (after header)
        if row[1] == username:
            if row[2] == new_password:
                return False
            users_sheet.update_cell(i, 3, new_password)  # Column 3 holds the password.
            return True
    return False

def get_all_users():
    """
    Retrieve all users from the users sheet as a list of dictionaries.
    """
    users = users_sheet.get_all_values()
    if len(users) < 2:
        return []
    headers = users[0]
    result = []
    for row in users[1:]:
        # Pad missing fields if necessary.
        if len(row) < len(headers):
            row += [""] * (len(headers) - len(row))
        result.append(dict(zip(headers, row)))
    return result

def remove_user(user_id):
    """
    Remove the user with the specified user id from the users sheet.
    """
    users = users_sheet.get_all_values()
    for i, row in enumerate(users[1:], start=2):
        if row[0] == str(user_id):
            delete_row_alternative(users_sheet, i)
            break


def get_next_report_id():
    """
    Calculate the next available report id from the dengue reports sheet.
    """
    reports = reports_sheet.get_all_values()
    if len(reports) < 2:
        return 1
    ids = [int(row[0]) for row in reports[1:] if row[0].isdigit()]
    return max(ids) + 1 if ids else 1

def addDengueReport(user_id, username, report_type, latitude, longitude, symptom=None, severity=None, hotspot_type=None):
    """
    Add a new dengue report to the reports sheet.
    Returns the report id of the inserted report.
    """
    report_id = get_next_report_id()
    date = time.strftime('%Y-%m-%d')
    symptom = symptom or ""
    severity = severity or ""
    hotspot_type = hotspot_type or ""
    reports_sheet.append_row([
        report_id, user_id, username, report_type, date,
        latitude, longitude, symptom, severity, hotspot_type, ""
    ])
    return report_id

def showDengueReports():
    """
    Retrieve all dengue reports from the reports sheet as a list of dictionaries.
    """
    reports = reports_sheet.get_all_values()
    if len(reports) < 2:
        return []
    headers = reports[0]
    result = []
    for row in reports[1:]:
        if len(row) < len(headers):
            row += [""] * (len(headers) - len(row))
        result.append(dict(zip(headers, row)))
    return result

def remove_report(report_id):
    """
    Remove a dengue report from the reports sheet by its report id.
    """
    reports = reports_sheet.get_all_values()
    for i, row in enumerate(reports[1:], start=2):
        if row[0] == str(report_id):
            delete_row_alternative(reports_sheet, i)
            break


def update_report_image(report_id, image_filename):
    """
    Update the image_filename field for a specified dengue report.
    """
    reports = reports_sheet.get_all_values()
    for i, row in enumerate(reports[1:], start=2):
        if row[0] == str(report_id):
            # Column 11 holds the image_filename.
            reports_sheet.update_cell(i, 11, image_filename)
            break

def delete_row_alternative(worksheet, row_index):
    # Build the request body to delete a row.
    body = {
        "requests": [{
            "deleteDimension": {
                "range": {
                    "sheetId": worksheet.id,
                    "dimension": "ROWS",
                    "startIndex": row_index - 1,  # 0-indexed, so subtract 1.
                    "endIndex": row_index         # endIndex is exclusive.
                }
            }
        }]
    }
    worksheet.spreadsheet.batch_update(body)
