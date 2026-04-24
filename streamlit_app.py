import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# 1. Page Config & Auto-Refresh (Live every 60 seconds)
st.set_page_config(layout="wide", page_title="NSE Sectorial Grid")
st_autorefresh(interval=60000, key="datarefresh")

# 2. Sector Definitions (NSE Tickers)
sectors = {
    "Banking": "^NSEBANK",
    "IT": "^CNXIT",
    "Auto": "NIFTY_AUTO.NS",
    "Metal": "NIFTY_METAL.NS",
    "Pharma": "NIFTY_PHARMA.NS",
    "Realty": "NIFTY_REALTY.NS"
}

def get_mini_chart(ticker):
    df = yf.download(ticker, period="1mo", interval="1d", progress=False)
    fig = go.Figure(data=[go.Scatter(x=df.index, y=df['Close'], line=dict(color='#00ff00', width=2))])
    fig.update_layout(height=150, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_visible=False, template="plotly_dark")
    return fig, df

# 3. Main UI Grid
st.title("🇮🇳 Live Indian Market Sectorial Board")
cols = st.columns(3) # Creates 3 columns

for i, (name, ticker) in enumerate(sectors.items()):
    with cols[i % 3]: # Cycles through columns
        with st.container(border=True):
            st.subheader(f"📊 {name}")
            fig, data = get_mini_chart(ticker)
            
            # Calculations
            curr = data['Close'].iloc[-1]
            prev_wk = data['Close'].iloc[-5]
            chg = ((curr - prev_wk)/prev_wk)*100
            
            # Header Stats
            c1, c2 = st.columns(2)
            c1.metric("Price", f"₹{curr:,.0f}")
            c2.metric("Wk %", f"{chg:.2f}%", delta=f"{chg:.2f}%")
            
            # Interactive Chart
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            # Potential Upside & Breakout
            high_52w = data['High'].max()
            upside = ((high_52w - curr)/curr)*100
            st.caption(f"🚀 Potential Upside: **{upside:.1f}%** to 52W High")
            
            if curr > data['Close'].rolling(20).mean().iloc[-1]:
                st.success("Trend: Bullish Breakout")
            else:
                st.warning("Trend: Consolidating")
