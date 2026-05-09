import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh
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
# CUSTOM CSS
# ======================================
st.markdown(
    """
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

    .info-box {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        border: 1px solid #e2e8f0;
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
    """,
    unsafe_allow_html=True
)

# ======================================
# AMBIL DATA DARI SERVER
# ======================================
try:
    latest_response = requests.get(f"{SERVER_URL}/latest", timeout=5)
    latest_data = latest_response.json()

    chart_response = requests.get(f"{SERVER_URL}/chart", timeout=5)
    chart_data = chart_response.json()

    history_response = requests.get(f"{SERVER_URL}/history", timeout=5)
    history_data = history_response.json()

except Exception as e:
    st.error("Gagal terhubung ke server")
    st.stop()

# ======================================
# STATUS DISTRIBUSI
# ======================================
status = latest_data.get("status", 0)

if status == 1:
    status_text = "🟢 AIR MENGALIR"
    status_class = "status-green"
else:
    status_text = "🔴 AIR TIDAK MENGALIR"
    status_class = "status-red"

# ======================================
# HEADER
# ======================================
st.markdown(
    """
    <div class='card'>
        <div class='main-title'>
            Sistem Peringatan Dini Kedatangan Air
        </div>
        <div class='subtitle'>
            Informasi kedatangan air distribusi berbasis IoT dan Machine Learning
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================
# STATUS SECTION
# ======================================
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class='card'>
            <div class='status-title'>STATUS DISTRIBUSI</div>
            <div class='{status_class}'>{status_text}</div>
            <br>
            <p><b>Hari:</b> {datetime.now().strftime('%A')}</p>
            <p><b>Waktu Deteksi:</b> {latest_data.get('time', '-')} WIB</p>
            <p><b>Status Sensor:</b> Online</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class='card'>
            <div class='status-title'>INFORMASI TERAKHIR</div>

            <div class='info-box'>
                <b>Kedatangan Air Terakhir</b><br>
                {latest_data.get('last_water_time', '-')}
            </div>

            <div class='info-box'>
                <b>Durasi Distribusi Terakhir</b><br>
                {latest_data.get('duration', '-')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================
# HISTORY TABLE
# ======================================
st.markdown(
    """
    <div class='card'>
        <div class='section-title'>Riwayat Distribusi Air</div>
        <div class='subtitle'>Riwayat kedatangan air distribusi</div>
    </div>
    """,
    unsafe_allow_html=True
)

history_df = pd.DataFrame(history_data)
st.dataframe(history_df, use_container_width=True)

# ======================================
# REALTIME CHART
# ======================================
st.markdown(
    """
    <div class='card'>
        <div class='section-title'>Grafik Distribusi Air</div>
        <div class='subtitle'>Visualisasi perubahan RMS secara realtime</div>
    </div>
    """,
    unsafe_allow_html=True
)

chart_df = pd.DataFrame(chart_data)

if 'rms' in chart_df.columns:
    st.line_chart(chart_df['rms'])
else:
    st.warning("Data RMS belum tersedia")

# ======================================
# TOMBOL OPERATOR
# ======================================

# Simpan state popup
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

# Klik tombol buka popup
if st.button("⚠ Informasi Gangguan Distribusi"):
    st.session_state.show_popup = True

# Popup operator
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

        with col1:
            if st.button("Kirim", use_container_width=True):

                if password == "admin123":

                    try:
                        response = requests.post(
                            f"{SERVER_URL}/send_warning",
                            json={
                                "message": "Distribusi air mengalami gangguan sementara"
                            },
                            timeout=5
                        )

                        if response.status_code == 200:
                            st.success("Informasi gangguan berhasil dikirim")
                            st.session_state.show_popup = False
                        else:
                            st.error("Gagal mengirim informasi")

                    except Exception as e:
                        st.error(f"Error: {e}")

                else:
                    st.error("Password operator salah")

        with col2:
            if st.button("Batal", use_container_width=True):
                st.session_state.show_popup = False

    operator_popup()

# ======================================
# FOOTER
# ======================================
st.markdown(
    """
    <div class='footer'>
        Sistem Peringatan Dini Kedatangan Air Distribusi Berbasis IoT Menggunakan Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================
# AUTO REFRESH
# ======================================
# Auto refresh setiap 5 detik
st_autorefresh(interval=5000, key="refresh")
