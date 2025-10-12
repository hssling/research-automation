import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense
import plotly.express as px

st.set_page_config(page_title="📊 Self-Contained Forecast Dashboard", layout="wide")

st.title("📊 Time Series Forecast Dashboard")
st.write("Upload your dataset and get Prophet, ARIMA, and LSTM forecasts instantly.")

# ================================
# 1. File Upload
# ================================
uploaded_file = st.file_uploader("Upload your time series CSV (columns: ds, y)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values("ds").reset_index(drop=True)

    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df.head())

    # ================================
    # 2. Prophet Forecast
    # ================================
    st.subheader("🔮 Prophet Forecast")
    with st.spinner("Training Prophet model..."):
        prophet_model = Prophet()
        prophet_model.fit(df)
        future = prophet_model.make_future_dataframe(periods=30)  # predict 30 days ahead
        forecast = prophet_model.predict(future)

    fig_prophet = px.line(forecast, x="ds", y="yhat", title="Prophet Forecast")
    fig_prophet.add_scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode="lines", name="Lower Bound")
    fig_prophet.add_scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode="lines", name="Upper Bound")
    st.plotly_chart(fig_prophet, use_container_width=True)

    # ================================
    # 3. ARIMA Forecast
    # ================================
    st.subheader("📈 ARIMA Forecast")
    with st.spinner("Training ARIMA model..."):
        train, test = df['y'][:-30], df['y'][-30:]
        arima_model = ARIMA(train, order=(5,1,0))
        arima_fit = arima_model.fit()
        forecast_arima = arima_fit.forecast(steps=30)

    arima_fig = px.line(x=df['ds'][-60:], y=df['y'][-60:], labels={'x':'Date','y':'Value'}, title="ARIMA Forecast")
    arima_fig.add_scatter(x=df['ds'][-30:], y=forecast_arima, mode="lines+markers", name="Forecast")
    st.plotly_chart(arima_fig, use_container_width=True)

    mse_arima = mean_squared_error(test, forecast_arima)
    st.info(f"ARIMA MSE: {mse_arima:.2f} | AIC: {arima_fit.aic:.2f} | BIC: {arima_fit.bic:.2f}")

    # ================================
    # 4. LSTM Forecast
    # ================================
    st.subheader("🤖 LSTM Forecast")
    with st.spinner("Training LSTM neural network..."):

        values = df['y'].values.reshape(-1,1)
        train_size = int(len(values)*0.8)
        train, test = values[:train_size], values[train_size:]

        scaler = MinMaxScaler()
        train_scaled = scaler.fit_transform(train)
        test_scaled = scaler.transform(test)

        def create_dataset(dataset, look_back=5):
            X, Y = [], []
            for i in range(len(dataset)-look_back):
                X.append(dataset[i:i+look_back,0])
                Y.append(dataset[i+look_back,0])
            return np.array(X), np.array(Y)

        look_back = 5
        X_train, y_train = create_dataset(train_scaled, look_back)
        X_test, y_test = create_dataset(test_scaled, look_back)

        X_train = X_train.reshape(X_train.shape[0], look_back, 1)
        X_test = X_test.reshape(X_test.shape[0], look_back, 1)

        model = Sequential([
            LSTM(50, return_sequences=False, input_shape=(look_back,1)),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=0)

        predictions = model.predict(X_test)
        predictions = scaler.inverse_transform(predictions)

    lstm_fig = px.line(x=df['ds'][-len(y_test):], y=scaler.inverse_transform(y_test.reshape(-1,1)).flatten(),
                       labels={'x':'Date','y':'Value'}, title="LSTM Forecast (Test Set)")
    lstm_fig.add_scatter(x=df['ds'][-len(predictions):], y=predictions.flatten(), mode="lines+markers", name="Predicted")
    st.plotly_chart(lstm_fig, use_container_width=True)

    mse_lstm = mean_squared_error(scaler.inverse_transform(y_test.reshape(-1,1)), predictions)
    st.info(f"LSTM MSE: {mse_lstm:.2f}")

    # ================================
    # 5. Model Comparison
    # ================================
    st.subheader("📊 Model Comparison")
    comparison = pd.DataFrame({
        'Model': ['Prophet','ARIMA','LSTM'],
        'MSE': ['(check residuals)', round(mse_arima,2), round(mse_lstm,2)],
        'AIC': ['(not applicable)', round(arima_fit.aic,2), '(not applicable)'],
        'BIC': ['(not applicable)', round(arima_fit.bic,2), '(not applicable)']
    })
    st.dataframe(comparison)

else:
    st.warning("⬆️ Please upload a CSV file with columns: ds (date), y (value).")

    st.subheader("📖 Instructions")
    st.markdown("""
    **How to use this dashboard:**

    1. Prepare your CSV file with exactly 2 columns:
       - `ds`: Date string (YYYY-MM-DD format)
       - `y`: Numeric value to forecast

    2. Click "Browse files" to upload your CSV

    3. Watch as the dashboard automatically:
       - Traines Prophet (Bayesian forecasting)
       - ARIMA (statistical time series)
       - LSTM (deep learning neural network)

    4. Explore interactive plots, metrics, and comparisons

    **Sample data included:** Can be found in `time_series_pipeline/data/timeseries.csv`
    """)
