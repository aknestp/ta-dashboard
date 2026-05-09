import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
from datetime import datetime

from ui import render_dashboard

# ==================================================
# CONFIG
# ==================================================
SERVER_URL = "https://ta-backend-production-f459.up.railway.app/"

st.set_page_config(
    page_title="Sistem Peringatan Dini Air",
    page_icon="💧",
    layout="wide"
)

# ==================================================
# AUTO REFRESH
# ==================================================
st_autorefresh(interval=15000, key="refresh")

# ==================================================
# GET DATA BACKEND
# ==================================================
try:

    latest_data = requests.get(
        f"{SERVER_URL}/latest",
        timeout=5
    ).json()

    chart_data = requests.get(
        f"{SERVER_URL}/chart",
        timeout=5
    ).json()

    history_data = requests.get(
        f"{SERVER_URL}/history",
        timeout=5
    ).json()

except Exception as e:

    st.error("Backend tidak dapat dihubungkan")
    st.error(e)
    st.stop()

# ==================================================
# VALIDASI DATA
# ==================================================
if isinstance(chart_data, dict):
    chart_data = [chart_data]

elif not isinstance(chart_data, list):
    chart_data = []

if isinstance(history_data, dict):
    history_data = [history_data]

elif not isinstance(history_data, list):
    history_data = []

# ==================================================
# STATUS
# ==================================================
status = latest_data.get("status", 0)

if status == 1:
    status_text = "🟢 AIR MENGALIR"
else:
    status_text = "🔴 AIR TIDAK MENGALIR"

# ==================================================
# SENSOR STATUS
# ==================================================
sensor_status = "🔴 Offline"

try:

    latest_time = pd.to_datetime(
        latest_data.get("time")
    )

    now = datetime.now()

    selisih = (
        now - latest_time
    ).total_seconds()

    if selisih < 30:
        sensor_status = "🟢 Online"

except:
    pass

# ==================================================
# RENDER UI
# ==================================================
render_dashboard(
    latest_data=latest_data,
    chart_data=chart_data,
    history_data=history_data,
    status_text=status_text,
    sensor_status=sensor_status,
    server_url=SERVER_URL
)
