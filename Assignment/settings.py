import streamlit as st
from database import change_password

def settings_page():
    new_password = st.text_input("New password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    
    if st.button("Change password"):
        username = st.session_state.username
        if not new_password:
            st.error("Please enter a new password.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        else:
            result = change_password(username, new_password)
            if result:
                st.success("Password changed successfully!")
            else:
                st.error("New password must be different from the current password.")

