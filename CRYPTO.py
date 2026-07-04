import streamlit as st
import pandas as pd
import requests
import asyncio
import aiohttp
from streamlit_autorefresh import st_autorefresh

# 1. Page Configuration & Auto-Refresh
st.set_page_config(page_title="THEFXEMPIRE // CRYPTO TRACKER", layout="wide", initial_sidebar_state="expanded")
st_autorefresh(interval=10000, limit=10000, key="ultimate_tracker_cycle")

# 2. Injecting Visual Theme Framework matching 1000028629.jpg
st.markdown("""
    <style>
        /* Global Background Layout overrides */
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #060B13 0%, #0A192F 50%, #051B2C 100%) !important;
            background-attachment: fixed !important;
            color: #E2E8F0 !important;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Shifting Main Block Padding up to position header at the absolute top */
        [data-testid="stMainBlockContainer"] {
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }
        
        [data-testid="stHeader"] {
            background: rgba(11, 19, 36, 0.5) !important;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 245, 255, 0.1);
        }
        
        /* Absolute Top Centered Logo & Brand Header Layout */
        .brand-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 25px;
            width: 100%;
        }
        .brand-logo {
            width: 55px;
            height: 55px;
            margin-bottom: -5px;
            filter: drop-shadow(0 0 12px #00F5FF);
        }
        .brand-header {
            text-align: center;
            font-size: 38px;
            font-weight: 900;
            color: #00F5FF;
            letter-spacing: 4px;
            text-transform: uppercase;
            text-shadow: 0 0 20px rgba(0, 245, 255, 0.4), 0 0 40px rgba(0, 245, 255, 0.1);
            font-family: 'Montserrat', -apple-system, sans-serif;
        }
        
        /* Target Row Matrix Cards matching 1000028629.jpg */
        .theater-card {
            background: rgba(15, 27, 46, 0.4);
            border: 1px solid rgba(0, 245, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            min-height: 120px;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .theater-label {
            font-size: 10px;
            color: #64748B;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .theater-value {
            font-size: 24px;
            font-weight: 800;
            color: #FFFFFF;
            font-family: monospace;
        }
        .section-title {
            text-align: center;
            font-size: 13px;
            color: #94A3B8;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 25px;
            margin-bottom: 25px;
            font-weight: 600;
        }
        
        /* Cyan Radar Node UI Frame */
        .target-circle {
            border: 3px solid #00F5FF;
            border-radius: 50%;
            width: 320px;
            height: 320px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: radial-gradient(circle, rgba(0,245,255,0.05) 0%, rgba(0,0,0,0) 70%);
            box-shadow: 0 0 30px rgba(0, 245, 255, 0.15), inset 0 0 30px rgba(0, 245, 255, 0.1);
        }
        .timeframe-dots {
            display: flex;
            gap: 10px;
            font-size: 9px;
            font-weight: bold;
            color: #94A3B8;
            margin-bottom: 15px;
            font-family: monospace;
        }
        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            align-self: center;
        }
        .dot-green { background-color: #00FF66; box-shadow: 0 0 8px #00FF66; }
        .dot-red { background-color: #FF4560; box-shadow: 0 0 8px #FF4560; }
        .target-asset {
            font-size: 38px;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .target-liquidity {
            font-size: 11px;
            font-weight: 800;
            color: #00F5FF;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .target-index { font-size: 10px; color: #64748B; letter-spacing: 1px; }

        /* Calculation Card Module Layout */
        .sizer-container {
            background: rgba(10, 25, 47, 0.4);
            border: 1px solid rgba(0, 245, 255, 0.15);
            border-radius: 12px;
            padding: 24px;
            backdrop-filter: blur(12px);
            margin-top: 15px;
        }
        .sizer-header {
            font-size: 14px;
            font-weight: 800;
            color: #00F5FF;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-bottom: 15px;
            border-bottom: 1px solid rgba(0, 245, 255, 0.1);
            padding-bottom: 8px;
        }
        .sizer-metric-box {
            background: rgba(6, 11, 19, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 12px;
            text-align: center;
        }

        /* Transparent Embedded Table styles */
        div[data-testid="stDataFrame"], div[data-testid="stDataFrame"] > div, div[data-testid="stDataFrame"] iframe {
            background-color: transparent !important; background: transparent !important;
        }
        div[data-testid="stDataFrame"] [data-testid="StyledDataTable"] {
            background-color: transparent !important; border: none !important;
        }
        div[data-testid="stDataFrame"] th {
            background-color: rgba(16, 28, 48, 0.6) !important;
            color: #00F5FF !important; font-size: 11px !important; text-transform: uppercase !important;
            letter-spacing: 1px !important; border-bottom: 1px solid rgba(0, 245, 255, 0.2) !important;
        }
        div[data-testid="stDataFrame"] td {
            background-color: transparent !important; border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            font-size: 12px !important; color: #E2E8F0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Absolute Top Header with Custom Vector Node Logo
# 3. Absolute Top Header with Custom Vector Node Logo
st.markdown("""
    <div class="brand-container">
        <svg class="brand-logo" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#00F5FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="#00F5FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div class="brand-header">THEFXEMPIRE CRYPTO TRACKER</div>
    </div>
""", unsafe_allow_html=True)