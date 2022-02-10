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
##Metrics Alpha Beta
ticker_df['daily_ret'] = ticker_df['Close'].pct_change(1)
index_df['daily_ret'] = index_df['Close'].pct_change(1)
LR = stats.linregress(ticker_df['daily_ret'].iloc[1:],index_df['daily_ret'].iloc[1:])
beta,alpha,r_val,p_val,std_err = LR

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Alpha", np.around(alpha,decimals=3), "")
col2.metric("Beta", np.around(beta,decimals=3), "")
col3.metric("std_err", np.around(std_err,decimals=3), "")


        ## Calculate log returns for the period based on Adj Close prices
ticker_df[selected_stock] = np.log(ticker_df['Adj Close'] / ticker_df['Adj Close'].shift(1))
index_df['spy'] = np.log(index_df['Adj Close'] / index_df['Adj Close'].shift(1))

####################################################

####################################################
## Create a dataframe with X's (spy, pep, usdx) and Y (ko)
df = pd.concat([index_df['spy'], ticker_df[selected_stock]], axis = 1)

## Save the csv file. Good practice to save data files after initial processing
#df.to_csv("Jul2021_data_lin_regression.csv")

####################################################

####################################################
## 2a. Fit a simple linear regression model to the data using statsmodels

### Create an instance of the class OLS
slr_sm_model = smf.ols(selected_stock+'~ spy', data=df)

### Fit the model (statsmodels calculates beta_0 and beta_1 here)
slr_sm_model_ko = slr_sm_model.fit()


param_slr = slr_sm_model_ko.params

####################################################

## Linear regression plot of X (spy) and Y (ko)
plt.figure(figsize = (10, 6))
plt.rcParams.update({'font.size': 14})
plt.xlabel("SPY returns")
plt.ylabel(selected_stock+" returns")
plt.title("Simple linear regression model")
plt.scatter(df['spy'],df[selected_stock])
plt.plot(df['spy'], param_slr.Intercept+param_slr.spy * df['spy'],
         label='Y={:.4f}+{:.4f}X'.format(param_slr.Intercept, param_slr.spy),color='red')
plt.legend()
## show plot
st.pyplot(plt)
### Summarize the model

if st.button('Linear Regression Summary'):
    st.text(slr_sm_model_ko.summary())

        ####################################################

        ############################################ main code ###############################################



        
