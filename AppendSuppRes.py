import os
import pandas as pd
import numpy as np

def calculate_daily_volatility(prices, span=20):
    log_returns = np.log(prices / prices.shift(1))
    return log_returns.ewm(span=span).std()

# Read the merged_dataset CSV file
orders = pd.read_csv('merged_dataset.csv')

# Initialize lists to store new column values
raw_close_values = []
upper_barrier_values = []
lower_barrier_values = []
diff_upper_barrier_values = []
diff_lower_barrier_values = []

# Iterate through each order in orders
for index, order in orders.iterrows():
    ticker = order['ticker']
    entry_price = order['entry_price']
    execution_date = pd.to_datetime(order['order_execution_datetime'])
    expiration_date = pd.to_datetime(order['expiration'])

    # Load the corresponding ticker_data.csv
    file_path = f'raw_stock_data/{ticker}.csv'
    if os.path.exists(file_path):
        ticker_data = pd.read_csv(file_path)
        ticker_data['Date'] = pd.to_datetime(ticker_data['Date'])

        # Filter data for the period between execution and expiration
        data_within_period = ticker_data[(ticker_data['Date'] >= execution_date) & (ticker_data['Date'] <= expiration_date)]

        if not data_within_period.empty:
            # Calculate daily volatility
            daily_vol = calculate_daily_volatility(data_within_period['Adj Close'])

            # Assuming we use a factor of daily volatility to set our barriers
            volatility_factor = 2  # This can be adjusted
            current_stock_price = data_within_period['Close'].iloc[-1]
            upper_barrier = current_stock_price + (current_stock_price * daily_vol.mean() * volatility_factor)
            lower_barrier = current_stock_price - (current_stock_price * daily_vol.mean() * volatility_factor)

            # Append the new column values to the respective lists
            raw_close_values.append(current_stock_price)
            upper_barrier_values.append(upper_barrier)
            lower_barrier_values.append(lower_barrier)
            diff_upper_barrier_values.append(upper_barrier - current_stock_price)
            diff_lower_barrier_values.append(current_stock_price - lower_barrier)
        else:
            # Append NaN values if no valid data found for the order
            raw_close_values.append(np.nan)
            upper_barrier_values.append(np.nan)
            lower_barrier_values.append(np.nan)
            diff_upper_barrier_values.append(np.nan)
            diff_lower_barrier_values.append(np.nan)
    else:
        # Append NaN values if no data file found for the order
        raw_close_values.append(np.nan)
        upper_barrier_values.append(np.nan)
        lower_barrier_values.append(np.nan)
        diff_upper_barrier_values.append(np.nan)
        diff_lower_barrier_values.append(np.nan)

# Add the new columns to the 'orders' DataFrame
orders['raw_close'] = raw_close_values
orders['upper_barrier'] = upper_barrier_values
orders['lower_barrier'] = lower_barrier_values
orders['diff_upper_barrier'] = diff_upper_barrier_values
orders['diff_lower_barrier'] = diff_lower_barrier_values

# Drop rows with NaN values
orders.dropna(inplace=True)

# Output the modified CSV with new columns added and NaN rows dropped
orders.to_csv('final_dataset_with_barriers.csv', index=False)
