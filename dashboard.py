import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import requests
from datetime import datetime

# ==================================================
# CONFIG
# ==================================================
SERVER_URL = "https://YOUR-BACKEND.up.railway.app"

st.set_page_config(
    page_title="Sistem Peringatan Dini Air",
    page_icon="💧",
    layout="wide"
)

# ==================================================
# AUTO REFRESH
# ==================================================
st_autorefresh(interval=5000, key="refresh")

# ==================================================
# CSS
# ==================================================
st.markdown("""
<style>

.stApp{
    background-color:#f1f5f9;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.main-title{
    font-size:44px;
    font-weight:800;
    color:#0f172a;
    margin-bottom:5px;
}

.subtitle{
    color:#64748b;
    font-size:17px;
    margin-bottom:35px;
}

.section-title{
    font-size:28px;
    font-weight:bold;
    color:#0f172a;
    margin-top:20px;
    margin-bottom:15px;
}

div[data-testid="stDataFrame"]{
    border-radius:15px;
    overflow:hidden;
}

.stButton > button{
    background-color:#dc2626;
    color:white;
    border:none;
    border-radius:12px;
    padding:12px 20px;
    font-weight:bold;
    width:100%;
}

.stButton > button:hover{
    background-color:#b91c1c;
    color:white;
}

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
    status_color = "#16a34a"
else:
    status_text = "🔴 AIR TIDAK MENGALIR"
    status_color = "#dc2626"

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
<div class="main-title">
Sistem Peringatan Dini Kedatangan Air
</div>

<div class="subtitle">
Monitoring distribusi air berbasis IoT dan Machine Learning
</div>
""", unsafe_allow_html=True)

# ==================================================
# TOP CARDS
# ==================================================
col1, col2 = st.columns(2)

# ==================================================
# STATUS CARD
# ==================================================
with col1:

    st.markdown(
        f"""
        <div style="
            background:white;
            padding:30px;
            border-radius:20px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            min-height:280px;
        ">

            <div style="
                color:{status_color};
                font-size:38px;
                font-weight:bold;
            ">
                {status_text}
            </div>

            <br>

            <div style="
                color:#64748b;
                font-size:15px;
            ">
                Status Sensor
            </div>

            <div style="
                color:#0f172a;
                font-size:24px;
                font-weight:bold;
            ">
                {sensor_status}
            </div>

            <br>

            <div style="
                color:#64748b;
                font-size:15px;
            ">
                Waktu Deteksi
            </div>

            <div style="
                color:#0f172a;
                font-size:22px;
                font-weight:bold;
            ">
                {latest_data.get("time", "-")}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# INFO CARD
# ==================================================
with col2:

    st.markdown(
        f"""
        <div style="
            background:white;
            padding:30px;
            border-radius:20px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            min-height:280px;
        ">

            <div style="
                color:#64748b;
                font-size:15px;
            ">
                Kedatangan Air Terakhir
            </div>

            <div style="
                color:#0f172a;
                font-size:28px;
                font-weight:bold;
            ">
                {latest_data.get("last_water_time", "-")}
            </div>

            <br><br>

            <div style="
                color:#64748b;
                font-size:15px;
            ">
                Durasi Distribusi Terakhir
            </div>

            <div style="
                color:#0f172a;
                font-size:28px;
                font-weight:bold;
            ">
                {latest_data.get("duration", "-")}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# HISTORY
# ==================================================
st.markdown("""
<div class="section-title">
Riwayat Distribusi Air
</div>
""", unsafe_allow_html=True)

if isinstance(history_data, dict):
    history_data = [history_data]

elif not isinstance(history_data, list):
    history_data = []

history_df = pd.DataFrame(history_data)

if not history_df.empty:

    st.dataframe(
        history_df,
        use_container_width=True,
        height=300
    )

else:

    st.info("Belum ada riwayat distribusi")

# ==================================================
# CHART
# ==================================================
st.markdown("""
<div class="section-title">
Grafik RMS Realtime
</div>
""", unsafe_allow_html=True)

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
        chart_df["rms"],
        height=350
    )

else:

    st.warning(
        "Data RMS belum tersedia"
    )

# ==================================================
# OPERATOR BUTTON
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
