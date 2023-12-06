import os
import pandas as pd

# Read the raw_orders_2023 CSV file
raw_orders = pd.read_csv('entries_matched_2023.csv')

# Function to calculate support and resistance levels for a specified duration
def calculate_long_term_support_resistance(data):
    pivot_point = (data['High'] + data['Low'] + data['Close']) / 3
    support_l1 = (pivot_point * 2) - data['High']
    support_l2 = pivot_point - (data['High'] - data['Low'])
    resistance_l1 = (pivot_point * 2) - data['Low']
    resistance_l2 = pivot_point + (data['High'] - data['Low'])
    
    return pivot_point, support_l1, support_l2, resistance_l1, resistance_l2

# Iterate through each order in raw_orders_2023
for index, order in raw_orders.iterrows():
    ticker = order['ticker']
    execution_date = pd.to_datetime(order['order_execution_datetime'], format='%m/%d/%Y %I:%M %p').strftime('%Y-%m-%d')
    
    # Load the corresponding ticker_data.csv
    file_path = f'yahoo_price_data/{ticker}_data.csv'
    if os.path.exists(file_path):
        ticker_data = pd.read_csv(file_path)
        
        # Convert Date column to datetime if not already in datetime format
        ticker_data['Date'] = pd.to_datetime(ticker_data['Date'])
        
        # Filter data for the specified window size
        window_start = pd.to_datetime(execution_date) - pd.DateOffset(days=90)
        window_end = pd.to_datetime(execution_date)
        data_within_window = ticker_data[(ticker_data['Date'] >= window_start) & (ticker_data['Date'] <= window_end)]
        
        if not data_within_window.empty:
            # Calculate long-term support and resistance levels
            pivot_point, support_l1, support_l2, resistance_l1, resistance_l2 = calculate_long_term_support_resistance(data_within_window)
            
            # Add indicators to the raw_orders_2023 DataFrame
            raw_orders.at[index, 'long_term_pivot'] = pivot_point.values[0]  # Get the first (and only) value
            raw_orders.at[index, 'long_term_support_l1'] = support_l1.values[0]
            raw_orders.at[index, 'long_term_support_l2'] = support_l2.values[0]
            raw_orders.at[index, 'long_term_resistance_l1'] = resistance_l1.values[0]
            raw_orders.at[index, 'long_term_resistance_l2'] = resistance_l2.values[0]

            # Add raw stock data columns for that day
            filtered_data = ticker_data[ticker_data['Date'].dt.strftime('%Y-%m-%d') == execution_date]
            raw_orders.at[index, 'day_high'] = filtered_data['High'].values[0] if not filtered_data.empty else None
            raw_orders.at[index, 'day_low'] = filtered_data['Low'].values[0] if not filtered_data.empty else None
            raw_orders.at[index, 'day_close'] = filtered_data['Close'].values[0] if not filtered_data.empty else None

# Output the modified CSV with new columns added
raw_orders.to_csv('indicators_added.csv', index=False)