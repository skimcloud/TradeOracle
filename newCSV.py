import pandas as pd
import numpy as np  # Import numpy for NaN handling

# Read the orders data
orders_df = pd.read_csv('new_maria_orders_processed.csv')

# Extract unique tickers (excluding NaN values)
unique_tickers = orders_df['ticker'].dropna().unique()

# Create column names for each of the 90 days for open, high, low, and volume
days_columns = [f'open_{i}' for i in range(1, 181)] + \
               [f'high_{i}' for i in range(1, 181)] + \
               [f'low_{i}' for i in range(1, 181)] + \
               [f'volume_{i}' for i in range(1, 181)]

# Add these columns to the orders dataframe
orders_df = pd.concat([orders_df, pd.DataFrame(columns=days_columns)])

# Loop through each unique ticker
for ticker in unique_tickers:
    if isinstance(ticker, str):  # Check if ticker is not NaN
        # Filter orders for the current ticker
        ticker_orders = orders_df[orders_df['ticker'] == ticker]

        # Read the corresponding ticker's daily price data
        try:
            ticker_price_data = pd.read_csv(f'price_data/{ticker}_daily_prices.csv')
            ticker_price_data['timestamp'] = pd.to_datetime(ticker_price_data['timestamp'])
        except FileNotFoundError:
            continue  # Skip processing if file not found for the ticker

        # Loop through orders for this ticker
        for index, order in ticker_orders.iterrows():
            # Extract necessary data from the order
            order_execution_date = pd.to_datetime(order['order_execution_datetime'])

            # Find the index of the row closest to the order execution date
            closest_index = ticker_price_data['timestamp'].sub(order_execution_date).abs().idxmin()

            # Get the first 60 elements leading up to the order execution date
            index_start = max(0, closest_index - 181)  # Ensure not to go below 0
            first_180_days_data = ticker_price_data.iloc[index_start:closest_index]

            # Assign price and volume values to the respective columns
            for i, row in first_180_days_data.iterrows():
                matching_day = closest_index - i
                orders_df.at[index, f'open_{matching_day}'] = row['open']
                orders_df.at[index, f'high_{matching_day}'] = row['high']
                orders_df.at[index, f'low_{matching_day}'] = row['low']
                orders_df.at[index, f'volume_{matching_day}'] = row['volume']

# Write the updated dataframe back to a new CSV or the same file
orders_df.to_csv('prices_with_order.csv', index=False)
