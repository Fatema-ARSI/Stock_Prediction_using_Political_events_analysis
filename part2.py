import streamlit as st
import numpy as np
import yfinance as yf
import yahoo_fin.stock_info as si
import pandas as pd
import datetime
from functools import reduce
import plotly.graph_objs as go
import plotly.io as pio
from plotly.offline import init_notebook_mode,iplot
from today_signal import today_signal
from get_data import get_self_made_data_frame
from get_predictions import get_predictions
from get_plot_data import get_plot_data1, get_plot_data2
###import to Hydralit
from hydralit import HydraHeadApp

#create a wrapper class
class stock_prediction(HydraHeadApp):
    #wrap all your code in this method and you should be done
    def run(self):
        ##############################################################
        ###SIDEBAR section
        st.sidebar.header('User Input Features')
        tickers=si.tickers_sp500()
        selected_stock=st.sidebar.multiselect('Select Stock (Maximum 5)',tickers,['AAPL','V','AZO','JNJ','FDX'])
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
                
        col1,col2,col3=st.columns(3)
        col1.metric(selected_stock[0],tickers[0],"")
        col2.metric(selected_stock[1],tickers[1],"")
        col3.metric(selected_stock[2],tickers[2],"")
        col1,col2=st.columns(2)
        col1.metric(selected_stock[3],tickers[3],"")
        col2.metric(selected_stock[4],tickers[4],"")
        
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

        #################################################################
        
         #predicted results
       
        df_forecast1=get_predictions(df1)
        df_forecast2=get_predictions(df2)
        df_forecast3=get_predictions(df3)
        df_forecast4=get_predictions(df4)
        df_forecast5=get_predictions(df5)
        
        df_forecast=[df_forecast1,df_forecast2,df_forecast3,df_forecast4,df_forecast5]
        
        df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],how='outer'), df_forecast)
        

        
        ########@#####################################################################@
        #get the plot data
       

        main_line1=get_plot_data1(df1,df_forecast1)
        main_line2=get_plot_data1(df2,df_forecast2)
        main_line3=get_plot_data1(df3,df_forecast3)
        main_line4=get_plot_data1(df4,df_forecast4)
        main_line5=get_plot_data1(df5,df_forecast5)

        signals1=get_plot_data2(main_line1,df1,df_forecast1)
        signals2=get_plot_data2(main_line2,df2,df_forecast2)
        signals3=get_plot_data2(main_line3,df3,df_forecast3)
        signals4=get_plot_data2(main_line4,df4,df_forecast4)
        signals5=get_plot_data2(main_line5,df5,df_forecast5)
        
     
        
        def plot_data(data1,data2):
            
            fig=go.Figure()
            fig.add_scatter(x=data1['Date'],y=data1['Prediction'],line={'color':'blue'},name='Predicted Data',
                            hovertemplate="Date: %{x}<br>Predicted Close Price: %{y}<br>HOLD<extra></extra>",opacity=0.5)
            fig.add_scatter(x=data2['Date'],y=data2['Close'],line={'color':'orange'},name='Actual Data',
                            hovertemplate="Date: %{x}<br>Close Price: %{y}<br>HOLD<extra></extra>",opacity=0.5)

            fig.update_xaxes(rangeslider_visible=False,rangeselector=dict(buttons=list ([dict(count=1,label='1m',step='month',stepmode='backward'),
                                                                                          dict(count=6,label='6m',step="month",stepmode='backward'),
                                                                                          dict(count=1,label='YTD',step="year",stepmode='todate'),
                                                                                          dict(count=1,label='1Y',step="year",stepmode='backward'),
                                                                                          dict(step="all")])
                                                                                         ))
            fig.add_scatter(mode="markers", x=data2['Date'], y=data2['buy'],marker_symbol='triangle-up',
                                        marker_color="green",
                                       marker_line_width=1, marker_size=10,
                                       hovertemplate="Date: %{x}<br>Close Price: %{y}<br>BUY<extra></extra>",showlegend=False)
            fig.add_scatter(mode="markers", x=data2['Date'], y=data2['sell'],marker_symbol='triangle-down',
                                        marker_color="red",
                                       marker_line_width=1, marker_size=10,
                                       hovertemplate="Date: %{x}<br>Close Price: %{y}<br>SELL<extra></extra>",showlegend=False)
            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
            return (fig)

        figs=[]
        figs.append(plot_data(main_line1,signals1))
        figs.append(plot_data(main_line2,signals2))
        figs.append(plot_data(main_line3,signals3))
        figs.append(plot_data(main_line4,signals4))
        figs.append(plot_data(main_line5,signals5))
        
        st.header('Stock Closing Price')
        for i in list(figs)[:num_company]:
            st.plotly_chart(i,use_container_width=True)
            
        if st.button('Show Model Prediction'):
            st.dataframe(df_merged)
           
        

       
