# Use `pip install -r requirements.txt` command in shell. Alternatively `pip3 install -r requirements.txt` can also be used.
import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

import functions as uf

### Streamlit App
image = Image.open('title03.png')
st.set_page_config(page_title = "Stock Data Analysis", page_icon="favicon.ico", layout = "wide")
# st.title(f"Trading")
st.image(image)

st.divider()
#selected_strategy = st.sidebar.selectbox("Select Strategy", ["Coiled Spring NR7", "Finger Finder", "Power Spike"])
selected_strategy = st.sidebar.selectbox("Select Strategy", ["SP500"])
start = st.sidebar.date_input("Enter the start date (YYYY-MM-DD): ")
end = st.sidebar.date_input("Enter the end date (YYYY-MM-DD): ")

welcome_statement = """This web app is designed to fetch all the S&P 500 stock data detect the ones that has NR7 and plot the same"""
st.write(welcome_statement)

if st.sidebar.button("Run Strategy"):
    tab1, tab2 = st.tabs(["Tabular", "Plots"])
    with tab1:
        with st.status("Operation in progress. Please wait."):
            ## Data Download
            st.write("Getting tickers (1/7)")
            # Fetch S&P 500 tickers
            sp500_tickers = uf.fetch_sp500_stocks()
            st.write(f'Gathering data from {start_date} to {current_date} (2/7)')
            for ticker in sp500_tickers:
                df = uf.get_stock_data(ticker, start, end)
                 # Find stocks with NR7 pattern
                nr7_stocks = uf.find_nr7_stocks(sp500_tickers,df)
                print(f"Stocks with NR7 pattern as of {datetime.now().date()}: {nr7_stocks}")
  
    with tab2:
        st.write("This section displays the buy/sell for the stocks with profitable trades for the selected duration.")
    
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Add Bollinger Bands using the ta library
        #data = uf.add_bollinger_bands(df)
        uf.plot_NR7(df,nr7_days)
        
