import pandas as pd
from datetime import datetime
import os

# Directory paths
CLOSED_OUTPUT_DIRECTORY = 'processed_trade_data.csv'
STOCK_DATA_DIRECTORY = 'final_stock_data'
FINAL_OUTPUT_DIRECTORY = 'final_trade_data.csv'

# Function to convert date format in processed_trade_data to match that in stock data files
def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%Y %I:%M %p')
    return date_obj.strftime('%Y-%m-%d')

# Read processed trade data
processed_trade_data = pd.read_csv(CLOSED_OUTPUT_DIRECTORY)
processed_trade_data['trade_date'] = processed_trade_data['order_execution_datetime'].apply(convert_date_format)

# Initialize a list to hold combined data
combined_data = []

# Determine the columns for the final combined dataset
final_columns = processed_trade_data.columns.tolist() + ['stock_data_found'] + ['stock_' + col for col in pd.read_csv(os.path.join(STOCK_DATA_DIRECTORY, 'AAPL.csv')).columns]

# Loop through each trade in processed_trade_data
for index, trade in processed_trade_data.iterrows():
    ticker = trade['ticker']
    trade_date = trade['trade_date']

    # Construct path to the ticker's CSV file in final_stock_data
    ticker_file_path = os.path.join(STOCK_DATA_DIRECTORY, f"{ticker}.csv")

    # Initialize a row with NaNs for stock data
    combined_row = pd.Series([None] * len(final_columns), index=final_columns)
    combined_row[processed_trade_data.columns] = trade

    # Check if the ticker's file exists
    if os.path.exists(ticker_file_path):
        stock_data = pd.read_csv(ticker_file_path)
        
        # Find the stock data for the matching date
        matching_stock_data = stock_data[stock_data['Date'] == trade_date]

        # If matching data is found, combine it with the trade data
        if not matching_stock_data.empty:
            for col in matching_stock_data.columns:
                combined_row['stock_' + col] = matching_stock_data.iloc[0][col]
            combined_row['stock_data_found'] = True
        else:
            combined_row['stock_data_found'] = False

    # Append the combined row to the list
    combined_data.append(combined_row)

# Concatenate all combined rows into a dataframe
final_trade_data = pd.DataFrame(combined_data)

# Save the combined data to a new CSV file
final_trade_data.to_csv(FINAL_OUTPUT_DIRECTORY, index=False)
