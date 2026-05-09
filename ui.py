# ui.py

import streamlit as st
import pandas as pd
import requests


# ==================================================
# LOAD CSS
# ==================================================
def load_css():

    st.markdown("""
    <style>

    /* =========================
       BACKGROUND
    ========================= */
    .stApp{
        background-color:#dfe8d5;
    }

    /* =========================
       MAIN LAYOUT
    ========================= */
    .block-container{
        max-width:1400px;
        padding-top:1rem;
        padding-bottom:1rem;
    }

    /* =========================
       HEADER
    ========================= */
    .top-header{
        background:#1b6b3a;
        border:2px solid #245c35;
        padding:20px;
        border-radius:4px;
        margin-bottom:20px;
    }

    .top-title{
        color:white;
        font-size:40px;
        font-weight:900;
        letter-spacing:1px;
    }

    .top-subtitle{
        color:#d7f0dc;
        margin-top:5px;
        font-size:15px;
    }

    /* =========================
       SECTION TITLE
    ========================= */
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

    /* =========================
       PANEL
    ========================= */
    .panel{
        background:#edf4e8;
        border:2px solid #9eb397;
        padding:15px;
        border-radius:4px;

        height:420px;

        display:flex;
        flex-direction:column;
        justify-content:flex-start;
    }

    /* =========================
       PANEL HEADER
    ========================= */
    .panel-header{
        background:#1b6b3a;
        color:white;
        padding:10px;
        font-size:22px;
        font-weight:bold;
        margin-bottom:15px;
        border-radius:2px;
    }

    /* =========================
       STATUS
    ========================= */
    .status-box{
        font-size:40px;
        font-weight:900;
        color:#17351e;
        margin-bottom:15px;
    }

    /* =========================
       MINI BOX
    ========================= */
    .mini-box{
        background:#f8fbf5;
        border:1px solid #b8c7b0;
        padding:15px;
        margin-bottom:12px;
        border-radius:2px;
    }

    /* =========================
       MINI TITLE
    ========================= */
    .mini-title{
        color:#245c35;
        font-size:14px;
        font-weight:bold;
        margin-bottom:8px;
    }

    /* =========================
       MINI VALUE
    ========================= */
    .mini-value{
        color:#17351e;
        font-size:30px;
        font-weight:900;
    }

    /* =========================
       TABLE
    ========================= */
    div[data-testid="stDataFrame"]{
        border:2px solid #9eb397;
        border-radius:4px;
        overflow:hidden;
    }

    /* =========================
       CHART
    ========================= */
    div[data-testid="stVegaLiteChart"]{
        background:#edf4e8;
        border:2px solid #9eb397;
        border-radius:4px;
        padding:10px;
    }

    /* =========================
       BUTTON
    ========================= */
    .stButton > button{
        background:#c0392b;
        color:white;
        border:none;
        border-radius:4px;
        font-weight:bold;
        padding:14px;
        width:100%;
        font-size:16px;
    }

    .stButton > button:hover{
        background:#a93226;
        color:white;
    }

    /* =========================
       FOOTER
    ========================= */
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
            DASHBOARD DISTRIBUSI AIR
        </div>

        <div class="top-subtitle">
            Sistem Peringatan Dini Kedatangan Air Berbasis IoT dan Machine Learning
        </div>

    </div>
    """, unsafe_allow_html=True)

    # ==================================================
    # TOP SECTION
    # ==================================================
    col1, col2 = st.columns(2)

    # ==================================================
    # STATUS PANEL
    # ==================================================
    with col1:

        html_status = f"""
        <div class="panel">

            <div class="panel-header">
                STATUS DISTRIBUSI
            </div>

            <div class="status-box">
                {status_text}
            </div>

            <div class="mini-box">

                <div class="mini-title">
                    STATUS SENSOR
                </div>

                <div class="mini-value">
                    {sensor_status}
                </div>

            </div>

            <div class="mini-box">

                <div class="mini-title">
                    WAKTU DETEKSI
                </div>

                <div class="mini-value">
                    {latest_data.get("time", "-")}
                </div>

            </div>

        </div>
        """

        st.markdown(
            html_status,
            unsafe_allow_html=True
        )

    # ==================================================
    # INFO PANEL
    # ==================================================
    with col2:

        html_info = f"""
        <div class="panel">

            <div class="panel-header">
                INFORMASI TERAKHIR
            </div>

            <div class="mini-box">

                <div class="mini-title">
                    KEDATANGAN AIR TERAKHIR
                </div>

                <div class="mini-value">
                    {latest_data.get("last_water_time", "-")}
                </div>

            </div>

            <div class="mini-box">

                <div class="mini-title">
                    DURASI DISTRIBUSI TERAKHIR
                </div>

                <div class="mini-value">
                    {latest_data.get("duration", "-")}
                </div>

            </div>

        </div>
        """

        st.markdown(
            html_info,
            unsafe_allow_html=True
        )

    # ==================================================
    # HISTORY TITLE
    # ==================================================
    st.markdown("""
    <div class="section-title">
        RIWAYAT DISTRIBUSI AIR
    </div>
    """, unsafe_allow_html=True)

    # ==================================================
    # HISTORY TABLE
    # ==================================================
    history_df = pd.DataFrame(history_data)

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

    # ==================================================
    # CHART
    # ==================================================
    chart_df = pd.DataFrame(chart_data)

    if (
        not chart_df.empty
        and "rms" in chart_df.columns
    ):

        chart_df = chart_df.tail(30)

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
    # POPUP OPERATOR
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
        Sistem Monitoring Distribusi Air Realtime
    </div>
    """, unsafe_allow_html=True)
