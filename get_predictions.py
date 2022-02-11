import numpy as np

import pandas as pd
import datetime

import tensorflow as tf


from sklearn.preprocessing import StandardScaler
from pandas.core.reshape.merge import merge





def get_predictions(data):
  #variables for training
  cols=list(data)[1:11]
  df_for_training=data[cols].astype(float)
  train_dates=pd.to_datetime(data['Date'])
  
  scaler=StandardScaler()
  scaler=scaler.fit(df_for_training)
  df_for_training_scaled=scaler.transform(df_for_training)

  train_x=[]
  train_y=[]
  n_future=1
  n_past=90

  for i in range(n_past,len(df_for_training_scaled)-n_future+1):
    train_x.append(df_for_training_scaled[i-n_past:i,0:df_for_training.shape[1]])
    train_y.append(df_for_training_scaled[i+n_future-1:i+n_future,1])

  train_x,train_y=np.array(train_x),np.array(train_y)

  model=tf.keras.models.load_model('stock_prediction.h5')

  
  n_futuredays=2000
  forecast_period_dates=pd.date_range(list(train_dates)[-1],periods=n_futuredays,freq='1d').tolist()

  forecast=model.predict(train_x[-n_futuredays:])

  forecast_copies=np.repeat(forecast,df_for_training.shape[1],axis=-1)

  y_pred_future=scaler.inverse_transform(forecast_copies)[:,0]

  forecast_dates=[]
  for time_i in forecast_period_dates:
    forecast_dates.append(time_i.date())

  df_forecast=pd.DataFrame({'Date':forecast_dates,'Prediction':y_pred_future})

  return(df_forecast)
  



