#import yfinance as yf
import datetime
import pandas as pd
import numpy as np

EndDate=datetime.datetime.strptime('2021-12-31', '%Y-%m-%d')
StartDate_raw=EndDate - datetime.timedelta(days=50)
EndDate = EndDate.strftime('%Y-%m-%d')
StartDate=StartDate_raw.strftime('%Y-%m-%d')


def today_signal(tickers):
    data=pd.read_excel("model_data_yfinance.xlsx")
    data=data[(data["Date"]>StartDate)&(data["Date"]<EndDate)]

    data1 = data[data["tickers"]==tickers[0]]
    data2 = data[data["tickers"]==tickers[1]]
    data3 = data[data["tickers"]==tickers[2]]
    data4 = data[data["tickers"]==tickers[3]]
    data5 = data[data["tickers"]==tickers[4]]


    def SMA(data,period=30,column='Close'):
        return data[column].rolling(window=period).mean()

    data1['SMA20']=SMA(data1,20)
    data1['SMA50']=SMA(data1,50)
    data2['SMA20']=SMA(data2,20)
    data2['SMA50']=SMA(data2,50)
    data3['SMA20']=SMA(data3,20)
    data3['SMA50']=SMA(data3,50)
    data4['SMA20']=SMA(data4,20)
    data4['SMA50']=SMA(data4,50)
    data5['SMA20']=SMA(data5,20)
    data5['SMA50']=SMA(data5,50)

    data1['signal']=np.where(data1['SMA20']>data1['SMA50'],1,0)
    data1['position']=data1['signal'].diff()
    data2['signal']=np.where(data2['SMA20']>data2['SMA50'],1,0)
    data2['position']=data2['signal'].diff()
    data3['signal']=np.where(data3['SMA20']>data3['SMA50'],1,0)
    data3['position']=data3['signal'].diff()
    data4['signal']=np.where(data4['SMA20']>data4['SMA50'],1,0)
    data4['position']=data4['signal'].diff()
    data5['signal']=np.where(data5['SMA20']>data5['SMA50'],1,0)
    data5['position']=data5['signal'].diff()

    data1['buy']=np.where(data1['position']==1,data1['Close'],np.NAN)
    data1['sell']=np.where(data1['position']== -1,data1['Close'],np.NAN)
    data2['buy']=np.where(data2['position']==1,data2['Close'],np.NAN)
    data2['sell']=np.where(data2['position']== -1,data2['Close'],np.NAN)
    data3['buy']=np.where(data3['position']==1,data3['Close'],np.NAN)
    data3['sell']=np.where(data3['position']== -1,data3['Close'],np.NAN)
    data4['buy']=np.where(data4['position']==1,data4['Close'],np.NAN)
    data4['sell']=np.where(data4['position']== -1,data4['Close'],np.NAN)
    data5['buy']=np.where(data5['position']==1,data5['Close'],np.NAN)
    data5['sell']=np.where(data5['position']== -1,data5['Close'],np.NAN)

    signal=[]

    signal.append(data1['position'].iloc[-1])
    signal.append(data2['position'].iloc[-1])
    signal.append(data3['position'].iloc[-1])
    signal.append(data4['position'].iloc[-1])
    signal.append(data5['position'].iloc[-1])

    return(signal)
