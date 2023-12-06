import os
import pandas as pd

# Read the raw_orders_2023 CSV file
raw_orders = pd.read_csv('entries_matched_2023.csv')

# Function to calculate support and resistance levels
def calculate_support_resistance(data):
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
        
        # Filter data for the specific execution date
        filtered_data = ticker_data[ticker_data['Date'].dt.strftime('%Y-%m-%d') == execution_date]
        
        if not filtered_data.empty:
            # Calculate support and resistance levels
            pivot_point, support_l1, support_l2, resistance_l1, resistance_l2 = calculate_support_resistance(filtered_data)
            
            # Add indicators to the raw_orders_2023 DataFrame
            raw_orders.at[index, 'pivot_point'] = pivot_point.values[0]  # Get the first (and only) value
            raw_orders.at[index, 'support_l1'] = support_l1.values[0]
            raw_orders.at[index, 'support_l2'] = support_l2.values[0]
            raw_orders.at[index, 'resistance_l1'] = resistance_l1.values[0]
            raw_orders.at[index, 'resistance_l2'] = resistance_l2.values[0]

# Output the modified CSV with new columns added
raw_orders.to_csv('indicators_added.csv', index=False)
