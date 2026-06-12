import streamlit as st
import pandas as pd
import requests
import plotly.express as px


def load_css():
    st.markdown("""
    <style>

    .stApp{
        background: linear-gradient(
            180deg,
            #eef7f2 0%,
            #f8faf9 100%
        );
    }

    .block-container{
        padding-top:1rem;
        max-width:1400px;
    }

    .top-header{
        background: linear-gradient(
            135deg,
            #0A6847,
            #2E8B57,
            #7ABA78
        );

        padding:35px;
        border-radius:25px;

        text-align:center;

        box-shadow:
        0 15px 35px rgba(0,0,0,0.12);

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
        border-radius:24px;
        padding:30px;

        text-align:center;

        box-shadow:
        0 10px 25px rgba(0,0,0,0.08);

        margin-bottom:25px;
    }

    .status-title{
        color:#888;
        font-size:18px;
        font-weight:700;
    }

    .status-value{
        font-size:42px;
        font-weight:900;
    }

    [data-testid="stMetric"]{
        background:white;
        padding:18px;
        border-radius:18px;

        box-shadow:
        0 6px 20px rgba(0,0,0,0.06);

        border:none;
    }

    [data-testid="stMetric"]:hover{
        transform:translateY(-3px);
        transition:0.3s;
    }

    div[data-testid="stDataFrame"]{
        border-radius:16px;
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
        color:#7f8c8d;
        margin-top:40px;
    }

    /* Tombol Bulat */

    div[data-testid="stButton"] button[kind="secondary"]{
        border-radius:50px;
    }

    .floating-container{
        position:fixed;
        right:25px;
        bottom:25px;
        z-index:99999;
    }

    @media (max-width:768px){

        .top-title{
            font-size:26px;
        }

        .status-value{
            font-size:28px;
        }
    }

    </style>
    """, unsafe_allow_html=True)


def render_dashboard(
    latest_data,
    chart_data,
    history_data,
    status_text,
    sensor_status,
    server_url
):

    load_css()

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

    color_status = (
        "#e74c3c"
        if is_not_flowing
        else "#27ae60"
    )

    st.markdown(f"""
    <div class="status-card">

        <div class="status-title">
            STATUS DISTRIBUSI AIR
        </div>

        <div
        class="status-value"
        style="color:{color_status};">

            {status_text}

        </div>

    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric(
            "📡 Status Sensor",
            sensor_status
        )

    with c2:
        st.metric(
            "🕒 Waktu Deteksi",
            latest_data.get("time","-")
        )

    with c3:
        st.metric(
            "💧 Kedatangan Terakhir",
            latest_data.get("last_water_time","-")
        )

    with c4:
        st.metric(
            "⏱ Durasi Terakhir",
            latest_data.get("duration","-")
        )

    st.markdown(
        '<div class="section-title">📈 Grafik RMS Realtime</div>',
        unsafe_allow_html=True
    )

    chart_df = pd.DataFrame(chart_data)

    if (
        not chart_df.empty
        and "rms" in chart_df.columns
    ):

        fig = px.line(
            chart_df,
            y="rms",
            markers=True
        )

        fig.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            xaxis_title="Data",
            yaxis_title="RMS"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning(
            "Data RMS belum tersedia"
        )

    st.markdown(
        '<div class="section-title">📋 Riwayat Distribusi Air</div>',
        unsafe_allow_html=True
    )

    history_df = pd.DataFrame(
        history_data
    )

    if not history_df.empty:

        st.dataframe(
            history_df,
            use_container_width=True,
            height=320
        )

    else:

        st.info(
            "Belum ada riwayat distribusi"
        )

    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    st.markdown(
        '<div class="floating-container">',
        unsafe_allow_html=True
    )

    if st.button(
        "🚨",
        key="warning_btn"
    ):
        st.session_state.show_popup = True

    st.markdown(
        '</div>',
        unsafe_allow_html=True
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

            col1,col2 = st.columns(2)

            with col1:

                if st.button(
                    "Kirim Informasi"
                ):

                    if password == "admin1":

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

                        st.error(
                            "Password salah"
                        )

            with col2:

                if st.button(
                    "Batal"
                ):
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
