import streamlit as st
import pandas as pd
import requests

# ==================================================
# CSS PROFESSIONAL & MINIMALIST
# ==================================================
def load_css():
    st.markdown("""
    <style>
    /* Mengubah font bawaan menjadi lebih rapi dan bersih */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Menyembunyikan elemen bawaan Streamlit agar terasa seperti Web App asli */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Background Aplikasi */
    .stApp {
        background-color: #F8FAFC;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* HEADER CORPORATE */
    .top-header {
        background-color: #0F172A; /* Slate Dark */
        padding: 24px 30px;
        border-radius: 8px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .top-title {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }

    .top-subtitle {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 400;
    }

    /* SECTION TITLE */
    .section-title {
        color: #334155;
        font-size: 18px;
        font-weight: 600;
        padding-bottom: 8px;
        border-bottom: 2px solid #E2E8F0;
        margin-top: 32px;
        margin-bottom: 16px;
    }

    /* CONTAINER CARD */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        display: flex;
        flex-direction: column;
        height: 100%;
        justify-content: space-between;
    }

    /* METRIC COMPONENT */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #F1F5F9;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
    }

    /* METRIC LABEL */
    [data-testid="stMetricLabel"] {
        color: #64748B;
        font-weight: 500;
        font-size: 13px !important;
    }

    /* METRIC VALUE */
    [data-testid="stMetricValue"] {
        color: #0F172A;
        font-weight: 700;
        font-size: 24px !important;
    }

    /* DATAFRAME */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        overflow: hidden;
    }

    /* CHART */
    div[data-testid="stVegaLiteChart"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    /* BUTTON ACTION */
    .stButton > button {
        background-color: #DC2626; /* Danger Red */
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        font-size: 14px;
        padding: 10px 16px;
        transition: background-color 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #B91C1C;
        color: white;
    }

    /* CUSTOM FOOTER */
    .custom-footer {
        text-align: center;
        color: #94A3B8;
        margin-top: 48px;
        font-size: 13px;
        font-weight: 400;
    }

    /* ALERT BANNER */
    .alert-banner {
        text-align: center; 
        background-color: #FFFFFF; 
        padding: 16px; 
        border-radius: 8px; 
        margin-bottom: 24px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    /* RESPONSIVE MOBILE */
    @media (max-width: 768px) {
        .top-header { padding: 20px; }
        .top-title { font-size: 22px; }
        .alert-banner h2 { font-size: 20px !important; }
        [data-testid="stMetricValue"] { font-size: 20px !important; }
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
        <div class="top-title">Water Distribution Early Warning System</div>
        <div class="top-subtitle">IoT & Machine Learning Monitoring Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    # ==================================================
    # BANNER STATUS UTAMA
    # ==================================================
    is_not_flowing = "TIDAK" in status_text.upper()
    color_status = "#DC2626" if is_not_flowing else "#059669" # Red or Emerald
    border_left = f"4px solid {color_status}"
    
    # Menggunakan status_text dari data asli (sudah memuat emoji merah dari data)
    st.markdown(f"""
    <div class="alert-banner" style="border-left: {border_left};">
        <h2 style="color: {color_status}; margin: 0; font-weight: 700; font-size: 24px; letter-spacing: 0.5px;">
            {status_text.
