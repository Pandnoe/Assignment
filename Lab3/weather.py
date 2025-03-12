# import streamlit as st
# import requests

# # Inject custom CSS for a dark theme and refined card layout
# st.markdown("""
# <style>
# body {
#     background-color: #1e1e1e;
#     color: #e0e0e0;
# }
# .card {
#     background-color: #2c2c2c;
#     padding: 20px;
#     border-radius: 10px;
#     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
#     margin-bottom: 20px;
# }
# .card h3, .card h4 {
#     color: #f0f0f0;
#     margin-bottom: 10px;
# }
# .card p {
#     color: #d0d0d0;
#     font-size: 16px;
#     margin: 5px 0;
# }
# hr {
#     border: 0;
#     height: 1px;
#     background: #444;
#     margin: 20px 0;
# }
# </style>
# """, unsafe_allow_html=True)

# @st.cache_data(ttl=600)
# def get_weather_data():
#     """
#     Fetches the 24-hour weather forecast from Data.gov.sg and returns the JSON data.
#     """
#     url = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# def show_weather():
#     """
#     Fetches and displays the weather forecast using a dark-themed, dashboard-style layout.
#     """
#     data = get_weather_data()
    
#     st.markdown("<h2 style='text-align: center; color: #4CAF50;'>24-Hour Weather Forecast</h2>", unsafe_allow_html=True)
    
#     # Uncomment below to display raw JSON for debugging purposes
#     # st.json(data)
    
#     if "items" in data:
#         items = data["items"]
#         if items:
#             record = items[0]
#             general = record.get("general", {})
#             valid_period = record.get("valid_period", {})

#             # General Forecast Card
#             st.markdown("<div class='card'>", unsafe_allow_html=True)
#             st.markdown("<h3>General Forecast</h3>", unsafe_allow_html=True)
#             st.markdown(f"<p><strong>Forecast:</strong> {general.get('forecast', 'N/A')}</p>", unsafe_allow_html=True)
            
#             temperature = general.get("temperature", {})
#             st.markdown(
#                 f"<p><strong>Temperature:</strong> {temperature.get('low', 'N/A')}°C - {temperature.get('high', 'N/A')}°C</p>",
#                 unsafe_allow_html=True
#             )
            
#             humidity = general.get("relative_humidity", {})
#             st.markdown(
#                 f"<p><strong>Relative Humidity:</strong> {humidity.get('low', 'N/A')}% - {humidity.get('high', 'N/A')}%</p>",
#                 unsafe_allow_html=True
#             )
            
#             wind = general.get("wind", {})
#             wind_speed = wind.get("speed", {})
#             st.markdown(
#                 f"<p><strong>Wind Speed:</strong> {wind_speed.get('low', 'N/A')} km/h - {wind_speed.get('high', 'N/A')} km/h</p>",
#                 unsafe_allow_html=True
#             )
#             st.markdown(f"<p><strong>Wind Direction:</strong> {wind.get('direction', 'N/A')}</p>", unsafe_allow_html=True)
            
#             st.markdown(
#                 f"<p><strong>Valid Period:</strong> {valid_period.get('start', 'N/A')} to {valid_period.get('end', 'N/A')}</p>",
#                 unsafe_allow_html=True
#             )
#             st.markdown("</div>", unsafe_allow_html=True)
            
#             st.markdown("<hr>", unsafe_allow_html=True)
            
#             # Detailed Forecast Cards
#             periods = record.get("periods", [])
#             if periods:
#                 st.markdown("<h3 style='color:#f0f0f0;'>Detailed Forecasts</h3>", unsafe_allow_html=True)
#                 for idx, period in enumerate(periods):
#                     time_period = period.get("time", {})
#                     start_time = time_period.get("start", "N/A")
#                     end_time = time_period.get("end", "N/A")
                    
#                     st.markdown("<div class='card'>", unsafe_allow_html=True)
#                     st.markdown(f"<h4>Period {idx+1}</h4>", unsafe_allow_html=True)
#                     st.markdown(f"<p><strong>Time:</strong> {start_time} to {end_time}</p>", unsafe_allow_html=True)
                    
#                     regions = period.get("regions", {})
#                     if regions:
#                         cols = st.columns(len(regions))
#                         for col, (region, description) in zip(cols, regions.items()):
#                             col.markdown(f"<p><strong>{region.title()}:</strong> {description}</p>", unsafe_allow_html=True)
#                     st.markdown("</div>", unsafe_allow_html=True)
#             else:
#                 st.error("No detailed period forecast data available.")
#         else:
#             st.error("No items available in forecast data.")
#     else:
#         st.error("No forecast data available.")


# import streamlit as st
# import requests

# # Inject custom CSS for a dark theme and refined card layout
# st.markdown("""
# <style>
# body {
#     background-color: #1e1e1e;
#     color: #e0e0e0;
# }
# .card {
#     background-color: #2c2c2c;
#     padding: 20px;
#     border-radius: 10px;
#     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
#     margin-bottom: 20px;
# }
# .card h3, .card h4 {
#     color: #f0f0f0;
#     margin-bottom: 10px;
# }
# .card p {
#     color: #d0d0d0;
#     font-size: 16px;
#     margin: 5px 0;
# }
# hr {
#     border: 0;
#     height: 1px;
#     background: #444;
#     margin: 20px 0;
# }
# </style>
# """, unsafe_allow_html=True)

# @st.cache_data(ttl=600)
# def get_weather_data():
#     """
#     Fetches the 24-hour weather forecast from Data.gov.sg and returns the JSON data.
#     """
#     url = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# def show_weather(lat, lon):
#     """
#     Fetches and displays the weather forecast using a dark-themed, dashboard-style layout.
#     """
#     data = get_weather_data()
    
#     st.markdown("<h2 style='text-align: center; color: #4CAF50;'>24-Hour Weather Forecast</h2>", unsafe_allow_html=True)
    
#     # Uncomment below to display raw JSON for debugging purposes
#     # st.json(data)
    
#     if "items" in data:
#         items = data["items"]
#         if items:
#             record = items[0]
#             general = record.get("general", {})
#             valid_period = record.get("valid_period", {})

#             # General Forecast Card
#             st.markdown("<div class='card'>", unsafe_allow_html=True)
#             st.markdown("<h3>General Forecast</h3>", unsafe_allow_html=True)
#             st.markdown(f"<p><strong>Forecast:</strong> {general.get('forecast', 'N/A')}</p>", unsafe_allow_html=True)
            
#             temperature = general.get("temperature", {})
#             st.markdown(
#                 f"<p><strong>Temperature:</strong> {temperature.get('low', 'N/A')}°C - {temperature.get('high', 'N/A')}°C</p>",
#                 unsafe_allow_html=True
#             )
            
#             humidity = general.get("relative_humidity", {})
#             st.markdown(
#                 f"<p><strong>Relative Humidity:</strong> {humidity.get('low', 'N/A')}% - {humidity.get('high', 'N/A')}%</p>",
#                 unsafe_allow_html=True
#             )
            
#             wind = general.get("wind", {})
#             wind_speed = wind.get("speed", {})
#             st.markdown(
#                 f"<p><strong>Wind Speed:</strong> {wind_speed.get('low', 'N/A')} km/h - {wind_speed.get('high', 'N/A')} km/h</p>",
#                 unsafe_allow_html=True
#             )
#             st.markdown(f"<p><strong>Wind Direction:</strong> {wind.get('direction', 'N/A')}</p>", unsafe_allow_html=True)
            
#             st.markdown(
#                 f"<p><strong>Valid Period:</strong> {valid_period.get('start', 'N/A')} to {valid_period.get('end', 'N/A')}</p>",
#                 unsafe_allow_html=True
#             )
#             st.markdown("</div>", unsafe_allow_html=True)
            
#             st.markdown("<hr>", unsafe_allow_html=True)
            
#             # Detailed Forecast Cards
#             periods = record.get("periods", [])
#             if periods:
#                 st.markdown("<h3 style='color:#f0f0f0;'>Detailed Forecasts</h3>", unsafe_allow_html=True)
#                 for idx, period in enumerate(periods):
#                     time_period = period.get("time", {})
#                     start_time = time_period.get("start", "N/A")
#                     end_time = time_period.get("end", "N/A")
                    
#                     st.markdown("<div class='card'>", unsafe_allow_html=True)
#                     st.markdown(f"<h4>Period {idx+1}</h4>", unsafe_allow_html=True)
#                     st.markdown(f"<p><strong>Time:</strong> {start_time} to {end_time}</p>", unsafe_allow_html=True)
                    
#                     regions = period.get("regions", {})
#                     if regions:
#                         cols = st.columns(len(regions))
#                         for col, (region, description) in zip(cols, regions.items()):
#                             if region.lower() == "ne":
#                                 col.markdown(f"<p><strong>{region.title()}:</strong> {description}</p>", unsafe_allow_html=True)
#                     st.markdown("</div>", unsafe_allow_html=True)

                    
#             else:
#                 st.error("No detailed period forecast data available.")
#         else:
#             st.error("No items available in forecast data.")
#     else:
#         st.error("No forecast data available.")

###############################################

# import streamlit as st
# import requests

# # Inject custom CSS for a dark theme and refined card layout
# st.markdown("""
# <style>
# body {
#     background-color: #1e1e1e;
#     color: #e0e0e0;
# }
# .card {
#     background-color: #2c2c2c;
#     padding: 20px;
#     border-radius: 10px;
#     box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
#     margin-bottom: 20px;
# }
# .card h3, .card h4 {
#     color: #f0f0f0;
#     margin-bottom: 10px;
# }
# .card p {
#     color: #d0d0d0;
#     font-size: 16px;
#     margin: 5px 0;
# }
# hr {
#     border: 0;
#     height: 1px;
#     background: #444;
#     margin: 20px 0;
# }
# </style>
# """, unsafe_allow_html=True)

# @st.cache_data(ttl=600)
# def get_weather_data():
#     """
#     Fetches the 24-hour weather forecast from Data.gov.sg and returns the JSON data.
#     """
#     url = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# def show_weather(lat, lon):
#     """
#     Fetches and displays the weather forecast using a dark-themed, dashboard-style layout.
#     If rain is detected, it triggers a dengue prevention pop-up alert.
#     """
#     data = get_weather_data()
    
#     st.markdown("<h2 style='text-align: center; color: #4CAF50;'>24-Hour Weather Forecast</h2>", unsafe_allow_html=True)

#     if "items" in data and data["items"]:  # Ensure data exists
#         record = data["items"][0]
#         general = record.get("general", {})
#         valid_period = record.get("valid_period", {})

#         # ✅ Extract forecast description for rain detection
#         forecast_text = general.get("forecast", "No forecast available")

#         # General Forecast Card
#         st.markdown("<div class='card'>", unsafe_allow_html=True)
#         st.markdown("<h3>General Forecast</h3>", unsafe_allow_html=True)
#         st.markdown(f"<p><strong>Forecast:</strong> {forecast_text}</p>", unsafe_allow_html=True)

#         temperature = general.get("temperature", {})
#         st.markdown(
#             f"<p><strong>Temperature:</strong> {temperature.get('low', 'N/A')}°C - {temperature.get('high', 'N/A')}°C</p>",
#             unsafe_allow_html=True
#         )

#         humidity = general.get("relative_humidity", {})
#         st.markdown(
#             f"<p><strong>Relative Humidity:</strong> {humidity.get('low', 'N/A')}% - {humidity.get('high', 'N/A')}%</p>",
#             unsafe_allow_html=True
#         )

#         wind = general.get("wind", {})
#         wind_speed = wind.get("speed", {})
#         st.markdown(
#             f"<p><strong>Wind Speed:</strong> {wind_speed.get('low', 'N/A')} km/h - {wind_speed.get('high', 'N/A')} km/h</p>",
#             unsafe_allow_html=True
#         )
#         st.markdown(f"<p><strong>Wind Direction:</strong> {wind.get('direction', 'N/A')}</p>", unsafe_allow_html=True)

#         st.markdown(
#             f"<p><strong>Valid Period:</strong> {valid_period.get('start', 'N/A')} to {valid_period.get('end', 'N/A')}</p>",
#             unsafe_allow_html=True
#         )
#         st.markdown("</div>", unsafe_allow_html=True)

#         # ✅ Check for Rainy Weather and Show Dengue Prevention Alert
#         rain_keywords = ["rain", "showers", "thundery", "storm"]
#         if any(keyword in forecast_text.lower() for keyword in rain_keywords):

#             # ✅ Ensure the toast notification appears ONLY ONCE per session
#             if "dengue_alert_shown" not in st.session_state:
#                 st.toast("⚠️ **Rainy Weather Alert!** Take dengue prevention measures!", icon="⚠️")
#                 st.session_state.dengue_alert_shown = True  # ✅ Mark the alert as shown

#             # ✅ Dengue Prevention Checklist (Interactive)
#             st.warning("⚠️ **Rainy Weather Alert!** Take dengue prevention measures:")
        
#             # ✅ Maintain checkbox states using session_state
#             if "checkbox_state" not in st.session_state:
#                 st.session_state.checkbox_state = {
#                     "clear_water": False,
#                     "apply_repellent": False,
#                     "use_insecticide": False
#                 }
        
#             # ✅ Interactive checkboxes
#             clear_water = st.checkbox(
#                 "Clear stagnant water to prevent mosquito breeding.",
#                 value=st.session_state.checkbox_state["clear_water"],
#                 key="clear_water"
#             )
#             apply_repellent = st.checkbox(
#                 "Apply mosquito repellent.",
#                 value=st.session_state.checkbox_state["apply_repellent"],
#                 key="apply_repellent"
#             )
#             use_insecticide = st.checkbox(
#                 "Use insecticide where necessary.",
#                 value=st.session_state.checkbox_state["use_insecticide"],
#                 key="use_insecticide"
#             )

#             # ✅ Update session state without modifying after widget instantiation
#             st.session_state.checkbox_state["clear_water"] = clear_water
#             st.session_state.checkbox_state["apply_repellent"] = apply_repellent
#             st.session_state.checkbox_state["use_insecticide"] = use_insecticide

#             # ✅ Display success message when all are checked
#             if all(st.session_state.checkbox_state.values()):
#                 st.success("✅ You have completed all dengue prevention measures! Stay safe! 🦟")

#         # Detailed Forecast Cards
#         periods = record.get("periods", [])
#         if periods:
#             st.markdown("<h3 style='color:#f0f0f0;'>Detailed Forecasts</h3>", unsafe_allow_html=True)
#             for idx, period in enumerate(periods):
#                 time_period = period.get("time", {})
#                 start_time = time_period.get("start", "N/A")
#                 end_time = time_period.get("end", "N/A")

#                 st.markdown("<div class='card'>", unsafe_allow_html=True)
#                 st.markdown(f"<h4>Period {idx+1}</h4>", unsafe_allow_html=True)
#                 st.markdown(f"<p><strong>Time:</strong> {start_time} to {end_time}</p>", unsafe_allow_html=True)

#                 regions = period.get("regions", {})
#                 if regions:
#                     cols = st.columns(len(regions))
#                     for col, (region, description) in zip(cols, regions.items()):
#                         col.markdown(f"<p><strong>{region.title()}:</strong> {description}</p>", unsafe_allow_html=True)
#                 st.markdown("</div>", unsafe_allow_html=True)

#         else:
#             st.error("No detailed period forecast data available.")

#     else:
#         st.error("No forecast data available.")  # Error handling


import streamlit as st
import requests

# Minimal CSS for dark theme
st.markdown("""
<style>
body {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: sans-serif;
}
.card {
    background-color: #2c2c2c;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_weather_data():
    url = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def show_weather(lat, lon, show_alert=True):
    """
    Fetches and displays only the forecast text.
    If show_alert is True and the forecast indicates rain, triggers a dengue prevention alert.
    """
    data = get_weather_data()
    
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>24-Hour Weather Forecast</h2>", unsafe_allow_html=True)
    
    if "items" in data and data["items"]:
        record = data["items"][0]
        general = record.get("general", {})
        forecast_text = general.get("forecast", "No forecast available")
        
        # Display the forecast in a simple card
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>Forecast:</strong> {forecast_text}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Check for rainy conditions and display dengue alert if required and if show_alert is True
        rain_keywords = ["rain", "showers", "thundery", "storm"]
        if show_alert and any(keyword in forecast_text.lower() for keyword in rain_keywords):
            if "dengue_alert_shown" not in st.session_state:
                st.toast("⚠️ **Rainy Weather Alert!** Take dengue prevention measures!", icon="⚠️")
                st.session_state.dengue_alert_shown = True

            st.warning("⚠️ **Rainy Weather Alert!** Take dengue prevention measures:")

            if "checkbox_state" not in st.session_state:
                st.session_state.checkbox_state = {
                    "clear_water": False,
                    "apply_repellent": False,
                    "use_insecticide": False
                }
            
            clear_water = st.checkbox(
                "Clear stagnant water to prevent mosquito breeding.",
                value=st.session_state.checkbox_state["clear_water"],
                key="clear_water"
            )
            apply_repellent = st.checkbox(
                "Apply mosquito repellent.",
                value=st.session_state.checkbox_state["apply_repellent"],
                key="apply_repellent"
            )
            use_insecticide = st.checkbox(
                "Use insecticide where necessary.",
                value=st.session_state.checkbox_state["use_insecticide"],
                key="use_insecticide"
            )

            st.session_state.checkbox_state["clear_water"] = clear_water
            st.session_state.checkbox_state["apply_repellent"] = apply_repellent
            st.session_state.checkbox_state["use_insecticide"] = use_insecticide

            if all(st.session_state.checkbox_state.values()):
                st.success("✅ You have completed all dengue prevention measures! Stay safe! 🦟")

        else:
            st.info("No rain forecasted. You don't need to worry about dengue, but remain aware of any stagnant water spots where mosquitoes might breed. Stay safe! 🦟")
    else:
        st.error("No forecast data available.")

# # Main page: show forecast with dengue alert
# show_weather(0, 0, show_alert=True)

# # Sidebar: show forecast without dengue alert to avoid duplicate keys
# with st.sidebar:
#     show_weather(0, 0, show_alert=False)


