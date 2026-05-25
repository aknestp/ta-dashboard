import streamlit as st
import pandas as pd
import requests

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

    load_css()

    # ==================================================
    # HEADER
    # ==================================================
    st.markdown("""
    <div class="top-header">
        <div class="top-title">💧 SISTEM PERINGATAN DINI KEDATANGAN AIR</div>
        <div class="top-subtitle">Monitoring Distribusi Air Berbasis IoT dan Machine Learning</div>
    </div>
    """, unsafe_allow_html=True)

   # ==================================================
    # BANNER STATUS UTAMA (DIPISAH KE ATAS)
    # ==================================================
    is_not_flowing = "TIDAK" in status_text.upper()
    color_status = "#c0392b" if is_not_flowing else "#0A6847"
    border_color = "#e74c3c" if is_not_flowing else "#7ABA78"
    
    st.markdown(f"""
    <div style="text-align: center; background-color: #ffffff; padding: 15px; 
                border-radius: 12px; margin-bottom: 20px; border: 2px solid {border_color};
                box-shadow: 0 4px 12px rgba(0,0,0,0.04);">
        <h2 style="color: {color_status}; margin: 0; font-weight: 900; letter-spacing: 1px;">
            {status_text.upper()}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # ==================================================
    # TOP SECTION (KOTAK KIRI DAN KANAN YANG SIMETRIS)
    # ==================================================
    col1, col2 = st.columns(2)

    # Kolom Kiri: Informasi Sensor
    with col1:
        with st.container(border=True):
            st.markdown("### 📡 Status Sensor")
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.metric("Koneksi", sensor_status)
            with sub_col2:
                st.metric("Waktu Deteksi", latest_data.get("time", "-"))

    # Kolom Kanan: Informasi Riwayat Terakhir
    with col2:
        with st.container(border=True):
            st.markdown("### 📊 Ringkasan Distribusi")
            
            sub_col3, sub_col4 = st.columns(2)
            with sub_col3:
                st.metric("Kedatangan Terakhir", latest_data.get("last_water_time", "-"))
            with sub_col4:
                st.metric("Durasi Terakhir", latest_data.get("duration", "-"))

    # ==================================================
    # HISTORY TITLE
    # ==================================================
    st.markdown("""
    <div class="section-title">
    📋 Riwayat Distribusi Air
    </div>
    """, unsafe_allow_html=True)

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
        st.info("Belum ada riwayat distribusi")

    # ==================================================
    # CHART TITLE
    # ==================================================
    st.markdown("""
    <div class="section-title">
    📈 Grafik RMS Realtime
    </div>
    """, unsafe_allow_html=True)

    chart_df = pd.DataFrame(chart_data)

    # ==================================================
    # SHOW CHART
    # ==================================================
    if (not chart_df.empty and "rms" in chart_df.columns):
        st.line_chart(
            chart_df["rms"],
            height=350
        )
    else:
        st.warning("Data RMS belum tersedia")

    # ==================================================
    # WARNING BUTTON
    # ==================================================
    st.markdown("<br>", unsafe_allow_html=True) 
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    if st.button("🚨 Kirim Informasi Gangguan", use_container_width=True):
        st.session_state.show_popup = True

    # ==================================================
    # POPUP
    # ==================================================
    if st.session_state.show_popup:
        @st.dialog("Konfirmasi Operator")
        def popup_operator():
            password = st.text_input("Masukkan Password Operator", type="password")
            st.warning("Pesan yang akan dikirim:\n\nDistribusi air mengalami gangguan sementara")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Kirim Informasi", use_container_width=True):
                    if password == "admin1":
                        try:
                            response = requests.post(
                                f"{server_url}/send_warning",
                                json={"message": "Distribusi air mengalami gangguan sementara"},
                                timeout=2
                            )
                            if response.status_code == 200:
                                st.success("Informasi berhasil dikirim")
                                st.session_state.show_popup = False
                            else:
                                st.error("Gagal mengirim informasi")
                        except Exception as e:
                            st.error(e)
                    else:
                        st.error("Password salah")
            with col2:
                if st.button("Batal", use_container_width=True):
                    st.session_state.show_popup = False

        popup_operator()

    # ==================================================
    # FOOTER
    # ==================================================
    st.markdown("""
    <div class="footer">
    © 2026 Sistem Peringatan Dini Kedatangan Air Distribusi <br>
    Berbasis IoT dan Machine Learning
    </div>
    """, unsafe_allow_html=True)
