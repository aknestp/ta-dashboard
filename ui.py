import streamlit as st
import pandas as pd
import requests
import plotly.express as px


# ==================================================
# MODERN UI STYLE
# ==================================================
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    :root {
        --primary: #0A6847;
        --secondary: #10b981;
        --danger: #e74c3c;
        --bg: linear-gradient(135deg, #f6f9fc 0%, #eef2f5 100%);
        --card: rgba(255, 255, 255, 0.90);
    }

    .stApp {
        background: var(--bg);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-header {
        background: linear-gradient(135deg, #0A6847, #10b981);
        padding: 40px;
        border-radius: 28px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(16, 185, 129, .25);
        margin-bottom: 30px;
    }

    .hero-title {
        color: white;
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: rgba(255, 255, 255, .9);
        font-size: 16px;
    }

    .status-hero {
        background: white;
        border-radius: 28px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, .05);
        margin-bottom: 25px;
    }

    .status-icon {
        font-size: 70px;
        margin-bottom: 10px;
    }

    .status-title {
        font-size: 52px;
        font-weight: 900;
        letter-spacing: -1px;
    }

    .status-subtitle {
        color: #64748b;
        margin-top: 8px;
        font-size: 15px;
    }

    [data-testid="stMetric"] {
        background: white;
        border: none;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, .04);
        border-top: 4px solid #10b981;
    }

    [data-testid="stMetricValue"] {
        color: #0A6847;
        font-weight: 800;
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #0A6847;
        margin-top: 25px;
        margin-bottom: 20px;
    }

    div[data-testid="stDataFrame"] {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, .05);
    }

    /* === MODERN BUTTON === */
    .stButton > button {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        border: none;
        border-radius: 16px;
        font-weight: 700;
        box-shadow: 0 8px 20px rgba(231, 76, 60, .35);
        transition: .3s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(231, 76, 60, .45);
    }

    /* === FAB BUTTON (FLOATING) === */
    button[key="fab_trigger"] {
        position: fixed !important;
        right: 30px !important;
        bottom: 40px !important;
        z-index: 9999 !important;
        width: 70px !important;
        height: 70px !important;
        min-width: 70px !important;
        border-radius: 50% !important;
        font-size: 32px !important;
    }

    .footer {
        text-align: center;
        color: #64748b;
        margin-top: 50px;
        font-size: 13px;
    }

    @media (max-width: 768px) {
        .hero-title { font-size: 28px; }
        .status-title { font-size: 34px; }
    }
    </style>
    """, unsafe_allow_html=True)


# ==================================================
# MAIN RENDER
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

    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    # --- HEADER ---
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">💧 Sistem Peringatan Dini Air</div>
        <div class="hero-subtitle">Monitoring Distribusi Air Berbasis IoT & Machine Learning</div>
    </div>
    """, unsafe_allow_html=True)

    # --- STATUS ---
    is_not_flowing = "TIDAK" in status_text.upper()
    status_color = "#e74c3c" if is_not_flowing else "#10b981"
    status_icon = "❌" if is_not_flowing else "✅"
    status_subtitle = "Distribusi air sedang mengalami gangguan" if is_not_flowing else "Sistem dalam kondisi normal"

    st.markdown(f"""
    <div class="status-hero">
        <div class="status-icon">{status_icon}</div>
        <div class="status-title" style="color: {status_color};">{status_text.upper()}</div>
        <div class="status-subtitle">{status_subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- SUMMARY CARDS ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📡 Status Sensor", sensor_status)
    with col2:
        st.metric("🕒 Waktu Deteksi", latest_data.get("time", "-"))
    with col3:
        st.metric("💧 Kedatangan Terakhir", latest_data.get("last_water_time", "-"))
    with col4:
        st.metric("⏱ Durasi Terakhir", latest_data.get("duration", "-"))

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CHART SECTION ---
    st.markdown('<div class="section-title">📈 Grafik RMS Realtime</div>', unsafe_allow_html=True)

    chart_df = pd.DataFrame(chart_data)

    if not chart_df.empty and "rms" in chart_df.columns:
        fig = px.line(chart_df, y="rms", markers=True)
        fig.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Data",
            yaxis_title="RMS",
            showlegend=False
        )
        fig.update_traces(line=dict(width=3))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data RMS belum tersedia")

    # --- HISTORY SECTION ---
    st.markdown('<div class="section-title">📋 Riwayat Distribusi Air</div>', unsafe_allow_html=True)

    history_df = pd.DataFrame(history_data)

    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True, hide_index=True, height=320)
    else:
        st.info("Belum ada riwayat distribusi")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- KONTROL OPERATOR ---
    st.markdown('<div class="section-title">⚙️ Kontrol Operator</div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([8, 1, 1])

    with col_c:
        if st.button("🚨", key="fab_trigger", use_container_width=True, help="Kirim Informasi Gangguan"):
            st.session_state.show_popup = True

    # --- POPUP OPERATOR ---
    if st.session_state.show_popup:
        @st.dialog("⚠️ Kirim Informasi Gangguan")
        def popup_operator():
            st.markdown("### Konfirmasi Operator\nInformasi ini akan dikirim ke grup WhatsApp warga.")
            password = st.text_input("Masukkan Password Operator", type="password")
            st.warning("Pesan yang akan dikirim:\n\nDistribusi air mengalami gangguan sementara.")

            btn1, btn2 = st.columns(2)

            with btn1:
                if st.button("Kirim Informasi ✅", use_container_width=True):
                    if password == "admin1":
                        try:
                            response = requests.post(
                                f"{server_url}/send_warning",
                                json={"message": "Distribusi air mengalami gangguan sementara"},
                                timeout=5
                            )
                            if response.status_code == 200:
                                st.success("Informasi berhasil dikirim.")
                                st.session_state.show_popup = False
                                st.rerun()
                            else:
                                st.error("Gagal mengirim informasi.")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Password salah.")

            with btn2:
                if st.button("Batal ❌", use_container_width=True):
                    st.session_state.show_popup = False
                    st.rerun()

        popup_operator()

    # --- FOOTER ---
    st.markdown("""
    <div class="footer">
        © 2026 Sistem Peringatan Dini Kedatangan Air Distribusi<br>
        Powered by IoT & Machine Learning
    </div>
    """, unsafe_allow_html=True)
