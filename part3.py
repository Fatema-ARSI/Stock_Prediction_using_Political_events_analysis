import streamlit as st
import numpy as np
import pandas as pd
import datetime
from annotated_text import annotated_text
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import plotly.graph_objects as go

import yahoo_fin.stock_info as si
import yfinance as yf
from get_data import get_self_made_data_frame
from get_predictions import get_predictions



#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class portfolio_optimization(HydraHeadApp):

#wrap all your code in this method and you should be done
    def run(self):


        ######################################################
        ## SIDEBAR SECTION

        #sidebar section
        st.sidebar.header('User Input Features')
        tickers=si.tickers_sp500()
        Amount=st.sidebar.number_input('Put your investment amount here',2000)
        selected_stock=st.sidebar.multiselect('Select Stock (Maximum 5)',tickers,['AAPL','V','AZO','JNJ','FDX'])
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
        
        
        st.write('Frontier Efficient theory by Professor Henry for portfolio optimization justifies that from the given set of portfolios with same rate of risk, investor will choose one with higher return.')
        st.write('This model creates the best fitted portfolio set for the given risk rate to increase the return by allocating the number of shares of non-correlated shares (for diversification of portfolio) for given capital amount. Allocation for given stocks and amount are as follows:')
        df.set_index('Date',inplace=True)
        #assign equivalent weights to each stock within the portfolio
        length=len(df)
        weights=np.array([0.2]*length )
        # This means if I had a total of 100 EURO in the portfolio, then I would have 20 EURO in each stock.
        #Show the daily simple returns, NOTE: Formula = new_price/old_price - 1
        # Calculate the expected returns and the annualised sample covariance matrix of daily asset returns.
        mu = expected_returns.mean_historical_return(df)#returns.mean() * 252
        S = risk_models.sample_cov(df) #Get the sample covariance matrix
        # Optimize for maximal Sharpe ration .
        ef = EfficientFrontier(mu, S)
        weights = ef.max_sharpe()
        #Maximize the Sharpe ratio, and get the raw weights
        cleaned_weights = ef.clean_weights()
        
        #Note the weights may have some rounding error, meaning they may not add up exactly to 1 but should be close
        data=ef.portfolio_performance(verbose=True)

        # Now we see that we can optimize this portfolio by having about 44.29% of the portfolio in Tesla , 55.71% in Amazon.
        # Also I can see that the expected annual volatility has increased to 34.5% but the annual expected rate also to 50.7% is . This optimized portfolio has a Sharpe ratio of 1.41 which is good.
        # I want to get the discrete allocation of each share of the stock, meaning I want to know exactly how many of each stock I should buy given some amount that I am willing to put into this portfolio.
        latest_prices = get_latest_prices(df)
        weights = cleaned_weights
        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=Amount)
        allocation, leftover = da.lp_portfolio()
        annotated_text(('hii','hii','#ffd127'))
        
        shares_allocations=pd.DataFrame(allocation.items(),columns=["Stocks","Shares"])
        st.write("Expected annual return {:.2f}".format(data[0]*100)+'%')
        st.write("Expected annual risk {:.2f}".format(data[1] * 100)+'%')
        st.write("Sharpe Ratio {:.2f}".format(data[2])+'%')
        
        st.write("Funds remaining: EURO {:.2f}".format(leftover))
        st.write('Sharper ratio is the average return earned in excess of the risk-free rate per unit of volatility or total risk. Usually, any Sharpe ratio greater than 1.0 is considered acceptable to good by investors. A ratio higher than 2.0 is rated as very good. A ratio of 3.0 or higher is considered excellent.')
 
                        
        
                
        labels=shares_allocations["Stocks"]
        values=shares_allocations["Shares"]
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig = go.Figure(data=[go.Pie(labels=labels,values=values)])
        fig.update_traces(hoverinfo='label+value+percent', textinfo='value', textfont_size=20,
                          marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        st.plotly_chart(fig)
        
        if st.button('Show Portfolio Allocation'):
            st.dataframe(shares_allocations)
