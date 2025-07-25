import streamlit as st
import numpy as np
#import yfinance as yf
#import yahoo_fin.stock_info as si
import pandas as pd
import datetime
import math

import plotly.graph_objs as go
import plotly.io as pio
from plotly.offline import init_notebook_mode,iplot
from today_signal import today_signal
#from get_data import get_self_made_data_frame
#from get_predictions import get_predictions
#from get_plot_data import get_plot_data1, get_plot_data2
###import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class stock_prediction(HydraHeadApp):
    #wrap all your code in this method and you should be done
    def run(self):
        ##############################################################
        
        
        
        st.write(' ## Stock Price Prediction Model ')
        
        ###SIDEBAR section
        st.sidebar.header('User Input Features')
        #tickers=si.tickers_sp500()
        tickers=["INTC","AAPL","NVDA","MSFT","TSLA"]
        selected_stock=st.sidebar.multiselect('Select Stocks (Maximum 5)',tickers,["INTC","AAPL","NVDA","MSFT","TSLA"])
        selected_start_date='2014-01-02'
        selected_end_date='2022-01-01'
        num_company=st.sidebar.slider('Number of Stock Prediction To Show',1,5,2)

####################################################
        ##today signals
        signal_data=today_signal(selected_stock)
        tickers=[]
        for i in signal_data:
            if i==0.0:
                tickers.append('HOLD')
            elif i==1.0:
                tickers.append('HOLD')
            else :
                tickers.append('SELL')
                
                
                
        st.write(" ##### Signal Indicator as of " + datetime.datetime.today().strftime('%Y-%m-%d') + " for selected stocks." )
        st.write("")
        st.write("")
        st.write("")
        st.write("")


        st.write(signal_data)
