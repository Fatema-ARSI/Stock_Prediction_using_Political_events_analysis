import streamlit as st
import base64


#add an import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class home_page(HydraHeadApp):


    def run(self):
        #sidebar section
        # Main panel
        st.markdown("""# Stock Price Prediction using News - Events Analysis""")
        file_ = open("logo.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="stock gif" width="750" height="500">',
            unsafe_allow_html=True,
        )
        
        st.markdown(""" **Can we predict stock prices and their movements?** """)
        st.markdown(""" This application leverages machine learning models to analyze how financial news impacts stock performance through sentiment analysis. It presents predicted stock prices based on daily news and events, offering insights into potential market movements.""")
        
        st.markdown(""" The model was trained using historical data from **January 1, 2014, to December 31, 2021**, for regression analysis and prediction. Data from **January 1, 2022, to May 31, 2023**, was used to evaluate the model’s accuracy and validate its predictive capability. """)
        
        st.markdown(""" From the navigation bar, you can explore:""")
        st.markdown(""" * **Regression on Stocks:** Compare individual stock performance with the S&P 500 index. """)
        st.markdown(""" * **Stock Price Prediction:** View forecasted prices of selected stocks. """)
        st.markdown(""" * **Portfolio Optimization:** Allocate capital efficiently to maximize returns on your selected portfolio. """)
        
        
        st.markdown(""" **Note:** This application is intended for informational purposes only and does not constitute financial advice. """)
        st.markdown(""" **Powered by Python libraries:** `Yahoo Finance`, `Pandas`, `Streamlit`, `Plotly`,`Hydralit`,`Tensorflow`, `Linear Regression`, `Pyportfolioopt`,`VaderSentiment`  """)
