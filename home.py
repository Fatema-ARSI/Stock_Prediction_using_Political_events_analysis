import streamlit as st
import base64


#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class home_page(HydraHeadApp):


    def run(self):
        #sidebar section
        # Main panel
        """# Stock Price Prediction using Poitical Events Analysis"""
        file_ = open("logo.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="stock gif" width="750" height="500">',
            unsafe_allow_html=True,
        )
        st.markdown("""##
        Can we predict the Stock Price and its movement in the future?
        Machine learning model helps to understand the affect of given news on the market stocks using sentiment analysis.
        This app showcase the predicted price using the news-events for the given day.
        Please select **Regression on Stocks** to compare the stock with Market Index S&P 500, **Stock Price Prediction** to see selected stock's future price and **Portfolio Optimization** for allocating the capital to get higher return on selected portfolio from the navigation bar.

        --- Note: This is app can be used for information purpose only.
        * Python libraries: `Yahoo Finance`, `Pandas`, `Streamlit`, `Plotly`,`Hydralit`,`Tensorflow`, `Linear Regression`, `Pyportfolioopt`,`VaderSentiment`
        """)
