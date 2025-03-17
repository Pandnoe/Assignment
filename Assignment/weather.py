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


