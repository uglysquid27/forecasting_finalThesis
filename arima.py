import pandas as pd

# Define the data
data = {
    'Date': ['3/23/2022', '4/1/2022', '5/1/2022', '6/1/2022', '7/1/2022', '8/1/2022', '9/1/2022', '10/1/2022',
             '11/1/2022', '12/1/2022', '1/1/2023', '2/1/2023', '3/1/2023', '4/1/2023', '5/1/2023', '6/1/2023',
             '7/3/2023', '8/1/2023', '9/1/2023'],
    'Value': [2.073, 2.07, 2.069, 2.9, 2.076, 2.072, 2.077, 2.067, 2.071, 2.069, 2.068, 2.91, 2.902, 2.07, 2.901, 2.908,
              2.078, 2.07, 2.075]
}

# Create a DataFrame
df = pd.DataFrame(data) 

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' column as index
df.set_index('Date', inplace=True)

# Display the DataFrame
print(df)

# Split data into training and testing sets
train_data = df.iloc[:8]
test_data = df.iloc[8:]

# Display the training and testing sets
print("Training Data:")
print(train_data)
print("\nTesting Data:")
print(test_data)

from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Fit ARIMA model with order (1, 1, 0)
model = ARIMA(train_data['Value'], order=(1, 1, 0))
results = model.fit()

# Display the model summary
print(results.summary())
 
# Forecast future values
forecast_steps = len(test_data)  # Number of steps ahead to forecast
forecast = results.forecast(steps=forecast_steps)

# Plot the original data and the forecasted values
plt.figure(figsize=(10, 6))
plt.plot(train_data.index, train_data['Value'], label='Training Data')
plt.plot(test_data.index, test_data['Value'], label='Testing Data')
plt.plot(test_data.index, forecast, label='Forecast')
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('ARIMA Forecast')
plt.legend()
plt.xticks(rotation=45)
plt.show()
