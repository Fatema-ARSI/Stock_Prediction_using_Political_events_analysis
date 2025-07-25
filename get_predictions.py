import numpy as np
import pandas as pd
import datetime
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

def get_predictions(data, forecast_horizon=252):
    # --- Prepare data ---
    cols = list(data)[1:11]  # Feature columns, excluding 'Date'
    df_features = data[cols].astype(float)
    train_dates = pd.to_datetime(data['Date'])
    
    # Find index of 'Close' column in the features
    close_idx = cols.index('Close')  # should be 3 as you said

    # --- Scale features ---
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_features)

    # --- Load model ---
    model = tf.keras.models.load_model('stock_prediction.h5')

    # --- Initialize with last 90 days of actual data ---
    n_past = 90
    input_seq = df_scaled[-n_past:].copy()

    predictions = []
    future_dates = []

    last_known_date = train_dates.iloc[-1]

    for i in range(forecast_horizon):
        # Prepare input for model: shape (1, 90, features)
        model_input = np.expand_dims(input_seq, axis=0)

        # Predict scaled value for the Close column
        pred_scaled = model.predict(model_input)[0]

        # To inverse transform, we create a fake scaled array with predicted Close at correct index
        fake_scaled = np.zeros((1, df_features.shape[1]))
        fake_scaled[0, close_idx] = pred_scaled[0]

        # Inverse transform to original scale
        pred_unscaled = scaler.inverse_transform(fake_scaled)[0][close_idx]

        predictions.append(pred_unscaled)
        future_dates.append((last_known_date + pd.Timedelta(days=i + 1)).date())

        # Prepare next input sequence: drop first row, append new row
        # Replace Close value in new row with predicted scaled value
        new_row = input_seq[-1].copy()
        new_row[close_idx] = pred_scaled[0]
        input_seq = np.vstack([input_seq[1:], new_row])

    # --- Create result DataFrame ---
    df_forecast = pd.DataFrame({
        'Date': future_dates,
        'Prediction': predictions
    })

    return df_forecast

