import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from streamlit_float import *

# ==================================================
# CSS MODERN & RESPONSIVE
# ==================================================
def load_css():
    st.markdown("""
    <style>
    /* Background Aplikasi Keseluruhan */
    .stApp {
        background-color: #F4F7F6;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 1200px;
    }
    /* HEADER MODERN DENGAN GRADIENT */
    .top-header {
        background: linear-gradient(135deg, #0A6847 0%, #7ABA78 100%);
        padding: 30px 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center;
    }
    .top-title {
        color: #ffffff;
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 1px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        margin-bottom: 5px;
    }
    .top-subtitle {
        color: #E8F3EE;
        font-size: 16px;
        font-weight: 500;
    }
    /* SECTION TITLE MODERN */
    .section-title {
        background: transparent;
        color: #0A6847;
        padding: 10px 0px;
        font-size: 22px;
        font-weight: 800;
        border-bottom: 3px solid #7ABA78;
        margin-top: 25px;
        margin-bottom: 15px;
        display: inline-block;
    }
    /* CARD MODERN (CONTAINER) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: none !important;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        display: flex;
        flex-direction: column;
        height: 100%;
        justify-content: space-between;
    }
    /* METRIC MODERN (KOTAK DATA) */
    [data-testid="stMetric"] {
        background: #F9FCFB;
        border: none;
        border-left: 5px solid #0A6847;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.06);
    }
    /* METRIC LABEL */
    [data-testid="stMetricLabel"] {
        color: #4A5551;
        font-weight: 600;
    }
    /* METRIC VALUE */
    [data-testid="stMetricValue"] {
        color: #0A6847;
        font-weight: 900;
    }
    /* DATAFRAME */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E0EBE5;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    /* CHART */
    div[data-testid="stVegaLiteChart"] {
        background: #ffffff;
        border: 1px solid #E0EBE5;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
    /* BUTTON WARNING MODERN */
    .stButton > button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 12px;
        box-shadow: 0 4px 10px rgba(192, 57, 43, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #c0392b 0%, #922b21 100%);
        color: white;
        box-shadow: 0 6px 14px rgba(192, 57, 43, 0.4);
        transform: scale(1.01);
    }
    /* FOOTER */
    .footer {
        text-align: center;
        color: #7f8c8d;
        margin-top: 40px;
        font-size: 14px;
        font-weight: 500;
        border-top: 1px solid #E0EBE5;
        padding-top: 20px;
    }
    /* ==================================================
       RESPONSIVE PADA LAYAR HANDPHONE / KECIL
       ================================================== */
    @media (max-width: 768px) {
        .top-header { padding: 20px 15px; }
        .top-title { font-size: 24px !important; }
        .top-subtitle { font-size: 13px !important; }
        .section-title { font-size: 18px !important; }
        [data-testid="stMetricValue"] > div { font-size: 1.4rem !important; }
        [data-testid="stMetricLabel"] p { font-size: 13px !important; }
        .footer { font-size: 12px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================================================
# MAIN UI
# ==================================================
def render_dashboard(
    latest_data,
    chart_data,
    history_data,
    status_text,
    sensor_status,
    server_url
):
    float_init()

    st.markdown("""
    <style>
    .stApp{
        background:linear-gradient(180deg,#eef7f2 0%,#f8faf9 100%);
    }

    .top-header{
        background:linear-gradient(135deg,#0A6847,#2E8B57,#7ABA78);
        padding:35px;
        border-radius:24px;
        text-align:center;
        box-shadow:0 15px 35px rgba(0,0,0,0.12);
        margin-bottom:25px;
    }

    .top-title{
        color:white;
        font-size:42px;
        font-weight:900;
    }

    .top-subtitle{
        color:#EAF7EE;
        font-size:16px;
    }

    .status-card{
        background:white;
        padding:35px;
        border-radius:24px;
        text-align:center;
        margin-bottom:25px;
        box-shadow:0 10px 30px rgba(0,0,0,0.08);
    }

    .status-title{
        color:#888;
        font-size:18px;
        font-weight:700;
        margin-bottom:10px;
    }

    .status-value{
        font-size:42px;
        font-weight:900;
    }

    [data-testid="stMetric"]{
        background:white;
        padding:20px;
        border-radius:20px;
        box-shadow:0 6px 20px rgba(0,0,0,0.06);
        border:none;
    }

    [data-testid="stMetric"]:hover{
        transform:translateY(-3px);
        transition:0.3s;
    }

    [data-testid="stDataFrame"]{
        border-radius:20px;
        overflow:hidden;
    }

    .section-title{
        color:#0A6847;
        font-size:24px;
        font-weight:800;
        margin-top:20px;
        margin-bottom:15px;
    }

    .footer{
        text-align:center;
        margin-top:50px;
        color:#7f8c8d;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="top-header">
        <div class="top-title">
            💧 SISTEM PERINGATAN DINI KEDATANGAN AIR
        </div>

        <div class="top-subtitle">
            Monitoring Distribusi Air Berbasis IoT dan Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

    is_not_flowing = "TIDAK" in status_text.upper()
    color_status = "#e74c3c" if is_not_flowing else "#27ae60"

    st.markdown(f"""
    <div class="status-card">

        <div class="status-title">
            STATUS DISTRIBUSI AIR
        </div>

        <div class="status-value"
        style="color:{color_status};">
            {status_text}
        </div>

    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric(
            "📡 Status Sensor",
            sensor_status
        )

    with col2:
        st.metric(
            "🕒 Waktu Deteksi",
            latest_data.get("time","-")
        )

    with col3:
        st.metric(
            "💧 Kedatangan Terakhir",
            latest_data.get("last_water_time","-")
        )

    with col4:
        st.metric(
            "⏱ Durasi Terakhir",
            latest_data.get("duration","-")
        )

    st.markdown(
        '<div class="section-title">📈 Grafik RMS Realtime</div>',
        unsafe_allow_html=True
    )

    chart_df = pd.DataFrame(chart_data)

    if not chart_df.empty and "rms" in chart_df.columns:

        fig = px.line(
            chart_df,
            y="rms",
            markers=True
        )

        fig.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            ),
            xaxis_title="Data",
            yaxis_title="RMS"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning("Data RMS belum tersedia")

    st.markdown(
        '<div class="section-title">📋 Riwayat Distribusi Air</div>',
        unsafe_allow_html=True
    )

    history_df = pd.DataFrame(history_data)

    if not history_df.empty:
        st.dataframe(
            history_df,
            use_container_width=True,
            height=320
        )
    else:
        st.info("Belum ada riwayat distribusi")

    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    if st.button("🚨", key="floating_warning"):
        st.session_state.show_popup = True

    float_parent(
        css="""
        position:fixed;
        bottom:25px;
        right:25px;
        width:80px;
        height:80px;
        border-radius:50%;
        z-index:999;
        """
    )

    if st.session_state.show_popup:

        @st.dialog("Konfirmasi Operator")
        def popup_operator():

            password = st.text_input(
                "Masukkan Password Operator",
                type="password"
            )

            st.warning(
                "Pesan yang akan dikirim ke Grup WhatsApp Warga:\n\nDistribusi air mengalami gangguan sementara"
            )

            c1,c2 = st.columns(2)

            with c1:
                if st.button("Kirim Informasi"):

                    if password == "admin1":

                        try:

                            response = requests.post(
                                f"{server_url}/send_warning",
                                json={
                                    "message":"Distribusi air mengalami gangguan sementara"
                                },
                                timeout=5
                            )

                            if response.status_code == 200:
                                st.success(
                                    "Informasi berhasil dikirim ke Grup WA!"
                                )
                                st.session_state.show_popup = False

                            else:
                                st.error(
                                    "Gagal mengirim informasi"
                                )

                        except Exception as e:
                            st.error(e)

                    else:
                        st.error("Password salah")

            with c2:

                if st.button("Batal"):
                    st.session_state.show_popup = False
                    st.rerun()

        popup_operator()

    st.markdown("""
    <div class="footer">
        © 2026 Sistem Peringatan Dini Kedatangan Air Distribusi
        <br>
        Berbasis IoT dan Machine Learning
    </div>
    """, unsafe_allow_html=True)
