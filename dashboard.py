# ======================================
# IMPORT
# ======================================
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import requests
from datetime import datetime

# ======================================
# CONFIG
# ======================================
SERVER_URL = "https://ta-backend-production-f459.up.railway.app/"

st.set_page_config(
    page_title="Sistem Peringatan Dini Air",
    page_icon="💧",
    layout="wide"
)

# ======================================
# AUTO REFRESH
# ======================================
st_autorefresh(interval=5000, key="refresh")

# ======================================
# CUSTOM CSS
# ======================================
st.markdown("""
<style>

.main {
    background-color: #f1f5f9;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.main-title {
    font-size: 34px;
    font-weight: bold;
    color: #1e293b;
}

.subtitle {
    color: #64748b;
    font-size: 16px;
    margin-top: 5px;
}

.status-title {
    color: #64748b;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 15px;
}

.status-green {
    color: #16a34a;
    font-size: 42px;
    font-weight: bold;
}

.status-red {
    color: #dc2626;
    font-size: 42px;
    font-weight: bold;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #1e293b;
}

.footer {
    text-align: center;
    color: #94a3b8;
    padding-top: 30px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# GET DATA FROM BACKEND
# ======================================
try:

    latest_response = requests.get(
        f"{SERVER_URL}/latest",
        timeout=5
    )

    latest_data = latest_response.json()

    chart_response = requests.get(
        f"{SERVER_URL}/chart",
        timeout=5
    )

    chart_data = chart_response.json()

    history_response = requests.get(
        f"{SERVER_URL}/history",
        timeout=5
    )

    history_data = history_response.json()

except Exception as e:

    st.error("Backend tidak dapat dihubungkan")
    st.error(e)
    st.stop()

# ======================================
# STATUS AIR
# ======================================
status = latest_data.get("status", 0)

if status == 1:
    status_text = "🟢 AIR MENGALIR"
    status_class = "status-green"
else:
    status_text = "🔴 AIR TIDAK MENGALIR"
    status_class = "status-red"

# ======================================
# STATUS SENSOR
# ======================================
sensor_status = "🔴 Offline"

try:

    latest_time = pd.to_datetime(
        latest_data.get("time")
    )

    now = datetime.now()

    selisih = (now - latest_time).total_seconds()

    if selisih < 30:
        sensor_status = "🟢 Online"
    else:
        sensor_status = "🔴 Offline"

except:
    sensor_status = "🔴 Offline"

# ======================================
# HEADER
# ======================================
st.markdown(f"""
<div class='card'>

    <div class='main-title'>
        Sistem Peringatan Dini Kedatangan Air
    </div>

    <div class='subtitle'>
        Informasi kedatangan air distribusi berbasis IoT dan Machine Learning
    </div>

</div>
""", unsafe_allow_html=True)

# ======================================
# STATUS SECTION
# ======================================
col1, col2 = st.columns(2)

# ======================================
# STATUS DISTRIBUSI
# ======================================
with col1:

    st.markdown(f"""
    <div class='card'>

        <div class='status-title'>
            STATUS DISTRIBUSI
        </div>

        <div class='{status_class}'>
            {status_text}
        </div>

        <br>

        <p>
            <b>Hari:</b>
            {datetime.now().strftime('%A')}
        </p>

        <p>
            <b>Waktu Deteksi:</b>
            {latest_data.get('time', '-')}
        </p>

        <p>
            <b>Status Sensor:</b>
            {sensor_status}
        </p>

    </div>
    """, unsafe_allow_html=True)

# ======================================
# INFORMASI TERAKHIR
# ======================================
with col2:

    st.markdown(f"""
    <div class='card'>

        <div class='status-title'>
            INFORMASI TERAKHIR
        </div>

        <div style='background-color:#f8fafc;
                    padding:15px;
                    border-radius:15px;
                    margin-bottom:15px;
                    border:1px solid #e2e8f0;'>

            <b>Kedatangan Air Terakhir</b>
            <br>

            {latest_data.get('last_water_time', '-')}

        </div>

        <div style='background-color:#f8fafc;
                    padding:15px;
                    border-radius:15px;
                    border:1px solid #e2e8f0;'>

            <b>Durasi Distribusi Terakhir</b>
            <br>

            {latest_data.get('duration', '-')}

        </div>

    </div>
    """, unsafe_allow_html=True)

# ======================================
# HISTORY TABLE
# ======================================
st.markdown("""
<div class='card'>

    <div class='section-title'>
        Riwayat Distribusi Air
    </div>

    <div class='subtitle'>
        Riwayat kedatangan air distribusi
    </div>

</div>
""", unsafe_allow_html=True)

if isinstance(history_data, dict):
    history_data = [history_data]

history_df = pd.DataFrame(history_data)

st.dataframe(
    history_df,
    use_container_width=True
)

# ======================================
# REALTIME CHART
# ======================================
st.markdown("""
<div class='card'>

    <div class='section-title'>
        Grafik Distribusi Air
    </div>

    <div class='subtitle'>
        Visualisasi perubahan RMS secara realtime
    </div>

</div>
""", unsafe_allow_html=True)

chart_df = pd.DataFrame(chart_data)

if "rms" in chart_df.columns:

    st.line_chart(
        chart_df["rms"]
    )

else:
    st.warning("Data RMS belum tersedia")

# ======================================
# BUTTON OPERATOR
# ======================================
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

if st.button("⚠ Informasi Gangguan Distribusi"):
    st.session_state.show_popup = True

# ======================================
# POPUP
# ======================================
if st.session_state.show_popup:

    @st.dialog("Konfirmasi Operator")
    def operator_popup():

        password = st.text_input(
            "Masukkan Password Operator",
            type="password",
            key="operator_password"
        )

        st.warning(
            "Pesan yang akan dikirim: Distribusi air mengalami gangguan sementara"
        )

        col1, col2 = st.columns(2)

        # ======================================
        # BUTTON KIRIM
        # ======================================
        with col1:

            if st.button(
                "Kirim",
                use_container_width=True
            ):

                if password == "admin123":

                    try:

                        response = requests.post(
                            f"{SERVER_URL}/send_warning",
                            json={
                                "message":
                                "Distribusi air mengalami gangguan sementara"
                            },
                            timeout=5
                        )

                        if response.status_code == 200:

                            st.success(
                                "Informasi gangguan berhasil dikirim"
                            )

                            st.session_state.show_popup = False

                        else:

                            st.error(
                                "Gagal mengirim informasi"
                            )

                    except Exception as e:

                        st.error(e)

                else:

                    st.error(
                        "Password operator salah"
                    )

        # ======================================
        # BUTTON BATAL
        # ======================================
        with col2:

            if st.button(
                "Batal",
                use_container_width=True
            ):

                st.session_state.show_popup = False

    operator_popup()

# ======================================
# FOOTER
# ======================================
st.markdown("""
<div class='footer'>

Sistem Peringatan Dini Kedatangan Air Distribusi
Berbasis IoT Menggunakan Machine Learning

</div>
""", unsafe_allow_html=True)
