import pandas as pd
import matplotlib.pyplot as plt

# Load the data
ticker = "AAPL"
file_path = f'stationary_stock_data/{ticker}_diff_prices.csv'
data = pd.read_csv(file_path)

# Convert 'Date' column to datetime format and set it as the index
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Plotting the 'Close' column
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['Adj Close'], label='Close Price', color='Green')
plt.title(f'{ticker}_Adj_Close_Daily')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.tight_layout()
plt.show()