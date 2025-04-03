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
from report import reporting_page
from settings import settings_page
from combinedmap import render_combined_map
from admin import admin_panel, view_report_image
import glob

view_report_image() #for new tab to view image (admin)

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
        #st.write(f"Retrieved geolocation: {loc}")
    else:
        st.warning("Unable to automatically fetch geolocation. Please enable location on browser.")

# If user is not logged in, show login/registration forms
if not st.session_state.logged_in:
    st.title("User Login / Registration")
    option = st.radio("Select an option", ["Login", "Register", "Forgot Password"])

    if option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.userId = username  # or a fixed ID for admin
                st.session_state.is_admin = True
                st.success("Logged in as admin!")
                showProgressBar()
                st.rerun()
            else:
                user = login_user(username, password)
                if user is not None:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.userId = user[0]
                    st.session_state.is_admin = False
                    st.success("Logged in!")
                    showProgressBar()
                    st.rerun()
                else:
                    st.error("Invalid credentials!")

    elif option == "Register1":
        st.title("User Registration")
        reg_username = st.text_input("Choose a Username", key="reg_username")
        reg_password = st.text_input("Choose a Password", type="password", key="reg_password")
        reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
        if st.button("Register"):
            if reg_password != reg_password_confirm:
                st.error("Passwords do not match!")
            elif reg_password == "None":
                st.error("Enter a password!")
            elif reg_username == "None":
                st.error("Enter a username!")
            else:
                success, message = register_user(reg_username, reg_password)
                if success:
                    st.success(message)
                    st.session_state.logged_in = True
                    st.session_state.username = reg_username
                    st.session_state.userId = reg_username
                    st.session_state.is_admin = False
                    showProgressBar()
                    st.rerun()
                else:
                    st.error(message)

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
        st.session_state.is_admin = False
        st.rerun()
    
    # Create tabs for navigation
    if st.session_state.get("is_admin", True):
        tab_map, tab_settings, tab_reporting, tab_admin = st.tabs(["Map", "Settings", "Reporting", "Admin"])
    else:
        tab_map, tab_settings, tab_reporting = st.tabs(["Map", "Settings", "Reporting"])
    
    with tab_map:
        st.header("Map")
        if st.button("Refresh Map", key="refresh_map"):
            st.rerun()
        # Render the map content
        render_combined_map()
    
    with tab_settings:
        st.header("Settings")
        settings_page()
    
    with tab_reporting:
        st.header("Reporting")
        reporting_page()

    # Admin-only panel
    if st.session_state.get("is_admin", True):
        with tab_admin:
            admin_panel()
    


# Sidebar for weather forecast
with st.sidebar:
    if st.session_state.latitude and st.session_state.longitude:
        show_weather(float(st.session_state.latitude), float(st.session_state.longitude))
    else:
        st.write("Fetching location...")

