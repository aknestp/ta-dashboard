import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
from datetime import datetime
import pytz 

from ui import render_dashboard

# ==================================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==================================================
SERVER_URL = "https://ta-backend-production-f459.up.railway.app" 

st.set_page_config(
    page_title="Sistem Peringatan Dini Air",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# 2. AUTO REFRESH (Berjalan tiap detik)
# ==================================================
st_autorefresh(interval=1000, key="refresh")

# ==================================================
# 3. GET DATA BACKEND
# ==================================================
try:
    latest_data = requests.get(f"{SERVER_URL}/latest", timeout=5).json()
    chart_data = requests.get(f"{SERVER_URL}/chart", timeout=5).json()
    history_data = requests.get(f"{SERVER_URL}/history", timeout=5).json()
except Exception as e:
    st.error("🚨 Koneksi ke Backend terputus atau API sedang offline.")
    st.error(f"Error: {e}")
    st.stop()

# Validasi Data Kosong
if isinstance(chart_data, dict): chart_data = [chart_data]
elif not isinstance(chart_data, list): chart_data = []

if isinstance(history_data, dict): history_data = [history_data]
elif not isinstance(history_data, list): history_data = []


# ==================================================
# 4. CEK KONEKSI SENSOR LEBIH DULU (TIMEOUT LOGIC)
# ==================================================
sensor_status = "🔴 Offline"
is_sensor_online = False

try:
    if latest_data and "time" in latest_data and latest_data["time"] != "-":
        latest_time = pd.to_datetime(latest_data.get("time"))

        # Sinkronisasi dengan waktu server Flask (WIB)
        tz_wib = pytz.timezone('Asia/Jakarta')
        now_wib = datetime.now(tz_wib).replace(tzinfo=None)

        selisih = (now_wib - latest_time).total_seconds()

        # Jika alat mengirim data dalam 30 detik terakhir, berarti alat AKTIF
        if 0 <= selisih <= 30:
            sensor_status = "🟢 Online"
            is_sensor_online = True
except Exception as e:
    pass


# ==================================================
# 5. LOGIKA STATUS DISTRIBUSI AIR (REALTIME)
# ==================================================
status_ml = latest_data.get("status", 0)

# Jika alat mati/dicabut, TIDAK MUNGKIN air mengalir. Paksa jadi Tidak Mengalir.
if not is_sensor_online:
    status_text = "🔴 AIR TIDAK MENGALIR"
else:
    # Jika alat hidup, barulah percaya pada hasil Machine Learning di database
    if status_ml == 1:
        status_text = "🟢 AIR MENGALIR"
    else:
        status_text = "🔴 AIR TIDAK MENGALIR"


# ==================================================
# 6. RENDER UI
# ==================================================
render_dashboard(
    latest_data=latest_data,
    chart_data=chart_data,
    history_data=history_data,
    status_text=status_text,
    sensor_status=sensor_status,
    server_url=SERVER_URL
)
