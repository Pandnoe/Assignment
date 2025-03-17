import streamlit as st
from database import addDengueReport, update_report_image
from widgets.progressbar import showProgressBar
import requests
from pathlib import Path
from PIL import Image
from datetime import datetime



API_KEY = "34291f9fc3344a6191554051bf74139b" # If can't work can get your own API key from geoapify
# Function to convert postcode into coordinates, returns list with 2 elements of latitude followed by longitude
def convertToLatLon(postal):
    url = f"https://api.geoapify.com/v1/geocode/search?text={postal}&lang=en&limit=1&type=postcode&format=json&apiKey=34291f9fc3344a6191554051bf74139b"
    response = requests.get(url)
    data = response.json()
    lat = data["results"][0]["lat"]
    lon = data["results"][0]["lon"]
    return [lat, lon]

def reporting_page():
    report_type = st.radio("Select type of reporting", ["Report person", "Report Location"], key="report_type_radio")

    if report_type == "Report person":
        form = st.form("Report person", clear_on_submit=True)
        postal_code = form.text_input("Postal code")
        symptom = form.selectbox("Select Symptom", ["Fever", "Headache", "Muscle pain", "Rash", "Nausea"])
        severity = form.selectbox("Select Severity", ["Mild", "Moderate", "Severe"])
        submitted = form.form_submit_button("Submit")
        
        if submitted:
            if postal_code:
                coordinates = convertToLatLon(postal_code)
                # Pass symptom and severity; hotspot_type left as default (empty)
                report_id = addDengueReport(
                    st.session_state.userId,
                    st.session_state.username,
                    report_type,
                    coordinates[0],
                    coordinates[1],
                    symptom,
                    severity
                )
                showProgressBar()
                st.success("Report submitted")
            else:
                st.error("Please enter a postal code")
                
    elif report_type == "Report Location":
        form = st.form("Report Location", clear_on_submit=True)
        postal_code = form.text_input("Postal code")
        hotspot_type = form.selectbox("Select Hotspot Type", [
            "Potted Plants", 
            "Construction Site", 
            "Drains", 
            "Discarded Containers", 
            "Gutters", 
            "Public Parks", 
            "Residential Areas", 
            "Others"
        ])
        picture = form.file_uploader("Upload Image of area", type=["jpg", "jpeg", "png"])
        submitted = form.form_submit_button("Submit")
        
        if submitted:
            if postal_code:
                coordinates = convertToLatLon(postal_code)
                # Pass hotspot_type; symptom and severity will remain empty
                report_id = addDengueReport(
                    st.session_state.userId,
                    st.session_state.username,
                    report_type,
                    coordinates[0],
                    coordinates[1],
                    hotspot_type=hotspot_type
                )
                if picture:
                    image_filename = save_image(picture, st.session_state.username, report_id)
                    update_report_image(report_id, image_filename)
                showProgressBar()
                st.success("Report submitted")
            else:
                st.error("Please enter a postal code")

def save_image(picture, username, report_id):
    curr_dir = Path.cwd()
    folder_dir = curr_dir / "images"
    folder_dir.mkdir(exist_ok=True)  # Ensure the folder exists
    file_type = picture.name.split('.')[-1]
    # Use report_id in the filename to make it unique per report.
    img_filename = f"{username}_{report_id}.{file_type}"
    img_loc = folder_dir / img_filename
    image = Image.open(picture)
    image.save(img_loc)
    return img_filename
