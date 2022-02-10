import numpy as np
import pandas as pd
import datetime
from annotated_text import annotated_text
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import plotly.graph_objects as go

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
        Amount=st.sidebar.number_input('Put your investment amount here',2000)
        

        ####################################################

        #Store the adjusted close price of stock into the data frame
        df=pd.read_csv(r'stockspredictions (1).csv')
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
        
        shares_allocations=pd.DataFrame(allocation.items(),columns=["Stocks","Shares"])
        st.write("Expected annual return {:.2f}".format(data[0]*100)+'%')
        st.write("Expected annual risk {:.2f}".format(data[1] * 100)+'%')
        st.write("Sharpe Ratio {:.2f}".format(data[2])+'%')
        annotated_text(shares_allocations[0,0],((df.iloc[0,1],'Shares','color')))
        st.write("Funds remaining: EURO {:.2f}".format(leftover))
        
        labels=df["Stocks"]
        values=df["Shares"]
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig = go.Figure(data=[go.Pie(labels=labels,values=values)])
        fig.update_traces(hoverinfo='label+value+percent', textinfo='value', textfont_size=20,
                          marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        st.plotlychart(fig)
