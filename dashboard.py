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

.stApp {
    background-color: #f1f5f9;
}

/* spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* title */
.main-title {
    font-size: 44px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #64748b;
    margin-bottom: 35px;
}

/* card */
.card {
    background: white;
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.07);
    margin-bottom: 20px;
    border: 1px solid #e2e8f0;
}

/* section title */
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #0f172a;
    margin-top: 10px;
    margin-bottom: 15px;
}

/* status */
.status-green {
    color: #16a34a;
    font-size: 38px;
    font-weight: bold;
}

.status-red {
    color: #dc2626;
    font-size: 38px;
    font-weight: bold;
}

/* info */
.info-title {
    color: #64748b;
    font-size: 15px;
    margin-bottom: 6px;
}

.big-info {
    color: #0f172a;
    font-size: 24px;
    font-weight: bold;
}

/* dataframe */
div[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* chart */
div[data-testid="stVegaLiteChart"] {
    background: white;
    border-radius: 20px;
    padding: 15px;
}

/* button */
.stButton > button {
    background-color: #dc2626;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background-color: #b91c1c;
    color: white;
}

/* footer */
.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 50px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# GET DATA
# ======================================
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
st.markdown("""
<div class='main-title'>
Sistem Peringatan Dini Kedatangan Air
</div>

<div class='subtitle'>
Monitoring distribusi air berbasis IoT dan Machine Learning
</div>
""", unsafe_allow_html=True)

# ======================================
# STATUS SECTION
# ======================================
col1, col2 = st.columns(2)

# ======================================
# STATUS CARD
# ======================================
with col1:

    st.markdown(
        f"""
        <div class='card'>

            <div class='{status_class}'>
                {status_text}
            </div>

            <br>

            <div class='info-title'>
                Status Sensor
            </div>

            <div class='big-info'>
                {sensor_status}
            </div>

            <br>

            <div class='info-title'>
                Waktu Deteksi
            </div>

            <div class='big-info'>
                {latest_data.get("time", "-")}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================
# INFO CARD
# ======================================
with col2:

    st.markdown(
        f"""
        <div class='card'>

            <div class='info-title'>
                Kedatangan Air Terakhir
            </div>

            <div class='big-info'>
                {latest_data.get("last_water_time", "-")}
            </div>

            <br><br>

            <div class='info-title'>
                Durasi Distribusi Terakhir
            </div>

            <div class='big-info'>
                {latest_data.get("duration", "-")}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================
# HISTORY TITLE
# ======================================
st.markdown("""
<div class='section-title'>
Riwayat Distribusi Air
</div>
""", unsafe_allow_html=True)

# ======================================
# HISTORY TABLE
# ======================================
if isinstance(history_data, dict):
    history_data = [history_data]

elif not isinstance(history_data, list):
    history_data = []

history_df = pd.DataFrame(history_data)

st.dataframe(
    history_df,
    use_container_width=True,
    height=300
)

# ======================================
# CHART TITLE
# ======================================
st.markdown("""
<div class='section-title'>
Grafik RMS Realtime
</div>
""", unsafe_allow_html=True)

# ======================================
# CHART DATA
# ======================================
if isinstance(chart_data, dict):
    chart_data = [chart_data]

elif not isinstance(chart_data, list):
    chart_data = []

chart_df = pd.DataFrame(chart_data)

# ======================================
# SHOW CHART
# ======================================
if (
    not chart_df.empty
    and "rms" in chart_df.columns
):

    st.line_chart(
        chart_df["rms"],
        height=350
    )

else:

    st.warning(
        "Data RMS belum tersedia"
    )

# ======================================
# OPERATOR BUTTON
# ======================================
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

if st.button(
    "⚠ Informasi Gangguan Distribusi"
):
    st.session_state.show_popup = True

# ======================================
# POPUP
# ======================================
if st.session_state.show_popup:

    @st.dialog("Konfirmasi Operator")
    def operator_popup():

        password = st.text_input(
            "Masukkan Password Operator",
            type="password"
        )

        st.warning(
            "Pesan yang akan dikirim:\n\nDistribusi air mengalami gangguan sementara"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Kirim Informasi",
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
Sistem Peringatan Dini Kedatangan Air Distribusi Berbasis IoT dan Machine Learning
</div>
""", unsafe_allow_html=True)
