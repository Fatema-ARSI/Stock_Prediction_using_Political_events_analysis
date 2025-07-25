import numpy as np
import pandas as pd
import datetime
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

def get_predictions(data, forecast_horizon=180):
    # --- Prepare data ---
    cols = list(data)[1:11]  # Feature columns, excluding 'Date'
    df_features = data[cols].astype(float)
    train_dates = pd.to_datetime(data['Date'])

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
        # Prepare input for model
        model_input = np.expand_dims(input_seq, axis=0)
        pred_scaled = model.predict(model_input)[0]

        # Inverse transform the predicted value
        fake_scaled = np.repeat(pred_scaled.reshape(1, -1), df_features.shape[1], axis=-1)
        pred_unscaled = scaler.inverse_transform(fake_scaled)[0][0]  # Assumes target is column 0

        predictions.append(pred_unscaled)
        future_dates.append((last_known_date + pd.Timedelta(days=i+1)).date())

        # Prepare next input: shift and append new prediction
        last_row = input_seq[-1].copy()
        new_row = last_row.copy()
        new_row[0] = pred_scaled[0]  # Replace only target feature

        input_seq = np.vstack([input_seq[1:], new_row])

    # --- Create result DataFrame ---
    df_forecast = pd.DataFrame({
        'Date': future_dates,
        'Prediction': predictions
    })

    return df_forecast
