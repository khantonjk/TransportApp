import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime

# SL API Details
SL_DEPARTURES_API_URL = "https://transport.integration.sl.se/v1/sites/{siteId}/departures"


# Load station data from the uploaded file
@st.cache_data
def load_station_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    station_map = {station['name']: station['id'] for station in sorted(data, key=lambda x: x['name'])}
    return station_map


# Streamlit App
st.title("Stockholm Subway Departures")

# Load the station map
station_file_path = 'data/sites.json'  # Path to the uploaded file
station_map = load_station_data(station_file_path)
station_transport_type_path = 'data/site_transport_types.json'
station_types = load_station_data(station_transport_type_path)


# Sidebar - User Inputs
st.header("Station Selection")
transport_mode = st.selectbox("Transport Mode", options=["METROSTN", "BUSTERM", "Spårvagn", "Boat", "Train"], index=0)

# Filter stations based on transport mode
filtered_stations = [station["name"] for station in station_types if transport_mode in station["Transport"]]

# Show dropdown with filtered stations
station_name = st.selectbox("Select Station", options=filtered_stations, placeholder="Select a station")


# Helper function to fetch data
def fetch_departures(station_id):
    url = SL_DEPARTURES_API_URL.format(siteId=station_id)
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    return response.json()


# Main App Logic
station_id = station_map.get(station_name)
if not station_id:
    st.error("Invalid station selection. Please try again.")
else:
    data = fetch_departures(station_id)
    st.write(data)
