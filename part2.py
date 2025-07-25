import streamlit as st
import numpy as np
#import yfinance as yf
#import yahoo_fin.stock_info as si
import pandas as pd
import datetime

import numpy as np

import pandas as pd
import datetime

import tensorflow as tf


from sklearn.preprocessing import StandardScaler
from pandas.core.reshape.merge import merge


import plotly.graph_objs as go
import plotly.io as pio
from plotly.offline import init_notebook_mode,iplot
from today_signal import today_signal
from get_data import get_self_made_data_frame
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
        tickers=["AAPL","ABNB","AMZN","GOOG","INTC","MSFT","NVDA","SBUX","TSLA"]
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


        col1,col2,col3=st.columns(3)
        col1.metric(selected_stock[0],tickers[0],"")
        col2.metric(selected_stock[1],tickers[1],"")
        col3.metric(selected_stock[2],tickers[2],"")
        col1,col2=st.columns(2)
        col1.metric(selected_stock[3],tickers[3],"")
        #col2.metric(selected_stock[4],tickers[4],"")

        ########data download#################################################
        #get stock value
        df1 = get_self_made_data_frame(selected_stock[0],selected_start_date,selected_end_date)
        df1.reset_index(inplace=True)

        df2 = get_self_made_data_frame(selected_stock[1],selected_start_date,selected_end_date)
        df2.reset_index(inplace=True)

        df3 = get_self_made_data_frame(selected_stock[2],selected_start_date,selected_end_date)
        df3.reset_index(inplace=True)

        df4 = get_self_made_data_frame(selected_stock[3],selected_start_date,selected_end_date)
        df4.reset_index(inplace=True)

        df5 = get_self_made_data_frame(selected_stock[4],selected_start_date,selected_end_date)
        df5.reset_index(inplace=True)
        cols=list(df1)[1:11]
        df_for_training=df1[cols].astype(float)
        train_dates=pd.to_datetime(df1['Date'])

        scaler=StandardScaler()
        scaler=scaler.fit(df_for_training)
        df_for_training_scaled=scaler.transform(df_for_training)
        
        st.write(df_for_training_scaled)

        #################################################################




        
