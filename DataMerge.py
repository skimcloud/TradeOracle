import os
import pandas as pd
from datetime import datetime

# Constants
TRADE_INPUT_DIRECTORY = 'processed_trade_data.csv'
STOCK_INPUT_DIRECTORY = 'final_stock_data'
AGGREGATED_INDEX_DATA_DIRECTORY = 'aggregated_index_data.csv'
FINAL_OUTPUT_DIRECTORY = 'final_trade_data.csv'

def read_trade_data(file_path):
    return pd.read_csv(file_path)

def convert_date_format(date_string):
    return datetime.strptime(date_string, '%m/%d/%Y').strftime('%Y-%m-%d')

def read_stock_data(ticker, date, stock_directory):
    try:
        file_path = os.path.join(stock_directory, f'{ticker}.csv')
        stock_data = pd.read_csv(file_path)
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        stock_data.set_index('Date', inplace=True)
        return stock_data.loc[date]
    except (FileNotFoundError, KeyError):
        return None

def process_trade_data(trade_data, stock_directory):
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

def append_index_data(trade_data, index_data):
    # Convert the date columns to datetime for proper matching
    trade_data['order_execution_datetime'] = pd.to_datetime(trade_data['order_execution_datetime']).dt.date
    index_data['Date'] = pd.to_datetime(index_data['Date']).dt.date

    # Merge the trade data with the index data based on the date
    merged_data = pd.merge(trade_data, index_data, left_on='order_execution_datetime', right_on='Date', how='left')

    # Drop the extra date column from the index data
    merged_data.drop('Date', axis=1, inplace=True)

    return merged_data

def drop_missing_data(data):
    initial_row_count = len(data)
    data.dropna(inplace=True)
    final_row_count = len(data)
    dropped_rows = initial_row_count - final_row_count
    if dropped_rows > 0:
        print(f"Dropped {dropped_rows} rows due to missing data.")
    else:
        print("No rows dropped, no missing data found.")
    return data

def save_processed_data(data, output_file):
    data.to_csv(output_file, index=False)

# Read trade data
trade_data = read_trade_data(TRADE_INPUT_DIRECTORY)

# Process trade data
processed_trade_data = process_trade_data(trade_data, STOCK_INPUT_DIRECTORY)

# Read the aggregated index data
index_data = pd.read_csv(AGGREGATED_INDEX_DATA_DIRECTORY)

# Append the index data to the processed trade data
final_trade_data_with_index = append_index_data(processed_trade_data, index_data)

# Drop rows with missing data
final_trade_data_with_index = drop_missing_data(final_trade_data_with_index)

# Save the final data
save_processed_data(final_trade_data_with_index, FINAL_OUTPUT_DIRECTORY)

# Indicate completion and output file location
print(f"Processed trade data saved to {FINAL_OUTPUT_DIRECTORY}")

"""

import os
import pandas as pd
from datetime import datetime

# Constants
TRADE_INPUT_DIRECTORY = 'processed_trade_data.csv'
STOCK_INPUT_DIRECTORY = 'final_stock_data'
AGGREGATED_INDEX_DATA_DIRECTORY = 'aggregated_index_data.csv'
FINAL_OUTPUT_DIRECTORY = 'final_trade_data.csv'

def read_trade_data(file_path):
    return pd.read_csv(file_path)

def convert_date_format(date_string):
    return datetime.strptime(date_string, '%m/%d/%Y').strftime('%Y-%m-%d')

def read_stock_data(ticker, date, stock_directory):
    try:
        file_path = os.path.join(stock_directory, f'{ticker}.csv')
        stock_data = pd.read_csv(file_path)
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        stock_data.set_index('Date', inplace=True)
        return stock_data.loc[date]
    except (FileNotFoundError, KeyError):
        return None

def process_trade_data(trade_data, stock_directory):
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

def append_index_data(trade_data, index_data):
    # Convert the date columns to datetime for proper matching
    trade_data['order_execution_datetime'] = pd.to_datetime(trade_data['order_execution_datetime']).dt.date
    index_data['Date'] = pd.to_datetime(index_data['Date']).dt.date

    # Merge the trade data with the index data based on the date
    merged_data = pd.merge(trade_data, index_data, left_on='order_execution_datetime', right_on='Date', how='left')

    # Drop the extra date column from the index data
    merged_data.drop('Date', axis=1, inplace=True)

    return merged_data

def save_processed_data(data, output_file):
    data.to_csv(output_file, index=False)

# Read trade data
trade_data = read_trade_data(TRADE_INPUT_DIRECTORY)

# Process trade data
processed_trade_data = process_trade_data(trade_data, STOCK_INPUT_DIRECTORY)

# Read the aggregated index data
index_data = pd.read_csv(AGGREGATED_INDEX_DATA_DIRECTORY)

# Append the index data to the processed trade data
final_trade_data_with_index = append_index_data(processed_trade_data, index_data)

# Save the final data
save_processed_data(final_trade_data_with_index, FINAL_OUTPUT_DIRECTORY)

print(f"Processed trade data with index data saved to {FINAL_OUTPUT_DIRECTORY}")

"""