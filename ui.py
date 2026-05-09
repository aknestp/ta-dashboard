import streamlit as st
import pandas as pd
import requests

# ==================================================
# CSS
# ==================================================
def load_css():

    st.markdown("""
    <style>

    .stApp{
        background-color:#dfe8d5;
    }

    .block-container{
        padding-top:1rem;
        padding-bottom:1rem;
        max-width:1400px;
    }

    /* HEADER */
    .top-header{
        background:#1b6b3a;
        padding:20px;
        border-radius:6px;
        margin-bottom:18px;
        border:2px solid #245c35;
    }

    .top-title{
        color:white;
        font-size:42px;
        font-weight:900;
        letter-spacing:1px;
    }

    .top-subtitle{
        color:#d7f0dc;
        font-size:16px;
        margin-top:5px;
    }

    /* SECTION */
    .section-title{
        background:#1b6b3a;
        color:white;
        padding:10px 15px;
        font-size:24px;
        font-weight:bold;
        border-radius:4px;
        margin-top:20px;
        margin-bottom:10px;
    }

    /* CARD */
    [data-testid="stVerticalBlockBorderWrapper"]{
        background:#edf4e8;
        border:2px solid #9eb397;
        border-radius:4px;
        padding:10px;
        box-shadow:none;
        display: flex;
        flex-direction: column;
        height: 100%;
        justify-content: space-between;
}
    }

    /* METRIC */
    [data-testid="stMetric"]{
        background:#f6faf2;
        border:1px solid #b7c7b0;
        padding:10px;
        border-radius:2px;
        margin-bottom: 10px;
    }

    /* METRIC LABEL */
    [data-testid="stMetricLabel"]{
        color:#245c35;
        font-weight:bold;
    }

    /* METRIC VALUE */
    [data-testid="stMetricValue"]{
        color:#1b3d22;
        font-weight:900;
    }

    /* DATAFRAME */
    div[data-testid="stDataFrame"]{
        border:2px solid #9eb397;
        border-radius:4px;
        overflow:hidden;
    }

    /* CHART */
    div[data-testid="stVegaLiteChart"]{
        background:#edf4e8;
        border:2px solid #9eb397;
        border-radius:4px;
        padding:10px;
    }

    /* BUTTON */
    .stButton > button{
        background:#c0392b;
        color:white;
        border:none;
        border-radius:4px;
        font-weight:bold;
        padding:12px;
    }

    .stButton > button:hover{
        background:#a93226;
        color:white;
    }

    /* FOOTER */
    .footer{
        text-align:center;
        color:#245c35;
        margin-top:30px;
        font-size:14px;
        font-weight:bold;
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

    <div class="top-title">
    SISTEM PERINGATAN DINI KEDATANGAN AIR
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

    # Kolom Kiri: Status Utama
    with col1:
        with st.container(border=True):
            # Header Status dengan Icon (Opsional: tambahkan emoji agar lebih hidup)
            st.markdown(f"### {status_text}")
            
            # Menggunakan sub-columns di dalam container agar metric berjejer rapi
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.metric("Status Sensor", sensor_status)
            with sub_col2:
                st.metric("Waktu Deteksi", latest_data.get("time", "-"))

    # Kolom Kanan: Informasi Riwayat Terakhir
    with col2:
        with st.container(border=True):
            st.markdown("### Ringkasan Distribusi")
            
            sub_col3, sub_col4 = st.columns(2)
            with sub_col3:
                st.metric("Kedatangan Terakhir", latest_data.get("last_water_time", "-"))
            with sub_col4:
                st.metric("Durasi Terakhir", latest_data.get("duration", "-"))

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
    GRAFIK RMS REALTIME
    </div>
    """, unsafe_allow_html=True)

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
    # WARNING BUTTON
    # ==================================================
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    if st.button(
        "⚠ INFORMASI GANGGUAN DISTRIBUSI"
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
                                f"{server_url}/send_warning",
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
