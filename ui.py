import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import pytz  # Pastikan import pytz ditambahkan

# ==================================================
# CSS MODERN (RESPONSIVE & FULL-WIDTH)
# ==================================================
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
    }
    
    .stApp { 
        background-color: #f1f5f9; 
    }
    
    /* HILANGKAN PADDING BAWAAN AGAR HEADER FULL LAYAR */
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* CONTAINER UTAMA (Menyesuaikan di Desktop & HP) */
    .app-shell {
        background: #ffffff;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        padding-bottom: 20px;
        overflow: hidden;
        margin: 0 auto;
        min-height: 100vh;
    }

    /* HEADER FULL WIDTH */
    .main-header {
        background: #0A6847;
        padding: 25px 5%;
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        color: white;
    }
    .header-left { 
        display: flex; 
        align-items: center; 
        gap: 15px; 
    }
    .header-logo {
        background: rgba(255,255,255,0.2); 
        width: 45px; 
        height: 45px;
        border-radius: 50%; 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        font-size: 24px;
        flex-shrink: 0;
    }
    .header-title { font-size: 26px; font-weight: 700; margin: 0; line-height: 1.2; }
    .header-subtitle { font-size: 14px; color: rgba(255,255,255,0.8); margin: 0; }
    
    .header-right { text-align: right; }
    .status-badge {
        background: rgba(255,255,255,0.15); 
        padding: 6px 14px; 
        border-radius: 20px;
        font-size: 13px; 
        display: inline-flex; 
        align-items: center; 
        gap: 8px; 
        margin-bottom: 5px;
    }
    .dot-green { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 8px #4ade80; }
    .dot-red { width: 8px; height: 8px; background: #ef4444; border-radius: 50%; box-shadow: 0 0 8px #ef4444; }
    .header-date { font-size: 12px; color: rgba(255,255,255,0.7); }

    /* STATUS UTAMA */
    .status-container {
        padding: 40px 20px; 
        text-align: center; 
        background: #fafafa;
        margin: 20px 5%; 
        border-radius: 16px; 
        border: 1px solid #e2e8f0;
    }
    .check-circle {
        color: white; width: 75px; height: 75px; border-radius: 50%;
        display: inline-flex; justify-content: center; align-items: center;
        font-size: 38px; margin-bottom: 15px;
    }
    .status-text-main { font-size: 42px; font-weight: 800; margin: 0; letter-spacing: -1px; }
    .status-sub-main { color: #64748b; font-size: 16px; margin-top: 8px; }

    /* CONTENT WRAPPER AGAR ADA MARGIN DI KIRI KANAN */
    .content-wrapper {
        padding: 0 5%;
    }

    /* SUMMARY CARD */
    .summary-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 16px; display: flex; align-items: center; gap: 15px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        height: 100%;
    }
    .card-icon {
        background: #ecfdf5; color: #10b981; width: 45px; height: 45px;
        border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;
        flex-shrink: 0;
    }
    .card-title { font-size: 12px; color: #64748b; margin-bottom: 2px; }
    .card-value { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 2px; }
    .card-subtitle { font-size: 11px; color: #94a3b8; }

    /* BAGIAN SECTION */
    .custom-box {
        margin-top: 20px; 
        background: white; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #e2e8f0;
    }
    .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
    .section-title { font-size: 18px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .badge-update {
        background: #ecfdf5; color: #10b981; padding: 4px 12px; border-radius: 20px;
        font-size: 12px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;
    }

    /* TABLE RESPONSIVE */
    .table-container { overflow-x: auto; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; min-width: 600px; }
    .custom-table th { background: #f8fafc; color: #0A6847; font-weight: 600; padding: 12px 15px; border-bottom: 2px solid #e2e8f0; }
    .custom-table td { padding: 12px 15px; border-bottom: 1px solid #f1f5f9; color: #334155; }
    .pill-success { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 6px; font-weight: 500; font-size: 12px; }

    /* TOMBOL MENGAMBANG (FAB) */
    .st-key-fab_trigger { position: fixed; bottom: 30px; right: 30px; z-index: 9999; }
    .st-key-fab_trigger button {
        width: 60px; height: 60px; border-radius: 50%; background: #ef4444 !important;
        border: none !important; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4) !important; transition: transform 0.2s !important;
    }
    .st-key-fab_trigger button p { font-size: 24px !important; color: white !important; margin: 0 !important; }
    
    header[data-testid="stHeader"] { display: none; }
    footer { display: none; }

    /* ==================================================
       MEDIA QUERIES (KHUSUS UNTUK HP / LAYAR KECIL)
       ================================================== */
    @media (max-width: 768px) {
        .main-header {
            flex-direction: column;
            text-align: center;
            padding: 20px 15px;
            gap: 15px;
        }
        .header-left {
            flex-direction: column;
            gap: 10px;
        }
        .header-logo { width: 40px; height: 40px; font-size: 20px; }
        .header-title { font-size: 20px; }
        .header-subtitle { font-size: 12px; }
        .header-right { text-align: center; }
        
        .status-container { padding: 25px 15px; margin: 15px; }
        .check-circle { width: 60px; height: 60px; font-size: 30px; }
        .status-text-main { font-size: 28px; }
        .status-sub-main { font-size: 14px; }
        
        .section-header { flex-direction: column; align-items: flex-start; gap: 10px; }
        .custom-box { padding: 15px; margin-top: 15px; }
        .content-wrapper { padding: 0 15px; }
        
        div[data-testid="stVerticalBlock"] > div {
            gap: 10px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ==================================================
# RENDER UTAMA (DIPANGGIL OLEH DASHBOARD.PY)
# ==================================================
def render_dashboard(latest_data, chart_data, history_data, status_text, sensor_status, server_url):
    load_css()
    
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    is_flowing = "TIDAK" not in status_text.upper()
    is_online = "Online" in sensor_status

    main_color = "#10b981" if is_flowing else "#ef4444"
    main_bg = "#ecfdf5" if is_flowing else "#fef2f2"
    dot_class = "dot-green" if is_online else "dot-red"
    sensor_txt = "Terhubung" if is_online else "Terputus"
    
    # PERBAIKAN ZONA WAKTU KE WIB (Asia/Jakarta)
    tz_wib = pytz.timezone('Asia/Jakarta')
    waktu_sekarang = datetime.now(tz_wib).strftime("%d %b %Y - %H:%M:%S")

    # BUKA APP SHELL
    st.markdown('<div class="app-shell">', unsafe_allow_html=True)

    # 1. HEADER FULL WIDTH (Kiri ke Kanan)
    st.markdown(f"""
        <div class="main-header">
            <div class="header-left">
                <div class="header-logo">💧</div>
                <div>
                    <h1 class="header-title">Sistem Peringatan Dini Air</h1>
                    <p class="header-subtitle">Monitoring Distribusi Air Berbasis IoT & Machine Learning</p>
                </div>
            </div>
            <div class="header-right">
                <div class="status-badge"><span class="{dot_class}"></span> {sensor_txt}</div>
                <div class="header-date">{waktu_sekarang}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. STATUS UTAMA
    status_icon = "✓" if is_flowing else "✕"
    status_title = "AIR MENGALIR" if is_flowing else "AIR TIDAK MENGALIR"
    status_subtitle = "Sistem dalam kondisi normal" if is_flowing else "Distribusi air sedang terhenti/gangguan"
    
    st.markdown(f"""
        <div class="status-container">
            <div class="check-circle" style="background: {main_color}; box-shadow: 0 4px 15px {main_color}40;">{status_icon}</div>
            <h2 class="status-text-main" style="color: {main_color};">{status_title}</h2>
            <p class="status-sub-main">{status_subtitle}</p>
        </div>
    """, unsafe_allow_html=True)

    # BUKA CONTENT WRAPPER (Agar konten di bawahnya memiliki jarak tepi yang rapi)
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

    # 3. 4 RINGKASAN UTAMA
    c1, c2, c3, c4 = st.columns(4)
    
    waktu_deteksi = latest_data.get("time", "-")
    kedatangan_terakhir = latest_data.get("last_water_time", "-")
    durasi_terakhir = latest_data.get("duration", "-")

    with c1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-icon" style="color: {main_color}; background: {main_bg};">📶</div>
            <div>
                <div class="card-title">Status Sensor</div>
                <div class="card-value" style="color: {main_color};">{sensor_txt}</div>
                <div class="card-subtitle">{"Koneksi stabil" if is_online else "Periksa alat"}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-icon">🕒</div>
            <div>
                <div class="card-title">Waktu Deteksi</div>
                <div class="card-value">{waktu_deteksi.split(' ')[1] if ' ' in waktu_deteksi else waktu_deteksi}</div>
                <div class="card-subtitle">{waktu_deteksi.split(' ')[0] if ' ' in waktu_deteksi else '-'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div class="summary-card">
            <div class="card-icon">💧</div>
            <div>
                <div class="card-title">Kedatangan Terakhir</div>
                <div class="card-value">{kedatangan_terakhir.split(' ')[1] if ' ' in kedatangan_terakhir else kedatangan_terakhir}</div>
                <div class="card-subtitle">{kedatangan_terakhir.split(' ')[0] if ' ' in kedatangan_terakhir else '-'}</div>
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

    # 4. GRAFIK REALTIME DINAMIS
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
            x=x_axis, y=y_axis, 
            mode='lines+markers',
            line=dict(color='#10b981', width=3),
            marker=dict(size=6, color='white', line=dict(width=2, color='#10b981')),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
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

    # 5. TABEL RIWAYAT DINAMIS
    st.markdown("""
        <div class="custom-box" style="margin-bottom: 25px;">
            <div class="section-title" style="margin-bottom: 15px;">📋 Riwayat Distribusi</div>
            <div class="table-container">
                <table class="custom-table">
                    <thead>
                        <tr>
                            <th>No</th>
                            <th>Waktu Deteksi</th>
                            <th>Kedatangan Air</th>
                            <th>Durasi</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
    """, unsafe_allow_html=True)

    history_df = pd.DataFrame(history_data)
    if not history_df.empty:
        for i, row in history_df.head(5).iterrows(): 
            w_deteksi = row.get("time", "-")
            w_kedatangan = row.get("last_water_time", w_deteksi)
            w_durasi = row.get("duration", "-")
            w_status = "Selesai"
            
            st.markdown(f"""
                <tr>
                    <td>{i+1}</td>
                    <td>{w_deteksi}</td>
                    <td>{w_kedatangan}</td>
                    <td>{w_durasi}</td>
                    <td><span class="pill-success">{w_status}</span></td>
                </tr>
            """, unsafe_allow_html=True)
    else:
         st.markdown("<tr><td colspan='5' style='text-align:center;'>Belum ada riwayat distribusi</td></tr>", unsafe_allow_html=True)

    st.markdown("""
                    </tbody>
                </table>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; color: #94a3b8; font-size: 12px; margin-bottom: 30px;">
        <span style="font-size: 16px; color: #10b981;">🛡️</span> 
        <div>
            © 2026 Sistem Peringatan Dini Kedatangan Air Distribusi<br>
            Powered by IoT & Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True) # TUTUP CONTENT WRAPPER
    st.markdown("</div>", unsafe_allow_html=True) # TUTUP APP SHELL

    # 6. FAB BUTTON (GANGGUAN)
    if st.button("🔔", key="fab_trigger", help="Kirim Peringatan Gangguan"):
        st.session_state.show_popup = True

    # 7. POPUP OPERATOR
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
