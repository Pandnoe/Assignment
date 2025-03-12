# import streamlit as st
# from database import init_db, register_user, login_user

# # Initialize the database (creates the DB file and table if they don't exist)
# init_db()

# # Initialize session state for login status
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # If user is not logged in, show login/registration forms
# if not st.session_state.logged_in:
#     st.title("User Login / Registration")
#     option = st.radio("Select an option", ["Login", "Register"])

#     if option == "Login":
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         if st.button("Login"):
#             if login_user(username, password):
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.success("Logged in!")
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials!")
#     else:
#         st.title("User Registration")
#         reg_username = st.text_input("Choose a Username", key="reg_username")
#         reg_password = st.text_input("Choose a Password", type="password", key="reg_password")
#         reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
#         if st.button("Register"):
#             if reg_password != reg_password_confirm:
#                 st.error("Passwords do not match!")
#             else:
#                 success, message = register_user(reg_username, reg_password)
#                 if success:
#                     st.success(message)
#                 else:
#                     st.error(message)

# # If the user is logged in, show the map (importing the map module)
# if st.session_state.logged_in:
#     st.title("Group 4 Dengue Tracker")
#     st.write(f"Welcome, {st.session_state.username}!")
#     from map import render_map  # map.py contains the map rendering function
#     render_map()

#     col1, col2, col3 = st.columns([1,1,1])
#     with col1:
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.rerun()
#     with col2:
#         if st.button("Settings"):
#             st.switch_page("pages/settings.py")
#     with col3:
#         if st.button("Reporting"):
#             st.switch_page("pages/report.py")

###################################################################################### 

# import streamlit as st
# from database import *
# from widgets.progressbar import showProgressBar
# from weather import show_weather  # Import the weather display function
# import time
# from streamlit_js_eval import (
#     get_geolocation,
#     get_user_agent,
#     get_browser_language,
#     get_page_location,
#     copy_to_clipboard,
#     create_share_link,
# )

# # Inject custom CSS
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# local_css("styles.css")

# # Initialize the database (creates the DB file and table if they don't exist)
# init_db()

# # Initialize session state for login status and weather toggle
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "show_weather" not in st.session_state:
#     st.session_state["show_weather"] = False
# if "latitude" not in st.session_state:
#     st.session_state.latitude = None
# if "longitude" not in st.session_state:
#     st.session_state.longitude = None

# if st.session_state.latitude is None or st.session_state.longitude is None:
#     loc = get_geolocation(component_key="geoloc")
#     if loc:
#         # Assuming that your frontend returns a JSON object with 'latitude' and 'longitude'
#         st.session_state.latitude = loc['coords']['latitude']
#         st.session_state.longitude = loc['coords']['longitude']
#         st.write(f"Retrieved geolocation: {loc}")
#     else:
#         st.write("Unable to automatically fetch geolocation.")

# # If user is not logged in, show login/registration forms
# if not st.session_state.logged_in:
#     st.title("User Login / Registration")
#     option = st.radio("Select an option", ["Login", "Register", "Forgot Password"])

#     if option == "Login":
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")
#         if st.button("Login"):
#             user = login_user(username,password)
#             if user is not None:
#                 st.session_state.logged_in = True
#                 st.session_state.username = username
#                 st.session_state.userId = user[0]
#                 st.success("Logged in!")
#                 showProgressBar()
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials!")

#     elif option == "Register":
#         st.title("User Registration")
#         reg_username = st.text_input("Choose a Username", key="reg_username")
#         reg_password = st.text_input("Choose a Password", type="password", key="reg_password")
#         reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
#         if st.button("Register"):
#             if reg_password != reg_password_confirm:
#                 st.error("Passwords do not match!")
#             else:
#                 success, message = register_user(reg_username, reg_password)
#                 if success:
#                     st.success(message)
#                     st.session_state.logged_in = True
#                     st.session_state.username = reg_username
#                     st.session_state.userId = reg_username
#                     showProgressBar()
#                     st.rerun()
#                 else:
#                     st.error(message)
#     elif option == "Forgot Password":
#         st.title("Forgot Password")
#         username = st.text_input("Enter your username")
#         new_password = st.text_input("Enter new password", type="password")
#         new_password_confirm = st.text_input("Confirm new password", type="password")
#         if st.button("Reset Password"):
#             if new_password != new_password_confirm:
#                 st.error("Passwords do not match!")
#             else:
#                 success = change_password(username, new_password)
#                 if success:
#                     st.success("Password has been reset successfully.")
#                 else:
#                     st.error("Failed to reset password.")
    

# # If the user is logged in, show the main page content
# if st.session_state.logged_in:
#     st.title("Group 4 Dengue Tracker")
#     st.write(f"Welcome, {st.session_state.username}!")

#     from pages.reportMap import displayMap
#     from map import render_map  # map.py contains the map rendering function
#     render_map()
#     displayMap()
#     # Navigation buttons for Logout, Settings, Reporting, and Weather toggle
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         if st.button("Logout"):
#             st.session_state.logged_in = False
#             st.rerun()
#     with col2:
#         if st.button("Settings"):
#             st.switch_page("pages/settings.py")
#     with col3:
#         if st.button("Reporting"):
#             st.switch_page("pages/report.py")
#     # with col4:
#     #     # Toggle the weather display on/off
#     #     if st.button("Weather"):
#     #         st.session_state["show_weather"] = not st.session_state["show_weather"]

#     # Display the weather forecast inline if toggled on
# #     if st.session_state.get("show_weather"):
# #         show_weather()

# with st.sidebar:
#     if st.session_state.latitude and st.session_state.longitude:
#         show_weather(float(st.session_state.latitude), float(st.session_state.longitude))
#     else:
#         st.write("Fetching location...")

import streamlit as st

st.set_page_config(layout="wide") #must be the first 

from database import *
from widgets.progressbar import showProgressBar
from weather import show_weather  # Import the weather display function
import time
from streamlit_js_eval import (
    get_geolocation,
    get_user_agent,
    get_browser_language,
    get_page_location,
    copy_to_clipboard,
    create_share_link,
)
from pages.report import reporting_page
from pages.settings import settings_page

# Inject custom CSS
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# local_css("styles.css")

# Initialize the database (creates the DB file and table if they don't exist)
init_db()

# Initialize session state for login status and weather toggle
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_weather" not in st.session_state:
    st.session_state["show_weather"] = False
if "latitude" not in st.session_state:
    st.session_state.latitude = None
if "longitude" not in st.session_state:
    st.session_state.longitude = None

if st.session_state.latitude is None or st.session_state.longitude is None:
    loc = get_geolocation(component_key="geoloc")
    if loc:
        # Assuming that your frontend returns a JSON object with nested 'coords' information
        st.session_state.latitude = loc['coords']['latitude']
        st.session_state.longitude = loc['coords']['longitude']
        st.write(f"Retrieved geolocation: {loc}")
    else:
        st.write("Unable to automatically fetch geolocation.")

# If user is not logged in, show login/registration forms
if not st.session_state.logged_in:
    st.title("User Login / Registration")
    option = st.radio("Select an option", ["Login", "Register", "Forgot Password"])

    if option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user is not None:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.userId = user[0]
                st.success("Logged in!")
                showProgressBar()
                st.rerun()
            else:
                st.error("Invalid credentials!")

    elif option == "Register":
        st.title("User Registration")
        reg_username = st.text_input("Choose a Username", key="reg_username")
        reg_password = st.text_input("Choose a Password", type="password", key="reg_password")
        reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
        if st.button("Register"):
            if reg_password != reg_password_confirm:
                st.error("Passwords do not match!")
            else:
                success, message = register_user(reg_username, reg_password)
                if success:
                    st.success(message)
                    st.session_state.logged_in = True
                    st.session_state.username = reg_username
                    st.session_state.userId = reg_username
                    showProgressBar()
                    st.rerun()
                else:
                    st.error(message)
    # elif option == "Forgot Password":
    #     st.title("Forgot Password")
    #     username = st.text_input("Enter your username")
    #     new_password = st.text_input("Enter new password", type="password")
    #     new_password_confirm = st.text_input("Confirm new password", type="password")
    #     if st.button("Reset Password"):
    #         if new_password != new_password_confirm:
    #             st.error("Passwords do not match!")
    #         else:
    #             success = change_password(username, new_password)
    #             if success:
    #                 st.success("Password has been reset successfully.")
    #             else:
    #                 st.error("Failed to reset password.")
    elif option == "Forgot Password":
        st.title("Forgot Password")
        username = st.text_input("Enter your username")
        new_password = st.text_input("Enter new password", type="password")
        new_password_confirm = st.text_input("Confirm new password", type="password")
        if st.button("Reset Password"):
            if not username:
                st.error("Please enter your username.")
            elif not new_password:
                st.error("Please enter a new password.")
            elif new_password != new_password_confirm:
                st.error("Passwords do not match!")
            else:
                success = change_password(username, new_password)
                if success:
                    st.success("Password has been reset successfully.")
                else:
                    st.error("New password must be different from the current password.")

# If the user is logged in, show the main page content with tabs
if st.session_state.logged_in:
    st.title("Group 4 Dengue Tracker")
    st.write(f"Welcome, {st.session_state.username}!")
    # Logout button outside the tabs
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    # Create tabs for navigation
    tab_map, tab_settings, tab_reporting = st.tabs(["Map", "Settings", "Reporting"])
    
    with tab_map:
        st.header("Map")
        # Render the map content
        from map import render_map  # map.py contains the map rendering function
        from pages.reportMap import displayMap
        from combinedmap import render_combined_map
        #render_map()
        #displayMap()
        render_combined_map()
    
    with tab_settings:
        st.header("Settings")
        settings_page()
    
    with tab_reporting:
        st.header("Reporting")
        reporting_page()
    


# Sidebar for weather forecast
with st.sidebar:
    if st.session_state.latitude and st.session_state.longitude:
        show_weather(float(st.session_state.latitude), float(st.session_state.longitude))
    else:
        st.write("Fetching location...")

