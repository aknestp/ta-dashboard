import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import requests
from datetime import datetime

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
st_autorefresh(interval=30000, key="refresh")

# ==================================================
# CSS
# ==================================================
st.markdown("""
<style>

.stApp{
    background-color:#eef2f7;
}

/* Main Layout */
.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
    max-width:1200px;
}

/* Header */
.top-header{
    background:linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
    padding:35px;
    border-radius:25px;
    margin-bottom:25px;
    color:white;
    box-shadow:0 8px 25px rgba(0,0,0,0.12);
}

.top-title{
    font-size:42px;
    font-weight:800;
    margin-bottom:8px;
}

.top-subtitle{
    font-size:17px;
    color:#cbd5e1;
}

/* Section Title */
.section-title{
    font-size:34px;
    font-weight:800;
    color:#0f172a;
    margin-top:15px;
    margin-bottom:18px;
}

/* Card */
[data-testid="stVerticalBlockBorderWrapper"]{
    background:white;
    border-radius:22px;
    padding:10px;
    border:none;
    box-shadow:0 4px 18px rgba(0,0,0,0.06);
}

/* Metric */
[data-testid="stMetric"]{
    background:#f8fafc;
    padding:15px;
    border-radius:18px;
}

/* Dataframe */
div[data-testid="stDataFrame"]{
    border-radius:20px;
    overflow:hidden;
}

/* Chart */
div[data-testid="stVegaLiteChart"]{
    background:white;
    border-radius:20px;
    padding:10px;
}

/* Button */
.stButton > button{
    background:linear-gradient(
        135deg,
        #dc2626,
        #ef4444
    );
    color:white;
    border:none;
    border-radius:15px;
    padding:14px 24px;
    font-weight:bold;
    font-size:16px;
    width:100%;
    box-shadow:0 4px 12px rgba(239,68,68,0.3);
}

.stButton > button:hover{
    color:white;
}

/* Footer */
.footer{
    text-align:center;
    color:#94a3b8;
    margin-top:40px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# GET DATA
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
# HEADER
# ==================================================
st.markdown("""
<div class="top-header">

<div class="top-title">
💧 Sistem Peringatan Dini Kedatangan Air
</div>

<div class="top-subtitle">
Monitoring distribusi air berbasis IoT dan Machine Learning
</div>

</div>
""", unsafe_allow_html=True)

# ==================================================
# TOP SECTION
# ==================================================
col1, col2 = st.columns(2)

# ==================================================
# STATUS CARD
# ==================================================
with col1:

    with st.container(border=True):

        st.subheader(status_text)

        st.metric(
            "Status Sensor",
            sensor_status
        )

        st.metric(
            "Waktu Deteksi",
            latest_data.get(
                "time",
                "-"
            )
        )

# ==================================================
# INFO CARD
# ==================================================
with col2:

    with st.container(border=True):

        st.metric(
            "Kedatangan Air Terakhir",
            latest_data.get(
                "last_water_time",
                "-"
            )
        )

        st.metric(
            "Durasi Distribusi Terakhir",
            latest_data.get(
                "duration",
                "-"
            )
        )

# ==================================================
# HISTORY TITLE
# ==================================================
st.markdown("""
<div class="section-title">
Riwayat Distribusi Air
</div>
""", unsafe_allow_html=True)

# ==================================================
# HISTORY DATA
# ==================================================
if isinstance(history_data, dict):
    history_data = [history_data]

elif not isinstance(history_data, list):
    history_data = []

history_df = pd.DataFrame(history_data)

# ==================================================
# SHOW HISTORY
# ==================================================
if not history_df.empty:

    st.dataframe(
        history_df,
        use_container_width=True,
        height=300
    )

else:

    st.info(
        "Belum ada riwayat distribusi"
    )

# ==================================================
# CHART TITLE
# ==================================================
st.markdown("""
<div class="section-title">
Grafik RMS Realtime
</div>
""", unsafe_allow_html=True)

# ==================================================
# CHART DATA
# ==================================================
if isinstance(chart_data, dict):
    chart_data = [chart_data]

elif not isinstance(chart_data, list):
    chart_data = []

chart_df = pd.DataFrame(chart_data)

# ==================================================
# SHOW CHART
# ==================================================
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

# ==================================================
# BUTTON WARNING
# ==================================================
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False

if st.button(
    "⚠ Informasi Gangguan Distribusi"
):
    st.session_state.show_popup = True

# ==================================================
# POPUP
# ==================================================
if st.session_state.show_popup:

    @st.dialog("Konfirmasi Operator")
    def popup_operator():

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
                                "Informasi berhasil dikirim"
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
                        "Password salah"
                    )

        with col2:

            if st.button(
                "Batal",
                use_container_width=True
            ):

                st.session_state.show_popup = False

    popup_operator()

# ==================================================
# FOOTER
# ==================================================
st.markdown("""
<div class="footer">
Sistem Peringatan Dini Kedatangan Air Distribusi Berbasis IoT dan Machine Learning
</div>
""", unsafe_allow_html=True)
