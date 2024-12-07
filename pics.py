# Use `pip install -r requirements.txt` command in shell. Alternatively `pip3 install -r requirements.txt` can also be used.
import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import date
import time

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

import functions as uf

### Streamlit App
image = Image.open('title02.png')
st.set_page_config(page_title = "WQU Swing Trading", page_icon="favicon.ico", layout = "wide")
# st.title(f"Swing Trading")
st.image(image)

st.divider()
selected_strategy = st.sidebar.selectbox("Select Strategy", ["Coiled Spring NR7", "Finger Finder", "Power Spike"])

start = st.sidebar.date_input("Enter the start date (YYYY-MM-DD): ")
end = st.sidebar.date_input("Enter the end date (YYYY-MM-DD): ")

welcome_statement = """This web app is designed as a part of capstone at WorldQuant University. Please make sure that the start date is atleast 6 months from today. 
Emphasis will be on identifying optimal entry and exit points and following the simple rule of
achieving returns: minimizing risks and maximizing profits."""
st.write(welcome_statement)

if st.sidebar.button("Run Strategy"):
    tab1, tab2 = st.tabs(["Tabular", "Plots"])
    with tab1:
        with st.status("Operation in progress. Please wait."):
            ## Data Download
            st.write("Getting tickers (1/7)")
            # Fetch S&P 500 tickers
            sp500_tickers = fetch_sp500_stocks()

            st.write(f'Gathering data from {start_date} to {current_date} (2/7)')
            # Find stocks with NR7 pattern
            nr7_stocks = find_nr7_stocks(sp500_tickers,start,end)
            print(f"Stocks with NR7 pattern as of {datetime.now().date()}: {nr7_stocks}")
  
    with tab2:
        st.write("This section displays the buy/sell for the stocks with profitable trades for the selected duration.")
    
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Add Bollinger Bands using the ta library
        data = uf.add_bollinger_bands(data)
        uf.plot_NR7(data,nr7_days)
        
