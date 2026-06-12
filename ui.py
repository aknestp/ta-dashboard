import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime

# ==================================================
# CSS MODERN (PIXEL PERFECT)
# ==================================================
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"]  { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background-color: #f1f5f9; }
    
    .block-container {
        max-width: 1100px;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    .app-shell {
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        padding-bottom: 20px;
        margin-bottom: 20px;
        overflow: hidden;
    }

    .main-header {
        background: #0A6847;
        padding: 20px 30px;
        display: flex; justify-content: space-between; align-items: center; color: white;
    }
    .header-left { display: flex; align-items: center; gap: 15px; }
    .header-logo {
        background: rgba(255,255,255,0.2); width: 40px; height: 40px;
        border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 20px;
    }
    .header-title { font-size: 22px; font-weight: 700; margin: 0; line-height: 1.2; }
    .header-subtitle { font-size: 13px; color: rgba(255,255,255,0.8); margin: 0; }
    
    .header-right { text-align: right; }
    .status-badge {
        background: rgba(255,255,255,0.15); padding: 5px 12px; border-radius: 20px;
        font-size: 13px; display: inline-flex; align-items: center; gap: 8px; margin-bottom: 5px;
    }
    .dot-green { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 8px #4ade80; }
    .dot-red { width: 8px; height: 8px; background: #ef4444; border-radius: 50%; box-shadow: 0 0 8px #ef4444; }
    .header-date { font-size: 12px; color: rgba(255,255,255,0.7); }

    .status-container {
        padding: 30px; text-align: center; background: #fafafa;
        margin: 20px; border-radius: 12px; border: 1px solid #e2e8f0;
    }
    .check-circle {
        color: white; width: 65px; height: 65px; border-radius: 50%;
        display: inline-flex; justify-content: center; align-items: center;
        font-size: 32px; margin-bottom: 15px;
    }
    .status-text-main { font-size: 38px; font-weight: 800; margin: 0; letter-spacing: -0.5px; }
    .status-sub-main { color: #64748b; font-size: 15px; margin-top: 5px; }

    .summary-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 16px; display: flex; align-items: center; gap: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .card-icon {
        background: #ecfdf5; color: #10b981; width: 45px; height: 45px;
        border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;
    }
    .card-title { font-size: 12px; color: #64748b; margin-bottom: 2px; }
    .card-value { font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 2px; }
    .card-subtitle { font-size: 11px; color: #94a3b8; }

    .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
    .section-title { font-size: 18px; font-weight: 700; color: #1e293b; display: flex; align-items: center; gap: 8px; }
    .badge-update {
        background: #ecfdf5; color: #10b981; padding: 4px 12px; border-radius: 20px;
        font-size: 12px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;
    }

    .custom-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }
    .custom-table th { background: #f8fafc; color: #0A6847; font-weight: 600; padding: 12px 15px; border-bottom: 2px solid #e2e8f0; }
    .custom-table td { padding: 12px 15px; border-bottom: 1px solid #f1f5f9; color: #334155; }
    .pill-success { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 6px; font-weight: 500; font-size: 12px; }

    .st-key-fab_trigger { position: fixed; bottom: 40px; right: 40px; z-index: 9999; }
    .st-key-fab_trigger button {
        width: 65px; height: 65px; border-radius: 50%; background: #ef4444 !important;
        border: none !important; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4) !important; transition: transform 0.2s !important;
    }
    .st-key-fab_trigger button:hover { transform: scale(1.05) !important; }
    .st-key-fab_trigger button p { font-size: 26px !important; color: white !important; margin: 0 !important; }
    
    header[data-testid="stHeader"] { display: none; }
    footer { display: none; }
    </style>
    """, unsafe_allow_html=True)


# ==================================================
# RENDER UTAMA (DIPANGGIL OLEH DASHBOARD.PY)
# ==================================================
def render_dashboard(latest_data, chart_data, history_data, status_text, sensor_status, server_url):
    load_css()
    
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    # Deteksi kondisi berdasarkan status_text dan sensor_status dari dashboard.py
    is_flowing = "TIDAK" not in status_text.upper()
    is_online = "Online" in sensor_status

    # Set Warna Tema Dinamis
    main_color = "#10b981" if is_flowing else "#ef4444"
    main_bg = "#ecfdf5" if is_flowing else "#fef2f2"
    dot_class = "dot-green" if is_online else "dot-red"
    sensor_txt = "Terhubung" if is_online else "Terputus"
    waktu_sekarang = datetime.now().strftime("%d %b %Y - %H:%M:%S")

    # 1. HEADER
    st.markdown(f"""
    <div class="app-shell" style="padding: 0; margin-bottom: 0;">
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

    # 3. 4 RINGKASAN UTAMA
    st.markdown("<div style='padding: 0 20px;'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    # Ambil data dari dictionary latest_data (gunakan fallback "-" jika kosong)
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
        <div style="margin-top: 30px; background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
            <div class="section-header">
                <div class="section-title">📈 Grafik RMS Realtime</div>
                <div class="badge-update"><span class="dot-green" style="box-shadow: none; width:6px; height:6px;"></span> Update realtime</div>
            </div>
    """, unsafe_allow_html=True)

    # Proses chart_data menjadi DataFrame Plotly
    chart_df = pd.DataFrame(chart_data)
    
    if not chart_df.empty and "rms" in chart_df.columns:
        # Asumsikan kolom waktu bernama "time" atau "timestamp", jika tidak, ganti sesuai index backend Anda
        x_axis = chart_df["time"] if "time" in chart_df.columns else chart_df.index
        y_axis = chart_df["rms"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis, y=y_axis, 
            mode='lines+markers',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8, color='white', line=dict(width=2, color='#10b981')),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        fig.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(color='#94a3b8'), title="RMS", titlefont=dict(color='#64748b')),
            plot_bgcolor='white', paper_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("📊 Data grafik sedang disiapkan atau sensor belum mengirim data.")

    st.markdown("</div>", unsafe_allow_html=True)

    # 5. TABEL RIWAYAT DINAMIS
    st.markdown("""
        <div style="margin-top: 20px; background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
            <div class="section-title" style="margin-bottom: 15px;">📋 Riwayat Distribusi</div>
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
        # Render Baris Tabel Dinamis dari DataFrame
        # Sesuaikan dengan nama kunci (key) dari response /history JSON backend Anda
        for i, row in history_df.head(5).iterrows(): # Tampilkan 5 terakhir
            w_deteksi = row.get("time", "-")
            w_kedatangan = row.get("last_water_time", w_deteksi) # fallback
            w_durasi = row.get("duration", "-")
            w_status = "Selesai" # Jika tersimpan di riwayat diasumsikan siklus selesai
            
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
    </div> """, unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; color: #94a3b8; font-size: 12px; padding-left: 10px;">
        <span style="font-size: 16px; color: #10b981;">🛡️</span> 
        <div>
            © 2026 Sistem Peringatan Dini Kedatangan Air Distribusi<br>
            Powered by IoT & Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 6. FAB BUTTON (GANGGUAN)
    if st.button("🔔", key="fab_trigger", help="Kirim Peringatan Gangguan"):
        st.session_state.show_popup = True

    # 7. POPUP OPERATOR & FUNGSI REQUEST KE FLASK BACKEND
    if st.session_state.show_popup:
        @st.dialog("⚠️ Kirim Informasi Gangguan")
        def popup_operator():
            st.markdown("### Konfirmasi Operator\nInformasi ini akan dikirim ke grup WhatsApp warga.")
            password = st.text_input("Masukkan Password Operator", type="password")
            st.warning("Pesan yang akan dikirim:\n\nDistribusi air mengalami gangguan sementara.")

            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("Kirim Informasi ✅", use_container_width=True):
                    if password == "admin1": # Ganti dengan password yang sesungguhnya nanti
                        try:
                            # Melakukan POST ke Backend API berdasarkan URL yang dikirim dari dashboard.py
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
