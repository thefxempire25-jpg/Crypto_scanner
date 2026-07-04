import streamlit as st
import pandas as pd
import requests
import asyncio
import aiohttp
from streamlit_autorefresh  import st_autorefresh

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
        <div class="brand-header">THEFXEMPIRE CRYPTO SCANNER</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# GLOBAL CONSTANTS & CONFIGURATION
# ==============================================================================
SCAN_TARGETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "LINKUSDT", "EURUSDT", "JPYUSDT"]

# 4. Multi-Timeframe Async Fetching Engine
async def fetch_klines(session, symbol, interval, limit=125):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        async with session.get(url, timeout=4) as response:
            if response.status == 200:
                return await response.json()
    except:
        pass
    return None

async def generate_comprehensive_matrix():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in SCAN_TARGETS:
            tasks.append((symbol, "15m", fetch_klines(session, symbol, "15m", limit=3)))
            tasks.append((symbol, "1h", fetch_klines(session, symbol, "1h", limit=3)))
            tasks.append((symbol, "4h", fetch_klines(session, symbol, "4h", limit=3)))
            tasks.append((symbol, "1w", fetch_klines(session, symbol, "1w", limit=3)))
            tasks.append((symbol, "1M", fetch_klines(session, symbol, "1M", limit=125)))
            
        raw_responses = await asyncio.gather(*[t[2] for t in tasks])
        matrix = {s: {} for s in SCAN_TARGETS}
        
        for idx, (symbol, interval, _) in enumerate(tasks):
            data = raw_responses[idx]
            if not data or len(data) < 2:
                continue
                
            closes = [float(candle[4]) for candle in data]
            current_price = closes[-1]
            matrix[symbol]["Price"] = current_price
            
            if interval == "15m":
                matrix[symbol]["15M"] = "BULLISH" if closes[-1] >= closes[-2] else "BEARISH"
            elif interval == "1h":
                matrix[symbol]["1H"] = "BULLISH" if closes[-1] >= closes[-2] else "BEARISH"
            elif interval == "4h":
                matrix[symbol]["4H"] = "BULLISH" if closes[-1] >= closes[-2] else "BEARISH"
            elif interval == "1w":
                matrix[symbol]["Weekly"] = "BULLISH" if closes[-1] >= closes[-2] else "BEARISH"
            elif interval == "1M":
                matrix[symbol]["Monthly"] = "BULLISH" if closes[-1] >= closes[-2] else "BEARISH"
                matrix[symbol]["Yearly"] = "BULLISH" if closes[-1] >= (closes[-13] if len(closes) >= 13 else closes[0]) else "BEARISH"
                matrix[symbol]["5-Year"] = "BULLISH" if closes[-1] >= (closes[-61] if len(closes) >= 61 else closes[0]) else "BEARISH"
                matrix[symbol]["10-Year"] = "BULLISH" if closes[-1] >= (closes[-121] if len(closes) >= 121 else closes[0]) else "BEARISH"
                
        return matrix

# Run execution thread loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
master_matrix = loop.run_until_complete(generate_comprehensive_matrix())

# 5. Top Metric Row Grid Cards (Directly matching 1000028629.jpg)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="theater-card"><div class="theater-label">Total Monitored</div><div class="theater-value">{len(SCAN_TARGETS)} Assets</div></div>', unsafe_allow_html=True)
with c2:
    active_surgeries = 0
    top_aligned_asset = SCAN_TARGETS[0]
    highest_score = 0
    
    for symbol, tfs in master_matrix.items():
        directions = [tfs.get("15M"), tfs.get("1H"), tfs.get("4H"), tfs.get("Monthly")]
        directions = [d for d in directions if d is not None]
        if not directions: continue
        
        score = max(directions.count("BULLISH"), directions.count("BEARISH"))
        if score == len(directions):
            active_surgeries += 1
        if score > highest_score:
            highest_score = score
            top_aligned_asset = symbol

    st.markdown(f'<div class="theater-card"><div class="theater-label">Active Surgeries</div><div class="theater-value" style="color: #00F5FF;">{active_surgeries} Live</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="theater-card"><div class="theater-label">Risk Protocol</div><div class="theater-value" style="color: #E2E8F0;">0.3% - 0.6%</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">— FULL-SPECTRUM OPERATING THEATER —</div>', unsafe_allow_html=True)

# 6. Central Panel Split Layout
left_panel, right_panel = st.columns([1, 1.4], gap="large")

with left_panel:
    # Circular Visual Target Node
    t_data = master_matrix.get(top_aligned_asset, {})
    
    def render_dot_element(state):
        if state == "BULLISH": return '<span class="dot dot-green"></span>'
        if state == "BEARISH": return '<span class="dot dot-red"></span>'
        return '<span class="dot" style="background-color:#475569;"></span>'

    dot_15m = render_dot_element(t_data.get("15M"))
    dot_1h = render_dot_element(t_data.get("1H"))
    dot_4h = render_dot_element(t_data.get("4H"))
    dot_m = render_dot_element(t_data.get("Monthly"))
    dot_12m = render_dot_element(t_data.get("Yearly"))
    
    is_bullish = t_data.get("1H") == "BULLISH"
    liquidity_msg = "⚡ BUY LIQUIDITY REQUIRED" if is_bullish else "⚡ SELL LIQUIDITY REQUIRED"
    index_rating = 124.5 if is_bullish else 76.2

    st.markdown(f"""
        <div class="target-circle">
            <div class="timeframe-dots">
                12M {dot_12m} &nbsp; 1M {dot_m} &nbsp; 4H {dot_4h} &nbsp; 1H {dot_1h} &nbsp; 15M {dot_15m}
            </div>
            <div class="target-asset">{top_aligned_asset[:3]}/{top_aligned_asset[3:]}</div>
            <div class="target-liquidity">{liquidity_msg}</div>
            <div class="target-index">Activity Index: {index_rating}% 🔥</div>
        </div>
    """, unsafe_allow_html=True)

with right_panel:
    # Glassmorphic Integrated Position Sizer Panel
    st.markdown('<div class="sizer-container">', unsafe_allow_html=True)
    st.markdown('<div class="sizer-header">🧮 SURGICAL POSITION SIZER</div>', unsafe_allow_html=True)
    
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        account_balance = st.number_input("Account Balance ($)", min_value=100.0, value=10000.0, step=500.0)
    with sc2:
        risk_percentage = st.slider("Risk Protocol (%)", min_value=0.3, max_value=0.6, value=0.5, step=0.05)
    with sc3:
        selected_asset = st.selectbox("Execution Target Asset", SCAN_TARGETS)
        
    live_price = master_matrix.get(selected_asset, {}).get("Price", 1.0)
    risk_amount = account_balance * (risk_percentage / 100.0)
    
    sc4, sc5 = st.columns(2)
    with sc4:
        sl_type = st.radio("Stop Loss Metric Type", ["Percentage Distance", "Fixed Price Value"])
    with sc5:
        if sl_type == "Percentage Distance":
            sl_pct = st.number_input("Stop Loss Distance (%)", min_value=0.05, max_value=5.0, value=0.5, step=0.05)
            sl_distance = live_price * (sl_pct / 100.0)
        else:
            target_sl_price = st.number_input("Target Stop Loss Price Level", min_value=0.0, value=live_price * 0.99)
            sl_distance = abs(live_price - target_sl_price)

    if sl_distance > 0:
        calculated_position_units = risk_amount / sl_distance
        notional_value = calculated_position_units * live_price
        
        st.markdown("<br>", unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            st.markdown(f'<div class="sizer-metric-box"><div class="theater-label">Risk Capital</div><div class="theater-value" style="color:#FF4560;">${risk_amount:.2f}</div></div>', unsafe_allow_html=True)
        with rc2:
            st.markdown(f'<div class="sizer-metric-box"><div class="theater-label">Contract Units</div><div class="theater-value" style="color:#00F5FF;">{calculated_position_units:,.3f}</div></div>', unsafe_allow_html=True)
        with rc3:
            st.markdown(f'<div class="sizer-metric-box"><div class="theater-label">Notional Size</div><div class="theater-value">${notional_value:,.2f}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Comprehensive Grid Matrix Table
    st.markdown("<br>##### 🔍 TIMEFRAME DIRECTION MATRIX", unsafe_allow_html=True)
    table_records = []
    for symbol in SCAN_TARGETS:
        m_data = master_matrix.get(symbol, {})
        table_records.append({
            "Asset Cross": f"🪐 {symbol}",
            "15M": m_data.get("15M", "FETCHING"),
            "1H": m_data.get("1H", "FETCHING"),
            "4H": m_data.get("4H", "FETCHING"),
            "Monthly": m_data.get("Monthly", "FETCHING"),
            "Yearly (12M)": m_data.get("Yearly", "FETCHING"),
            "10-Year": m_data.get("10-Year", "FETCHING"),
        })
        
    st.dataframe(pd.DataFrame(table_records), use_container_width=True, hide_index=True)
