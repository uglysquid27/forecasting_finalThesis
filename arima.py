import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error

file_path = "testdata.xlsx"

df = pd.read_excel(file_path, header=0)

ts = pd.Series(df['Temp_Glue_Scrapper_PV'].values, index=df['epochtime'])

train_size = int(len(ts) * 0.8)
train, test = ts[:train_size], ts[train_size:]

# Fit Autoregressive (AR) model
ar_model = AutoReg(train, lags=5)
ar_model_fit = ar_model.fit()

# Fit Moving Average (MA) model
ma_model = SARIMAX(train, order=(0, 0, 1))
ma_model_fit = ma_model.fit()

# Combine AR and MA components to form ARIMA model
ar_values = ar_model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
ma_values = ma_model_fit.predict(start=len(train), end=len(train)+len(test)-1)

forecast = ar_values + ma_values
print(forecast)
print(test)
errors = test - forecast
absolute_errors = np.abs(errors)
percentage_errors = absolute_errors / test
percentage_errors[~np.isfinite(percentage_errors)] = 0 
mape = np.mean(percentage_errors) * 100
print(f'Mean Absolute Percentage Error (MAPE): {mape:.2f}%')

plt.figure(figsize=(12, 8))

# Plot Autoregressive (AR) component
plt.subplot(3, 1, 1)
plt.plot(test.index, ar_values, color='blue')
plt.title('Autoregressive (AR) Component')
plt.xlabel('Date')
plt.ylabel('Value')

# Plot Moving Average (MA) component
plt.subplot(3, 1, 2)
plt.plot(test.index, ma_values, color='orange')
plt.title('Moving Average (MA) Component')
plt.xlabel('Date')
plt.ylabel('Value')

# Plot Forecast
plt.subplot(3, 1, 3)
plt.plot(train, label='Train')
plt.plot(test.index, forecast, label='Forecast', color='red')
plt.plot(test, label='Test', color='green')
plt.legend()
plt.title('ARIMA Forecast')
plt.xlabel('Date')
plt.ylabel('Value')

plt.tight_layout()
plt.show()
