
import numpy as np


import pandas as pd
import datetime



def get_plot_data1(data1,data2):

    main_line=pd.DataFrame(data1[['Date','Close']])
    main_line=main_line.append(data2)

    return(main_line)

def get_plot_data2(main_line,data1,data2):

    signals=pd.DataFrame()
    signals['Date']=main_line['Date']
    signals['Close']=data1['Close'].append(data2['Prediction'])

    def SMA(data,period=30,column='Close'):
        return data[column].rolling(window=period).mean()

    signals['SMA20']=SMA(signals,20)
    signals['SMA50']=SMA(signals,50)
    signals['signal']=np.where(signals['SMA20']>signals['SMA50'],1,0)
    signals['position']=signals['signal'].diff()
    signals['buy']=np.where(signals['position']==1,signals['Close'],np.NAN)
    signals['hold']=np.where(signals['position']==0,signals['Close'],np.NAN)
    signals['sell']=np.where(signals['position']== -1,signals['Close'],np.NAN)

    return(signals)
