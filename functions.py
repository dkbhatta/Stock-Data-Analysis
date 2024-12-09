## Functions.py

##Import the required libraries

import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.offline as pyo

from warnings import filterwarnings
from datetime import datetime
from ta import add_all_ta_features
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator


filterwarnings('ignore')



def fetch_sp500_stocks():
    """
    Fetches the list of S&P 500 companies from Wikipedia.

    Returns:
        list: List of S&P 500 ticker symbols.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_table = pd.read_html(url)[0]
    return sp500_table['Symbol'].tolist()

def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)[['Open', 'High', 'Low', 'Close', 'Volume']]
    #data.columns = data.columns.droplevel(0)
    data['Ticker'] = ticker
    return data
    
def find_nr7_stocks(sp500_tickers, df):
    """
    Identifies S&P 500 stocks with an NR7 pattern as of the current date.

    Parameters:
        sp500_tickers (list): List of S&P 500 ticker symbols.
        df (pd.DataFrame): DataFrame containing stock data with columns ['Ticker', 'Date', 'High', 'Low'].

    Returns:
        list: List of tickers with NR7 patterns.
    """
    nr7_stocks = []

    for ticker in sp500_tickers:
        try:
            # Filter the data for the current ticker
            ticker_data = df[df['Ticker'] == ticker].sort_values('Date', ascending=False)
            
            # Ensure at least 7 days of data are available
            if len(ticker_data) < 7:
                continue
            
            # Check for NR7 pattern
            if detect_nr7(ticker_data.head(7)):
                nr7_stocks.append(ticker)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    return nr7_stocks

def detect_nr7(data):
    """
    Checks if the given 7-day stock data exhibits an NR7 pattern.

    Parameters:
        data (pd.DataFrame): DataFrame containing 7 rows with columns ['High', 'Low'].

    Returns:
        bool: True if NR7 pattern is detected, False otherwise.
    """
    ranges = data['High'] - data['Low']
    return ranges.iloc[-1] == ranges.min()

def plot_NR7(data, nr7_days):
    """
    Args:
        data: historical data for the stock (pandas DataFrame with Open, High, Low, Close columns)
        nr7_days: list of dates (datetime or string) where the narrowest range of 7 days was identified
    """
    # Ensure the index is a DatetimeIndex
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    # Convert nr7_days to datetime objects if they are strings
    nr7_days = [pd.Timestamp(day) for day in nr7_days]

    # Create a candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])

    # Add markers for NR7 days
    for day in nr7_days:
        if day in data.index:  # Ensure the day exists in the data
            fig.add_shape(
                type="line",
                x0=day,
                y0=data.loc[day]['Low'],
                x1=day,
                y1=data.loc[day]['High'],
                line=dict(color="Purple", width=4, dash="dot")
            )
    # Add Bollinger Bands
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Upper_BB"],
            line=dict(color="blue", width=1),
            name="Upper Bollinger Band"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Middle_BB"],
            line=dict(color="green", width=1, dash="dot"),
            name="Middle Bollinger Band"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Lower_BB"],
            line=dict(color="red", width=1),
            name="Lower Bollinger Band"
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Stock Price with NR7 Days Marked",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )
    # Update layout
    #fig.update_layout(title='Stock Price with NR7 Days Marked')
    #xaxis_rangeslider_visible=True

    # Show plot
    fig.show()

def add_bollinger_bands(df, price_col="Close", window=20, num_std_dev=2):
    """
    Adds Bollinger Bands to the DataFrame using the ta library.

    Parameters:
        df (pd.DataFrame): Input DataFrame with price data.
        price_col (str): Column name to calculate Bollinger Bands on. Default is "Close".
        window (int): Rolling window size for the moving average. Default is 20.
        num_std_dev (float): Number of standard deviations for the bands. Default is 2.

    Returns:
        pd.DataFrame: DataFrame with Bollinger Bands columns added.
    """
    # Initialize the BollingerBands object
    bb_indicator = BollingerBands(close=df[price_col], window=window, window_dev=num_std_dev)

    # Add Bollinger Bands to the DataFrame
    df['Upper_BB'] = bb_indicator.bollinger_hband()
    df['Lower_BB'] = bb_indicator.bollinger_lband()
    df['Middle_BB'] = bb_indicator.bollinger_mavg()

    return df


