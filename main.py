import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

from arctic import Arctic
from arctic.date import DateRange
from binance.client import Client

from dashboard_utils import get_tv_chart, get_pair_funding, get_funding_chart

# Load .env variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

# Tokens of interest
universe = ['BTC', 'ETH', 'SOL', 'APE', 'BNB', 'DOT', 
            'FTM', 'AAVE', 'GMT', 'ADA', 'AVAX', 'DOGE',
            'TRX', 'SHIB', 'MATIC', 'LTC', 'MANA', 'NEAR',
            'FTT', 'UNI', 'BCH', 'LINK', 'XMR', 'ALGO',
            'FLOW', 'HBAR', 'VET', 'CRV', 'CVX', 'SAND',
            'ALPHA', 'ETC', 'LRC', 'ZIL', 'ATOM', 'BAT',
            'GRT', 'HNT', 'KNC', 'NEO', 'THETA', 'EGLD',
            'COMP', 'ZEC', 'SCRT', 'XVG', 'ROSE', 'OMG',
            'REN', 'ONE', 'GALA', 'AXS','XLM','ICP',
            'FIL', 'MKR', 'RUNE', 'KSM', 'SNX', 'WAVES',
            'QTUM','1INCH','SCRT', 'AUDIO', 'ENS']

# Load Binance Client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

### APP GRAPHIC CONTENT ###
st.set_page_config(layout="wide")
st.markdown("""<style>footer {visibility: hidden;}</style>""", unsafe_allow_html=True) 

### Logo and Title ###
headcol1, headcol2 = st.columns([1, 10])
with headcol1:
    st.image('./src/logo.png', width=100)

with headcol2:
    st.title("Delta Foundry - Pair Trading Screener")

### Token Selection ###
tokenA_col, tokenB_col = st.columns([2,2])
with tokenA_col:
    tokenA = st.selectbox('Token A: ', universe, 1)
with tokenB_col:
    tokenB = st.selectbox('Token B: ', universe, 0)

### TradingView Charts ###
pair_chart = get_tv_chart(tokenA,tokenB)

tokenA_chart_col, tokenB_chart_col = st.columns([1,1])

with tokenA_chart_col:
    tokenA_chart = get_tv_chart(tokenA,'USDT')

with tokenB_chart_col:
    tokenA_chart = get_tv_chart(tokenB,'USDT')


### Funding Rates Chart ###
fundings = get_pair_funding(tokenA, tokenB, client)
funding_chart = get_funding_chart(fundings)
st.header('Monthly funding rates')
st.plotly_chart(funding_chart, use_container_width=True)

### Footer ###
st.markdown(
    '''
    <div style="text-align: center; margin-top:8%; margin-bottom:-90%; font-family: sans-serif">
        &#129302; Created by 
        <a href="https://twitter.com/0xD0C97" style="text-decoration:none">0xDOC97</a> 
        & 
        <a href="https://it.tradingview.com/u/Ray_Burst/" style="text-decoration:none">RayBurst</a> 
        &#129302;
    </div>
    ''',
    unsafe_allow_html=True)
