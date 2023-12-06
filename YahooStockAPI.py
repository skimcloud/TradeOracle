import os
import pandas as pd
import yfinance as yf

# Create a subfolder if it doesn't exist
if not os.path.exists('yahoo_price_data'):
    os.makedirs('yahoo_price_data')

# Read the raw_orders_2023 CSV file
raw_orders = pd.read_csv('raw_orders_2023.csv')

# Function to calculate support and resistance levels
def calculate_support_resistance(data):
    pivot_point = (data['High'] + data['Low'] + data['Close']) / 3
    support_l1 = (pivot_point * 2) - data['High']
    support_l2 = pivot_point - (data['High'] - data['Low'])
    resistance_l1 = (pivot_point * 2) - data['Low']
    resistance_l2 = pivot_point + (data['High'] - data['Low'])
    
    return pivot_point, support_l1, support_l2, resistance_l1, resistance_l2

# Iterate through unique tickers
unique_tickers = raw_orders['ticker'].unique()
for ticker in unique_tickers:
    # Specify the date range
    start_date = '2022-12-01'
    end_date = '2023-11-27'
    
    # Retrieve historical price data using yfinance
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Save stock data to indicator_data subfolder
    stock_data.to_csv(f'yahoo_price_data/{ticker}_data.csv')
