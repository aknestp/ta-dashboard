import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import pytz 

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background-color: #f1f5f9; }
    
    .block-container, [data-testid="stAppViewBlockContainer"] { padding: 0rem !important; max-width: 100% !important; }
    header[data-testid="stHeader"] { display: none !important; }

    .app-shell { background: #ffffff; box-shadow: 0 4px 20px rgba(0,0,0,0.05); padding-bottom: 20px; overflow: hidden; margin: 0 auto; }
    .content-wrapper { padding: 0 5%; }

    /* HEADER DESKTOP */
    .main-header { background: #0A6847; padding: 20px 5%; display: flex; justify-content: space-between; align-items: center; color: white; }
    .header-left { display: flex; align-items: center; gap: 15px; }
    .header-logo { background: rgba(255,255,255,0.2); width: 45px; height: 45px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; flex-shrink: 0; }
    .header-title-wrapper { display: flex; flex-direction: column; }
    .header-title { font-size: 20px; font-weight: 700; margin: 0; line-height: 1.2; }
    .header-subtitle { font-size: 14px; color: rgba(255,255,255,0.9); margin: 0; }
    
    .header-right { display: flex; align-items: center; gap: 15px; }
    .status-badge { background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px; font-size: 13px; display: inline-flex; align-items: center; gap: 8px; }
    .dot-green { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; }
    .header-date { font-size: 13px; font-weight: 500; }

    /* STATUS BANNER - LINGKARAN ICON */
    .status-container { padding: 30px 15px; text-align: center; background: #fafafa; margin: 20px 5%; border-radius: 16px; border: 1px solid #e2e8f0; }
    .check-circle { color: white; width: 60px; height: 60px; border-radius: 50%; display: inline-flex; justify-content: center; align-items: center; font-size: 30px; margin-bottom: 15px; }
    .status-text-main { font-size: 28px; font-weight: 800; margin: 0; }

    /* CARD RINGKASAN */
    .summary-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; display: flex; align-items: center; gap: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); height: 100%; }
    .card-icon { background: #ecfdf5; color: #10b981; width: 45px; height: 45px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px; flex-shrink: 0; }
    .card-title { font-size: 12px; color: #64748b; margin-bottom: 2px; }
    .card-value { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 2px; }
    .card-subtitle { font-size: 11px; color: #94a3b8; }

    /* BOX GRAFIK & TABEL */
    .custom-box { margin-top: 20px; background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; }
    .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
    .section-title { font-size: 18px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; margin: 0; }
    .badge-update { background: #ecfdf5; color: #10b981; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; }

    /* TABEL HTML RAPI */
    .table-container { overflow-x: auto; border-radius: 8px; border: 1px solid #e2e8f0; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 14px; text-align: center; white-space: nowrap; }
    .custom-table th { background: #f8fafc; color: #0A6847; font-weight: 600; padding: 14px 15px; border-bottom: 2px solid #e2e8f0; }
    .custom-table td { padding: 12px 15px; border-bottom: 1px solid #f1f5f9; color: #334155; }
    .custom-table tbody tr:hover { background-color: #f8fafc; }
    .pill-success { background: #dcfce7; color: #166534; padding: 6px 12px; border-radius: 6px; font-weight: 600; font-size: 12px; display: inline-block; }

    /* FLOATING BUTTON */
    .st-key-fab_trigger { position: fixed; bottom: 30px; right: 30px; z-index: 9999; }
    .st-key-fab_trigger button { width: 60px; height: 60px; border-radius: 50%; background: #ef4444 !important; border: none !important; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4) !important; transition: transform 0.2s !important; }
    .st-key-fab_trigger button p { font-size: 24px !important; color: white !important; margin: 0 !important; }
    
    footer { display: none; }


    
    /* RESPONSIVE HP */
    @media (max-width: 768px) {
        .main-header { padding: 12px 10px; }
        .header-logo { width: 28px; height: 28px; font-size: 14px; }
        .header-title { font-size: 12px !important; }
        .header-subtitle { font-size: 12px !important; }
        .header-right { gap: 5px; flex-direction: column; align-items: flex-end; }
        .status-badge { font-size: 8px !important; padding: 2px 6px !important; }
        .header-date { font-size: 8px !important; }
        .status-text-main { font-size: 20px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================================================
# FUNGSI RENDER (DIPANGGIL DARI DASHBOARD.PY)
# ==================================================
def render_dashboard(latest_data, chart_data, history_data, status_text, sensor_status, server_url):
    load_css()
    
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    # === VARIABEL WARNA DAN TEXT ===
    is_flowing = "TIDAK" not in status_text.upper()
    status_icon = "✓" if is_flowing else "✕"
    status_title = "AIR MENGALIR" if is_flowing else "AIR TIDAK MENGALIR"
    status_subtitle = "Sistem dalam kondisi normal" if is_flowing else "Distribusi air sedang terhenti"
    main_color = "#10b981" if is_flowing else "#ef4444"
    
    is_sensor_online = "Online" in sensor_status
    sensor_txt = "Online" if is_sensor_online else "Offline"
    sensor_color = "#10b981" if is_sensor_online else "#ef4444"
    sensor_bg = "#ecfdf5" if is_sensor_online else "#fef2f2"

    tz_wib = pytz.timezone('Asia/Jakarta')
    waktu_sekarang = datetime.now(tz_wib).strftime("%d %b %Y - %H:%M:%S")

    st.markdown('<div class="app-shell">', unsafe_allow_html=True)

    # === HEADER ===
    st.markdown(f"""
        <div class="main-header">
            <div class="header-left">
                <div class="header-logo">💧</div>
                <div>
                    <h1 class="header-title">Sistem Peringatan Dini Kedatangan Air Distribusi</h1>
                    <p class="header-subtitle">Monitoring Distribusi Air Berbasis IoT & Machine Learning</p>
                </div>
            </div>
            <div class="header-right">
                <div class="status-badge"><span class="dot-green"></span> Server Terhubung</div>
                <div class="header-date">{waktu_sekarang}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # === STATUS UTAMA ===
    st.markdown(f"""
        <div class="status-container">
            <div class="check-circle" style="background: {main_color}; box-shadow: 0 4px 15px {main_color}40;">{status_icon}</div>
            <h2 class="status-text-main" style="color: {main_color};">{status_title}</h2>
            <p class="status-sub-main">{status_subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

    # === AMBIL DATA WAKTU DAN DURASI ===
    waktu_deteksi = latest_data.get("time", "-")
    kedatangan_terakhir = latest_data.get("last_water_time", "-")
    durasi_terakhir = "-"
    
    if history_data:
        first_row = history_data[0]
        durasi_terakhir = str(first_row.get("durasi", "-"))

    c1, c2, c3, c4 = st.columns(4)

    # === KARTU INFORMASI ===
    with c1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-icon" style="color: {sensor_color}; background: {sensor_bg};">📶</div>
            <div>
                <div class="card-title">Status Sensor</div>
                <div class="card-value" style="color: {sensor_color};">{sensor_txt}</div>
                <div class="card-subtitle">{"Koneksi stabil" if is_sensor_online else "Periksa alat"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-icon">🕒</div>
            <div>
                <div class="card-title">Waktu Deteksi</div>
                <div class="card-value">{waktu_deteksi.split(' ')[1] if ' ' in str(waktu_deteksi) else waktu_deteksi}</div>
                <div class="card-subtitle">{waktu_deteksi.split(' ')[0] if ' ' in str(waktu_deteksi) else '-'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-icon">💧</div>
            <div>
                <div class="card-title">Kedatangan Terakhir</div>
                <div class="card-value">{kedatangan_terakhir.split(' ')[1] if ' ' in str(kedatangan_terakhir) else kedatangan_terakhir}</div>
                <div class="card-subtitle">{kedatangan_terakhir.split(' ')[0] if ' ' in str(kedatangan_terakhir) else '-'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-icon">⏱</div>
            <div>
                <div class="card-title">Durasi Terakhir</div>
                <div class="card-value">{durasi_terakhir}</div>
                <div class="card-subtitle">Berdasarkan siklus terakhir</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


    # ==================================================
    # TABEL RIWAYAT DENGAN FITUR FILTER
    # ==================================================
    st.markdown('<div class="custom-box" style="margin-bottom: 25px;">', unsafe_allow_html=True)
    
    col_judul, col_filter = st.columns([4, 1])
    
    with col_judul:
        st.markdown('<div class="section-title">📋 Riwayat Distribusi</div>', unsafe_allow_html=True)
        
    with col_filter:
        sort_order = st.selectbox(
            "Filter:",
            ["Terbaru", "Terlama"],
            label_visibility="collapsed" 
        )

    # Struktur Tabel HTML
    html_table = """
        <div class="table-container" style="margin-top: 15px;">
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>No</th>
                        <th>Tanggal</th>
                        <th>Jam Mulai</th>
                        <th>Jam Selesai</th>
                        <th>Durasi</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
    """

    if history_data:
        sorted_history = list(history_data)
        
        def get_id(row):
            try: return int(row.get("id", 0))
            except: return 0

        is_descending = True if sort_order == "Terbaru" else False
        sorted_history.sort(key=get_id, reverse=is_descending)

        for i, row in enumerate(sorted_history[:5]):
            nomor_id = str(row.get("id", "-"))
            tanggal_db = str(row.get("tanggal", "-"))
            jam_mulai_db = str(row.get("jam_mulai", "-"))
            jam_selesai_db = str(row.get("jam_selesai", "-"))
            w_durasi = str(row.get("durasi", "-"))
            w_status = str(row.get("status", "Selesai"))
            
            html_table += f"<tr><td>{nomor_id}</td><td>{tanggal_db}</td><td>{jam_mulai_db}</td><td>{jam_selesai_db}</td><td>{w_durasi}</td><td><span class='pill-success'>{w_status}</span></td></tr>"
    else:
        html_table += "<tr><td colspan='6' style='padding: 20px;'>Belum ada riwayat distribusi tersedia di database.</td></tr>"

    html_table += "</tbody></table></div>"
    
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


    # === GRAFIK REALTIME ===
    st.markdown("""
        <div class="custom-box">
            <div class="section-header">
                <div class="section-title">📈 Grafik RMS Realtime</div>
                <div class="badge-update"><span class="dot-green" style="box-shadow: none; width:6px; height:6px;"></span> Update realtime</div>
            </div>
    """, unsafe_allow_html=True)

    chart_df = pd.DataFrame(chart_data)
    if not chart_df.empty and "rms" in chart_df.columns:
        x_axis = chart_df["time"] if "time" in chart_df.columns else chart_df.index
        y_axis = chart_df["rms"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis, y=y_axis, mode='lines+markers',
            line=dict(color='#10b981', width=3),
            marker=dict(size=6, color='white', line=dict(width=2, color='#10b981')),
            fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        fig.update_layout(
            height=280, margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#94a3b8', size=10)),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#94a3b8', size=10), title="RMS"),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("📊 Data grafik sedang disiapkan atau sensor belum mengirim data.")

    st.markdown("</div>", unsafe_allow_html=True)


    # === FOOTER ===
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; color: #94a3b8; font-size: 12px; margin-top: 15px; margin-bottom: 30px;">
        <span style="font-size: 16px; color: #10b981;">🛡️</span> 
        <div>
            © 2026 Sistem Peringatan Dini Kedatangan Air Distribusi<br>
            Powered by IoT & Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True) 
    st.markdown("</div>", unsafe_allow_html=True) 

    # === POPUP OPERATOR (GANGGUAN) ===
    if st.button("🔔", key="fab_trigger", help="Kirim Peringatan Gangguan"):
        st.session_state.show_popup = True

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
                                st.success("Informasi berhasil dikirim ke grup warga.")
                            else:
                                st.error("Gagal mengirim pesan ke server bot.")
                        except Exception as e:
                            st.error(f"Error Request: {e}")
                    else:
                        st.error("Password salah.")
            with btn2:
                if st.button("Batal ❌", use_container_width=True):
                    st.session_state.show_popup = False
                    st.rerun()

        popup_operator()
