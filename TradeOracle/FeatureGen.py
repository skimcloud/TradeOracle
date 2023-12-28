import os
import pandas as pd
import numpy as np
import scipy.stats as stats

# Constants
INDEX_INPUT_DIRECTORY = 'processed_index_data'
INDEX_OUTPUT_DIRECTORY = 'final_index_data'
INDEX_AGGREGATED_OUTPUT_NAME = 'aggregated_index_data.csv'

STOCK_INPUT_DIRECTORY = 'processed_stock_data'
STOCK_OUTPUT_DIRECTORY = 'final_stock_data'

# Create the output directory if it doesn't exist
os.makedirs(INDEX_OUTPUT_DIRECTORY, exist_ok=True)
os.makedirs(STOCK_OUTPUT_DIRECTORY, exist_ok=True)

def calculate_distribution_parameters(data):
    """Calculate normal and log-normal distribution parameters."""
    values = data['Adj Close'].dropna()
    mean_norm, std_dev_norm = np.mean(values), np.std(values)
    shape_lognorm, loc_lognorm, scale_lognorm = stats.lognorm.fit(values)

    return {
        'Mean': mean_norm,
        'Variance': std_dev_norm ** 2,
        'Skewness': stats.skew(values),
        'Kurtosis': stats.kurtosis(values),
        'Shape': shape_lognorm,
        'Location': loc_lognorm,
        'Scale': scale_lognorm
    }

def calculate_moving_averages(data, ticker_prefix):
    """Calculate various moving averages and append them to the dataframe."""
    data[ticker_prefix + 'MA_5'] = data['Adj Close'].rolling(window=5, min_periods=5).mean()
    data[ticker_prefix + 'MA_20'] = data['Adj Close'].rolling(window=20, min_periods=20).mean()
    data[ticker_prefix + 'MA_250'] = data['Adj Close'].rolling(window=250, min_periods=250).mean()

def calculate_volatility(data, ticker_prefix):
    """Calculate volatility."""
    data[ticker_prefix + 'realVolatility20'] = data['Adj Close'].rolling(window=20, min_periods=20).std()
    data[ticker_prefix + 'realVolatility60'] = data['Adj Close'].rolling(window=60, min_periods=60).std()
    data[ticker_prefix + 'realVolatility250'] = data['Adj Close'].rolling(window=250, min_periods=250).std()

def calculate_volume(data, ticker_prefix):
    """Calculate average volume indicators."""
    if not (data['Volume'] == 0).all(): # For SKEW, VIX, etc...no volume
        data[ticker_prefix + 'avgVolume_20'] = data['Volume'].rolling(window=20, min_periods=20).mean()
        data[ticker_prefix + 'avgVolume_60'] = data['Volume'].rolling(window=60, min_periods=60).mean()
        data[ticker_prefix + 'avgVolume_250'] = data['Volume'].rolling(window=250, min_periods=250).mean()

def calculate_logarithmic_returns(data, ticker_prefix):
    """Calculate logarithmic returns and related indicators."""
    if np.all(data['Adj Close'] != data['Open']): # Check if all values in Adj Close are equal to Open For skew
        data[ticker_prefix + 'log1DayRet'] = np.log(np.abs(data['Adj Close'] / data['Open']))
    data[ticker_prefix + 'logMA5_20'] = np.log(np.abs(data[ticker_prefix + 'MA_5'] / data[ticker_prefix + 'MA_20']))
    data[ticker_prefix + 'logMA20_250'] = np.log(np.abs(data[ticker_prefix + 'MA_20'] / data[ticker_prefix + 'MA_250']))
    data[ticker_prefix + 'logMA5_250'] = np.log(np.abs(data[ticker_prefix + 'MA_5'] / data[ticker_prefix + 'MA_250']))
    absolute_diffD2 = np.abs(data['Adj Close'] - data['Adj Close'].shift(2))
    data[ticker_prefix + 'logD2'] = np.log(absolute_diffD2)
    absolute_diffD5 = np.abs(data['Adj Close'] - data['Adj Close'].shift(5))
    data[ticker_prefix + 'logD5'] = np.log(absolute_diffD5)

def calculate_additional_indicators(data, ticker_prefix):
    """Calculate additional indicators such as HL_20_realVol_20."""
    if np.all(data['High'] != data['Low']): # Check if all values in High are equal to High
        data[ticker_prefix + 'log1DayRange'] = np.log(np.abs(data['High'] - data['Low']))
        data[ticker_prefix + 'HL_20_realVol_20'] = data[ticker_prefix + 'log1DayRange'].rolling(window=20).std()
        data[ticker_prefix + 'HL_5_realVol_20'] = data[ticker_prefix + 'log1DayRange'].rolling(window=5).std()

def generate_features(file_path, output_directory):
    """Process each file and save the results."""
    data = pd.read_csv(file_path)
    ticker = file_path.split('\\')[-1].split('_')[0]

    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

    ticker_prefix = f'{ticker}_'
    calculate_moving_averages(data, ticker_prefix)
    calculate_volatility(data, ticker_prefix)
    calculate_volume(data, ticker_prefix)
    calculate_logarithmic_returns(data, ticker_prefix)
    calculate_additional_indicators(data, ticker_prefix)

    # Calculate distribution parameters
    distribution_params = calculate_distribution_parameters(data)
    for key, value in distribution_params.items():
        data[ticker_prefix + key] = value

    # Drop columns with all values as "0.0"
    data = data.loc[:, (data != 0.0).any(axis=0)]

    # Save the updated data to a new CSV file
    output_file = os.path.join(output_directory, os.path.basename(file_path))
    # Delete the first 250 rows
    data = data.iloc[250:]
    data.to_csv(output_file, index=True)

def merge_files_based_on_date(directory):
    columns_to_drop = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    merged_df = pd.DataFrame()
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        df['Date'] = pd.to_datetime(df['Date'])
        # Drop specified columns if they exist in the DataFrame
        df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)
        if merged_df.empty:
            merged_df = df
        else:
            file_identifier = os.path.splitext(os.path.basename(file_path))[0]
            merged_df = pd.merge(merged_df, df, on='Date', how='outer', suffixes=('', f'_{file_identifier}'))
    merged_df.to_csv(INDEX_AGGREGATED_OUTPUT_NAME, index=False)
    
if __name__ == "__main__":
    for file in os.listdir(INDEX_INPUT_DIRECTORY):
        file_path = os.path.join(INDEX_INPUT_DIRECTORY, file)
        generate_features(file_path, INDEX_OUTPUT_DIRECTORY)

    for file in os.listdir(STOCK_INPUT_DIRECTORY):
        file_path = os.path.join(STOCK_INPUT_DIRECTORY, file)
        generate_features(file_path, STOCK_OUTPUT_DIRECTORY)

    merge_files_based_on_date(INDEX_OUTPUT_DIRECTORY)
