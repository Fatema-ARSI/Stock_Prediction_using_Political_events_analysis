import streamlit as st
import numpy as np
import pandas as pd
import datetime

#import yfinance as yf
#import yahoo_fin.stock_info as si

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
        
        st.write(' ## Regression Analysis ')

        ticker_df = pd.read_excel("model_data_yfinance.xlsx")

        #sidebar section
        st.sidebar.header('User Input Features')
        #tickers=si.tickers_sp500()
        tickers=ticker_df["tickers"].unique().tolist()
        selected_stock=st.sidebar.selectbox('Select Stock',tickers)
        selected_start_date=st.sidebar.date_input('Select Start Date',datetime.date(2019,7,6),min_value=datetime.date(2014,1,1),max_value=datetime.date(2021,12,31))
        selected_end_date=st.sidebar.date_input('Select Start Date',datetime.date(2020,7,6),min_value=datetime.date(2014,1,1),max_value=datetime.date(2021,12,31))

        ####################################################
        ## Fetched data from yfinance

        ticker_df = ticker_df[ticker_df["tickers"]==selected_stock]
        ticker_df=ticker_df[(ticker_df["Date"]>str(selected_start_date))&(ticker_df["Date"]<str(selected_end_date))]
        index_df = pd.read_excel("spy_current.xlsx")
        index_df=index_df[(index_df["Date"]>str(selected_start_date))&(index_df["Date"]<str(selected_end_date))]

        ####################################################

        st.write(" This page presents a regression analysis between" + str(selected_stock) + "and the S&P 500 market index to assess the relationship between" +  str(selected_stock) +"’s daily returns and overall market performance.")
        st.write()
        st.write(""" **Regression Metrics (Based on CAPM Model):** """)
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

        st.write("")

        col1, col2 = st.columns(2)

        col1.metric("Alpha", np.around(alpha,decimals=3), "")
        col2.metric("Beta", np.around(beta,decimals=3), "")

        st.write("")

        st.markdown(""" These values are derived using the **Capital Asset Pricing Model (CAPM)**, which evaluates a stock's performance and volatility relative to the market.""")

        st.markdown(""" ###### How to interpret the numbers? """)

        st.markdown(""" **Alpha** indicates the stock’s excess return relative to the market.""")
        st.markdown(""" - A positive alpha (e.g., 1) means the stock outperformed the market by 1%.""")
        st.markdown(""" - A negative alpha (e.g., -4) means the stock underperformed the market by 4%.""")

        st.markdown(""" **Beta** imeasures the stock’s volatility compared to the market:""")
        st.markdown(""" - A beta of 1 implies the stock moves in line with the market.""")
        st.markdown(""" - A beta of 1.5 suggests the stock is 50% more volatile than the market.""")
        st.markdown(""" - A beta below 1 (like 0.723) indicates less volatility than the market, but still a positive correlation.""")


        st.markdown(""" ###### Summary: """)
        st.write(" Based on this analysis,"+ str(selected_stock) +" has derperformed "+ str(alpha_result) +" compared to the S&P 500. However, its beta of "+ str(beta_result) +" shows it moves in the same direction as the market, but with lower volatility. This relationship is further illustrated in the graph below.

        st.write(" ###### The " + str(selected_stock)+" has performed " + str(alpha_result) + " compare to S&P 500. Further in terms of volatility, it is " + str(beta_result) + " the market which can be graphically demonstrated below:")

        st.write("")

        ticker_df[selected_stock] = np.log(ticker_df['Adj Close'] / ticker_df['Adj Close'].shift(1))
        index_df['spy'] = np.log(index_df['Adj Close'] / index_df['Adj Close'].shift(1))

        # Merge the two DataFrames on 'Date' column
        df = pd.merge(
           ticker_df[['Date', selected_stock]],
           index_df[['Date', 'spy']],
           on='Date',
           how='inner'
           )
        df.dropna(inplace=True)

        slr_sm_model = smf.ols(selected_stock+'~ spy', data=df)
        slr_sm_model_ko = slr_sm_model.fit()
        param_slr = slr_sm_model_ko.params

        st.write("")
        plt.figure(figsize = (10, 6))
        plt.rcParams.update({'font.size': 14})
        plt.xlabel("SPY returns")
        plt.ylabel(selected_stock+" returns")
        plt.title("Simple linear regression model")
        plt.scatter(df['spy'],df[selected_stock])
        plt.plot(df['spy'], param_slr.Intercept+param_slr.spy * df['spy'],label='Y={:.4f}+{:.4f}X'.format(param_slr.Intercept, param_slr.spy),color='red')
        plt.legend()
        st.pyplot(plt)

        st.write("")

        st.markdown(""" To get the detailed summary click below """)

        if st.button('Linear Regression Summary'):
            st.text(slr_sm_model_ko.summary())
