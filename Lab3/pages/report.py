import streamlit as st
from database import addDengueReport
from widgets.progressbar import showProgressBar
import requests
import json


option = st.radio("Select type of reporting", ["Report person", "Report case"])

API_KEY = "34291f9fc3344a6191554051bf74139b" # If can't work can get your own API key from geoapify
# Function to convert postcode into coordinates, returns list with 2 elements of latitude followed by longitude
def convertToLatLon(postal):
    url = f"https://api.geoapify.com/v1/geocode/search?text={postal}&lang=en&limit=1&type=postcode&format=json&apiKey=34291f9fc3344a6191554051bf74139b"
    response = requests.get(url)
    data = response.json()
    lat = data["results"][0]["lat"]
    lon = data["results"][0]["lon"]
    return [lat, lon]


# if option == "Report person":
#     form = st.form("Report person", clear_on_submit=True)
#     location = form.text_input("Postal code")
#     details = form.text_area("Details")
#     submitted = form.form_submit_button("Submit")
#     if submitted:
#         if location and details:
#             coordinates = convertToLatLon(location) # Element 0 is latitude, element 1 is longitude
#             addDengueReport(st.session_state.userId, details, option, coordinates[0], coordinates[1])
#             showProgressBar()
#         st.toast("Submitted")
# elif option == "Report case":
#     form = st.form("Report case", clear_on_submit=True)
#     location = form.text_input("Postal code")
#     details = form.text_area("Details")
#     submitted = form.form_submit_button("Submit")
#     if submitted:
#         if location and details:
#             coordinates = convertToLatLon(location) # Element 0 is latitude, element 1 is longitude
#             addDengueReport(st.session_state.userId, details, option, coordinates[0], coordinates[1])
#             showProgressBar()
#         st.toast("Submitted")
# if st.button("Return to home"):
#     st.switch_page("main.py")

def reporting_page():
    option_report = st.radio("Select type of reporting", ["Report person", "Report case"])
    
    if option_report == "Report person":
        form = st.form("Report person", clear_on_submit=True)
        location = form.text_input("Postal code")
        details = form.text_area("Details")
        submitted = form.form_submit_button("Submit")
        if submitted:
            if location and details:
                coordinates = convertToLatLon(location)  # Element 0 is latitude, element 1 is longitude
                addDengueReport(st.session_state.userId, details, option_report, coordinates[0], coordinates[1])
                showProgressBar()
                st.toast("Submitted")
    elif option_report == "Report case":
        form = st.form("Report case", clear_on_submit=True)
        location = form.text_input("Postal code")
        details = form.text_area("Details")
        submitted = form.form_submit_button("Submit")
        if submitted:
            if location and details:
                coordinates = convertToLatLon(location)  # Element 0 is latitude, element 1 is longitude
                addDengueReport(st.session_state.userId, details, option_report, coordinates[0], coordinates[1])
                showProgressBar()
                st.toast("Submitted")




