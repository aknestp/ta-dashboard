import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import requests
from datetime import datetime

SERVER_URL = "https://ta-backend-production-f459.up.railway.app/"

st.set_page_config(
    page_title="Sistem Peringatan Dini Air",
    layout="wide"
)

st_autorefresh(interval=10000, key="refresh")

# ======================================
# GET DATA
# ======================================
try:

    latest_data = requests.get(
        f"{SERVER_URL}/latest"
    ).json()

    chart_data = requests.get(
        f"{SERVER_URL}/chart"
    ).json()

    history_data = requests.get(
        f"{SERVER_URL}/history"
    ).json()

except Exception as e:

    st.error(e)
    st.stop()

# ======================================
# STATUS AIR
# ======================================
status = latest_data.get("status", 0)

if status == 1:
    status_text = "🟢 AIR MENGALIR"
else:
    status_text = "🔴 AIR TIDAK MENGALIR"

# ======================================
# STATUS SENSOR
# ======================================
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

# ======================================
# HEADER
# ======================================
st.title(
    "Sistem Peringatan Dini Kedatangan Air"
)

st.caption(
    "IoT dan Machine Learning"
)

# ======================================
# STATUS
# ======================================
col1, col2 = st.columns(2)

with col1:

    st.subheader(status_text)

    st.write(
        "Status Sensor:",
        sensor_status
    )

    st.write(
        "Waktu:",
        latest_data.get("time", "-")
    )

with col2:

    st.info(
        f"""
Kedatangan Air Terakhir:
{latest_data.get("last_water_time", "-")}
"""
    )

# ======================================
# HISTORY
# ======================================
st.subheader(
    "Riwayat Distribusi"
)

if isinstance(history_data, dict):
    history_data = [history_data]

history_df = pd.DataFrame(history_data)

st.dataframe(
    history_df,
    use_container_width=True
)

# ======================================
# CHART
# ======================================
st.subheader(
    "Grafik RMS Realtime"
)

if isinstance(chart_data, dict):
    chart_data = [chart_data]

elif not isinstance(chart_data, list):
    chart_data = []

chart_df = pd.DataFrame(chart_data)

if (
    not chart_df.empty
    and "rms" in chart_df.columns
):

    st.line_chart(
        chart_df["rms"]
    )

else:

    st.warning(
        "Data RMS belum tersedia"
    )

# ======================================
# POPUP OPERATOR
# ======================================
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

if st.button(
    "⚠ Informasi Gangguan Distribusi"
):
    st.session_state.show_popup = True

if st.session_state.show_popup:

    @st.dialog("Konfirmasi Operator")
    def operator_popup():

        password = st.text_input(
            "Password Operator",
            type="password"
        )

        if st.button("Kirim"):

            if password == "admin123":

                requests.post(
                    f"{SERVER_URL}/send_warning",
                    json={
                        "message":
                        "Distribusi air mengalami gangguan sementara"
                    }
                )

                st.success(
                    "Informasi berhasil dikirim"
                )

                st.session_state.show_popup = False

            else:

                st.error(
                    "Password salah"
                )

    operator_popup()
