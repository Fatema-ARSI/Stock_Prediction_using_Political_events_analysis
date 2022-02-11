import streamlit as st
import numpy as np
import pandas as pd
import datetime

import yfinance as yf
import yahoo_fin.stock_info as si

import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats


## To use sklearn for linear regression
from sklearn.linear_model import LinearRegression

#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class regression_analysis(HydraHeadApp):
    
    #wrap all your code in this method and you should be done
    
    def run(self):

        ############################################ main code ###############################################



        #sidebar section
        st.sidebar.header('User Input Features')
        tickers=si.tickers_sp500()
        selected_stock=st.sidebar.selectbox('Select Stock',tickers)
        selected_start_date=st.sidebar.date_input('Select Start Date',datetime.date(2019,7,6))
        selected_end_date=st.sidebar.date_input('Select Start Date',datetime.date(2020,7,6))

        ####################################################
        ## Fetch data from yfinance

        ticker_df = yf.download(selected_stock, start = selected_start_date, end = selected_end_date)
        index_df = yf.download("SPY", start = selected_start_date, end = selected_end_date)


        ####################################################
        
        #st.write(
            
            " - This page showcase the Regression analysis performed for " + str(selected_stock) + " and stock market index S&P 500 returns to determine the relationship between " +  str(selected_stock) + "’s daily returns and market index."
        )
        
        ##Metrics Alpha Beta
        ticker_df['daily_ret'] = ticker_df['Close'].pct_change(1)
        index_df['daily_ret'] = index_df['Close'].pct_change(1)

        LR = stats.linregress(ticker_df['daily_ret'].iloc[1:],index_df['daily_ret'].iloc[1:])
        beta,alpha,r_val,p_val,std_err = LR
        
        
        
        alpha_result=[]
        if alpha<0:
            alpha_result='badly'
        elif alpha>0:
            alpha_result='well'
        else:
            alpha_result='same as'
            
        beta_result=[]
        if beta>0.5:
            beta_result='positively correlated with'
        elif beta<0:
            beta_result='negatively correlated with'
        elif beta>1:
            beta_result='more volatile than'
        else:
            beta_result='not correlated with'
            
        col1, col2 = st.columns(2)
        col1.metric("Alpha", np.around(alpha,decimals=3), "")
        col2.metric("Beta", np.around(beta,decimals=3), "")
        
        #st.write(' - In the above metrics, the shown alpha and beta calculated using CAPM model, represents how stock well performed and its volatility compare to the market index.')
        
        #st.write(' ###### How to interpret the numbers?')
        
        #st.write(' - Alpha is represented as a number like 1 which means the stock performed better than market index by 1% and for the negative number like -4, its vice a versa. For as Beta, the base number is 1 indicating the volatility of the stock is exactly correlated with the market index and 1.5 its 50% mre volatile than the index.')
        
        #st.write(" ###### The " + (selected stock)+" has performed " + str(alpha_result) + " compare to S&P 500. Further in terms of volatility, it is " + str(beta_result) + " the market which can be graphically demonstrated below:")
 
        
        ticker_df[selected_stock] = np.log(ticker_df['Adj Close'] / ticker_df['Adj Close'].shift(1))
        index_df['spy'] = np.log(index_df['Adj Close'] / index_df['Adj Close'].shift(1))
        
        df = pd.concat([index_df['spy'], ticker_df[selected_stock]], axis = 1)
        
        slr_sm_model = smf.ols(selected_stock+'~ spy', data=df)
        slr_sm_model_ko = slr_sm_model.fit()
        param_slr = slr_sm_model_ko.params
        
        plt.figure(figsize = (10, 6))
        plt.rcParams.update({'font.size': 14})
        plt.xlabel("SPY returns")
        plt.ylabel(selected_stock+" returns")
        plt.title("Simple linear regression model")
        plt.scatter(df['spy'],df[selected_stock])
        plt.plot(df['spy'], param_slr.Intercept+param_slr.spy * df['spy'],label='Y={:.4f}+{:.4f}X'.format(param_slr.Intercept, param_slr.spy),color='red')
        plt.legend()
        st.pyplot(plt)
        
        #st.write("To get the detailed summary click below")
        
        if st.button('Linear Regression Summary'):
            st.text(slr_sm_model_ko.summary())

        
        

        
        

        
