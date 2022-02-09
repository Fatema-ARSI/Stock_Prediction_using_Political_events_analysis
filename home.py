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
        This app showcase the Stock Valuation and Sector analysis.
        Please select **Company analysis** for comparable companies analysis, **Sector Analysis** for sector analysis and **Sector Opportunity and Challenges** for sector trends and threats for industries in 2022 from the navigation bar.

        --- Note: This is app can be used for information purpose only.
        * Python libraries: `Yahoo Finance`, `Pandas`, `Streamlit`, `Plotly`,`Hydralit`,`Long Short-Term Memory(LSTM) Model`, `Linear Regression
        """)
