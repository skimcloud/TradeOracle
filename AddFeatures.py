import os
import pandas as pd
from datetime import datetime

# Constants
TRADE_INPUT_DIRECTORY = 'processed_trade_data.csv'
STOCK_INPUT_DIRECTORY = 'final_stock_data'
FINAL_OUTPUT_DIRECTORY = 'final_trade_data.csv'

def read_trade_data(file_path):
    """Reads the trade data from a CSV file."""
    return pd.read_csv(file_path)

def convert_date_format(date_string):
    """Converts the date format from MM/DD/YYYY to YYYY-MM-DD."""
    return datetime.strptime(date_string, '%m/%d/%Y').strftime('%Y-%m-%d')

def read_stock_data(ticker, date, stock_directory):
    """Reads stock data for a specific ticker and date."""
    try:
        file_path = os.path.join(stock_directory, f'{ticker}.csv')
        stock_data = pd.read_csv(file_path)
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        stock_data.set_index('Date', inplace=True)
        return stock_data.loc[date]
    except (FileNotFoundError, KeyError):
        return None

def process_trade_data(trade_data, stock_directory):
    """Processes the trade data by appending stock features."""
    feature_columns = [
        'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume',
        'MA_5', 'MA_20', 'MA_250', 'realVolatility20', 'realVolatility60', 'realVolatility250',
        'avgVolume_20', 'avgVolume_60', 'avgVolume_250', 'log1DayRet', 'logMA5_20', 'logMA20_250', 
        'logMA5_250', 'log1DayRange', 'HL_20_realVol_20', 'HL_5_realVol_20', 'logD2', 'logD5',
        'Mean', 'Variance', 'Skewness', 'Kurtosis', 'Shape', 'Location', 'Scale'
    ]

    updated_trade_data = []

    for index, row in trade_data.iterrows():
        trade_date = convert_date_format(row['order_execution_datetime'].split(' ')[0])
        ticker = row['ticker']
        stock_features = read_stock_data(ticker, trade_date, stock_directory)

        if stock_features is not None:
            # Flatten the concatenated Series into a single Series
            updated_row = pd.concat([row, stock_features[feature_columns]]).to_frame().T
            updated_trade_data.append(updated_row)
        else:
            print(f"Data for {ticker} on {trade_date} not found.")

    return pd.concat(updated_trade_data, ignore_index=True)


def save_processed_data(data, output_file):
    """Saves the processed data to a CSV file."""
    data.to_csv(output_file, index=False)

# Read trade data
trade_data = read_trade_data(TRADE_INPUT_DIRECTORY)

# Process trade data
processed_trade_data = process_trade_data(trade_data, STOCK_INPUT_DIRECTORY)

# Save processed data
save_processed_data(processed_trade_data, FINAL_OUTPUT_DIRECTORY)

# Indicate completion and output file location
print(f"Processed trade data saved to {FINAL_OUTPUT_DIRECTORY}")