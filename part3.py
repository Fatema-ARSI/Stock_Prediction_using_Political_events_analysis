import streamlit as st
import numpy as np
import pandas as pd
import datetime

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import plotly.graph_objects as go

#import yahoo_fin.stock_info as si
#import yfinance as yf
from get_data import get_self_made_data_frame
from get_predictions import get_predictions



#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class portfolio_optimization(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):


        ######################################################
        
        
        st.write(' ## Portfolio Optimization ')
        
        
        ## SIDEBAR SECTION

        #sidebar section
        st.sidebar.header('User Input Features')
        #tickers=si.tickers_sp500()
        tickers=["AAPL","ABNB","AMZN","GOOG","INTC","MSFT","NVDA","SBUX","TSLA"]
        Amount=st.sidebar.number_input('Put your investment amount here',2000)
        selected_stock=st.sidebar.multiselect('Select Stock (Maximum 5)',tickers,["INTC","AAPL","NVDA","MSFT","TSLA"])
        selected_start_date='2014-01-02'
        selected_end_date='2022-01-01'
        

        ####################################################

        #Store the predicted stocks data into the data frame
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
        
        df_forecast1=get_predictions(df1)
        df_forecast2=get_predictions(df2)
        df_forecast3=get_predictions(df3)
        df_forecast4=get_predictions(df4)
        df_forecast5=get_predictions(df5)
        
        df=pd.DataFrame(df_forecast1['Date'])
        df[selected_stock[0]]=df_forecast1['Prediction']
        df[selected_stock[1]]=df_forecast2['Prediction']
        df[selected_stock[2]]=df_forecast3['Prediction']
        df[selected_stock[3]]=df_forecast4['Prediction']
        df[selected_stock[4]]=df_forecast5['Prediction']
        
        
        st.write('- Frontier Efficient theory by Professor Henry for portfolio optimization justifies that from the given set of portfolios with same rate of risk, investor will choose one with higher return.')
        
        st.write(' - This model creates the best fitted portfolio set for the given risk rate to increase the return by allocating the number of shares of non-correlated shares (for diversification of portfolio) for given capital amount. Allocation for given stocks and amount are as follows:')
        
        df.set_index('Date',inplace=True)
        #assign equivalent weights to each stock within the portfolio
        length=len(df)
        st.write(df)

                                 
        
