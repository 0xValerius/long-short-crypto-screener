"""
Dashboard Utility Functions

This module contains utility functions used by the main Streamlit dashboard script
to fetch funding rates, create TradingView chart widgets, and plot funding rate charts.

The following functions are included in this module:
- get_token_funding
- get_pair_funding
- get_funding_chart
- get_tv_chart

Author: 0xValerius
"""

from binance.client import Client
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

def get_token_funding(token, client):
    """
    Fetches the funding rates for the given token from the Binance API.

    Args:
        token (str): The token symbol for which to fetch funding rates.
        client (binance.Client): An instance of the Binance client.

    Returns:
        pandas.DataFrame: A DataFrame containing the funding rates for the given token.
    """

    fundingRates = client.futures_funding_rate(symbol=token+'USDT', limit=90)
    fundingRates = pd.DataFrame(fundingRates)
    fundingRates['fundingTime'] = fundingRates['fundingTime']/1000
    fundingRates['fundingTime'] = pd.to_datetime(fundingRates['fundingTime'].astype(int), unit='s')
    fundingRates['fundingTime'] = pd.to_datetime(fundingRates['fundingTime'])
    fundingRates = fundingRates.set_index("fundingTime")
    fundingRates['fundingRate'] = fundingRates['fundingRate'].astype(float)*100
    fundingRates.drop("symbol", axis=1, inplace=True)
    fundingRates.rename(columns={"fundingRate": token+'/USDT'}, inplace=True)
    return fundingRates

def get_pair_funding(tokenA, tokenB, client):
    """
    Fetches the funding rates for the given token pair from the Binance API.

    Args:
        tokenA (str): The first token symbol in the pair.
        tokenB (str): The second token symbol in the pair.
        client (binance.Client): An instance of the Binance client.

    Returns:
        pandas.DataFrame: A DataFrame containing the funding rates for the given token pair.
    """

    tokenA_funding = get_token_funding(tokenA, client)
    tokenB_funding = get_token_funding(tokenB, client)
    fundings = pd.concat([tokenA_funding, tokenB_funding], axis=1)
    fundings['LONG '+tokenA+'/'+tokenB] = fundings[tokenA+'/USDT'] - fundings[tokenB+'/USDT']
    return fundings

def get_funding_chart(fundings):
    """
    Creates a Plotly line chart for the given funding rates.

    Args:
        fundings (pandas.DataFrame): A DataFrame containing funding rates.

    Returns:
        plotly.graph_objects.Figure: A Plotly line chart for the given funding rates.
    """

    absMax = fundings.abs().max().max()*1.05
    fig = px.line(fundings,x=fundings.index, y=fundings.columns, markers=True)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#1e232c')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#1e232c', range=[-absMax, absMax])
    fig.update_layout(
        xaxis_title="<b>Time</b>",
        yaxis_title="<b>Funding Rate (%)</b>",
        legend_title="<b>Pairs</b>",
        plot_bgcolor = "#151923",
        font=dict(
            family="sans-serif",
            size=14,
            color='#f1f3f6'
            )
        )
    return fig


def get_tv_chart(tokenA, tokenB):
    """
    Creates a TradingView chart widget for the given token pair.

    Args:
        tokenA (str): The first token symbol in the pair.
        tokenB (str): The second token symbol in the pair.

    Returns:
        streamlit.components.html: A Streamlit component containing the TradingView chart widget.
    """

    if(tokenB != 'USDT'):
        chart = components.html(
        '''
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
            <div id="tradingview_ac9e6"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
                new TradingView.widget(
                {
                "width": '100%',
                "height": '800',
                "symbol": "BINANCE:'''+tokenA+'''USDT/BINANCE:'''+tokenB+'''USDT",
                "timezone": "exchange",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "withdateranges": true,
                "range": "12M",
                "hide_side_toolbar": false,
                "allow_symbol_change": false,
                "save_image": false,
                "watchlist": [
                    "BINANCE:'''+tokenA+'''USDT/BINANCE:BTCUSDT",
                    "BINANCE:'''+tokenB+'''USDT/BINANCE:BTCUSDT",
                    "BINANCE:BTCUSDT"
                ],
                "details": true,
                "studies": [
                    {
                        "id": "MAExp@tv-basicstudies",
                        "version": 60,
                        "inputs": {
                            "length": 11
                        }
                    },
                    {
                        "id": "MAExp@tv-basicstudies",
                        "version": 60,
                        "inputs": {
                            "length": 22
                        }
                    }
                ],
                "container_id": "tradingview_ac9e6"
                }
                );
            </script>
        </div>
        <!-- TradingView Widget END -->
        ''',
        height=810)

    else:
        chart = components.html(
        '''
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container">
            <div id="tradingview_ac9e6"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
                new TradingView.widget(
                {
                "width": '100%',
                "height": '800',
                "symbol": "BINANCE:'''+tokenA+'''USDT",
                "timezone": "exchange",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "withdateranges": true,
                "range": "12M",
                "hide_side_toolbar": false,
                "allow_symbol_change": false,
                "save_image": false,
                "container_id": "tradingview_ac9e6"
                }
                );
            </script>
        </div>
        <!-- TradingView Widget END -->
        ''',
        height=810)
    return chart



