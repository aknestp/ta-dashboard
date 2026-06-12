import streamlit as st
import pandas as pd
import requests

# ==================================================
# CSS MODERN & RESPONSIVE (GLASSMORPHISM)
# ==================================================
def load_css():
    st.markdown("""
    <style>
    /* === GLOBAL FONTS & COLORS === */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    :root {
        --primary-color: #0A6847;
        --secondary-color: #7ABA78;
        --accent-blue: #0984e3;
        --danger-color: #e74c3c;
        --bg-gradient: linear-gradient(135deg, #f6f9fc 0%, #eef2f5 100%);
        --card-bg: rgba(255, 255, 255, 0.85);
        --text-main: #1e293b;
        --text-muted: #64748b;
    }

    /* APP BACKGROUND */
    .stApp {
        background: var(--bg-gradient);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-main);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    /* === GLASSMORPHISM HEADER === */
    .modern-header {
        background: linear-gradient(135deg, #0A6847 0%, #10b981 100%);
        padding: 35px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(10, 104, 71, 0.25);
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .modern-header h1 {
        color: #ffffff;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .modern-header p {
        color: rgba(255,255,255,0.9);
        font-size: 16px;
        font-weight: 400;
        margin-top: 8px;
    }

    /* === STATUS CARD (GLASS STYLE) === */
    .status-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.6);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .status-card:hover {
        transform: translateY(-2px);
    }
    .status-text {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    /* === METRIC CARDS === */
    [data-testid="stMetric"] {
        background: var(--card-bg);
        border: none;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        border-left: 4px solid var(--primary-color);
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-muted);
        font-weight: 600;
        font-size: 14px;
    }
    [data-testid="stMetricValue"] {
        color: var(--primary-color);
        font-weight: 800;
        font-size: 26px;
    }

    /* === SECTIONS === */
    .section-header {
        color: var(--primary-color);
        font-size: 22px;
        font-weight: 800;
        margin-top: 30px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-header::after {
        content: "";
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, var(--secondary-color), transparent);
    }

    /* === DATAFRAME & CHART === */
    div[data-testid="stDataFrame"], div[data-testid="stVegaLiteChart"] {
        background: var(--card-bg);
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        border: 1px solid rgba(255,255,255,0.6);
    }

    /* === FLOATING ACTION BUTTON (FAB) === */
    /* Target the specific button by key using data-based attributes */
    button[key="fab_trigger"] {
        position: fixed !important;
        right: 25px !important;
        bottom: 40px !important;
        z-index: 9999 !important;
        
        width: 70px !important;
        height: 70px !important;
        min-width: 70px !important;
        border-radius: 50% !important;
        
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
        
        color: white !important;
        font-size: 30px !important;
        
        border: none !important;
        
        box-shadow: 0 8px 20px rgba(231, 76, 60, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    button[key="fab_trigger"]:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 12px 25px rgba(231, 76, 60, 0.5) !important;
    }

    /* === FOOTER === */
    .modern-footer {
        text-align: center;
        color: var(--text-muted);
        padding: 30px 0;
        margin-top: 50px;
        font-size: 13px;
        border-top: 1px solid rgba(0,0,0,0.05);
    }

    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .modern-header { padding: 25px 20px; }
        .modern-header h1 { font-size: 26px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================================================
# MAIN UI RENDER
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

    # Initialize session state
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    # --- HEADER ---
    st.markdown("""
    <div class="modern-header">
        <h1>💧 Sistem Peringatan Dini Air</h1>
        <p>Monitoring Distribusi Air Berbasis IoT & Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

    # --- STATUS BANNER ---
    is_not_flowing = "TIDAK" in status_text.upper()
    status_color = "#e74c3c" if is_not_flowing else "#10b981"
    
    st.markdown(f"""
    <div class="status-card" style="border-top: 5px solid {status_color}">
        <span class="status-text" style="color: {status_color}">
            {status_text.upper()}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # --- METRICS SECTION ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📡 STATUS SENSOR")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric("Koneksi", sensor_status)
        with m_col2:
            st.metric("Waktu Deteksi", latest_data.get("time", "-"))

    with col2:
        st.markdown("### 📊 RINGKASAN")
        m_col3, m_col4 = st.columns(2)
        with m_col3:
            st.metric("Kedatangan Terakhir", latest_data.get("last_water_time", "-"))
        with m_col4:
            st.metric("Durasi Terakhir", latest_data.get("duration", "-"))

    # --- HISTORY SECTION ---
    st.markdown("""
    <div class="section-header">
    📋 Riwayat Distribusi
    </div>
    """, unsafe_allow_html=True)
    
    history_df = pd.DataFrame(history_data)
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True, height=280, hide_index=True)
    else:
        st.info("Belum ada riwayat distribusi")

    # --- CHART SECTION ---
    st.markdown("""
    <div class="section-header">
    📈 Grafik RMS Realtime
    </div>
    """, unsafe_allow_html=True)
    
    chart_df = pd.DataFrame(chart_data)
    if not chart_df.empty and "rms" in chart_df.columns:
        st.line_chart(chart_df["rms"], height=320)
    else:
        st.warning("Data RMS belum tersedia")

    # --- FLOATING ACTION BUTTON (FAB) ---
    # Using columns to push the button to the right side
    
    col_left, col_right = st.columns([9, 1])
    
    with col_right:
        if st.button(
            "🚨",
            key="fab_trigger",
            help="Kirim Informasi Gangguan"
        ):
            st.session_state.show_popup = True

    # --- POPUP DIALOG ---
    if st.session_state.show_popup:
        @st.dialog("⚠️ Kirim Informasi Gangguan")
        def popup_operator():
            password = st.text_input("Masukkan Password Operator", type="password")
            
            st.warning(
                "Pesan yang akan dikirim ke Grup WhatsApp Warga:\n\n"
                "**Distribusi air mengalami gangguan sementara**"
            )
            
            p_col1, p_col2 = st.columns(2)
            
            with p_col1:
                if st.button("Kirim Informasi ✅", use_container_width=True):
                    if password == "admin1":
                        try:
                            response = requests.post(
                                f"{server_url}/send_warning",
                                json={"message": "Distribusi air mengalami gangguan sementara"},
                                timeout=5
                            )
                            if response.status_code == 200:
                                st.success("Berhasil dikirim ke Grup WA!")
                                st.session_state.show_popup = False
                                st.rerun()
                            else:
                                st.error("Gagal mengirim")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Password salah")
            
            with p_col2:
                if st.button("Batal ❌", use_container_width=True):
                    st.session_state.show_popup = False
                    st.rerun()

        popup_operator()

    # --- FOOTER ---
    st.markdown("""
    <div class="modern-footer">
    © 2026 Sistem Peringatan Dini Kedataan Air Distribusi <br>
    Powered by IoT & Machine Learning
    </div>
    """, unsafe_allow_html=True)
