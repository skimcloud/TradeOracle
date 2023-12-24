import os
import pandas as pd
import numpy as np

# Create a new directory to store the output files
output_directory = 'Playground/Processed_Index_Data'
os.makedirs(output_directory, exist_ok=True)

# Function to calculate indicators
def calculate_indicators(file_path):
    data = pd.read_csv(file_path)
    ticker = file_path.split('\\')[-1].split('_')[0]
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)


    # Calculating Moving Averages
    data['MA_5'] = data['Adj Close'].rolling(window=5, min_periods=5).mean()
    data['MA_20'] = data['Adj Close'].rolling(window=20, min_periods=20).mean()
    #data['MA_33'] = data['Adj Close'].rolling(window=33).mean()
    #data['MA_89'] = data['Adj Close'].rolling(window=89).mean()
    #data['MA_233'] = data['Adj Close'].rolling(window=233).mean()
    data['MA_250'] = data['Adj Close'].rolling(window=250, min_periods=250).mean()

    # Calculating Volatility
    data['realVolatility20'] = data['Adj Close'].rolling(window=20, min_periods=20).std()
    data['realVolatility60'] = data['Adj Close'].rolling(window=60, min_periods=60).std()
    data['realVolatility250'] = data['Adj Close'].rolling(window=250, min_periods=250).std()
    
    # Average Volume
    data['avgVolume_20'] = data['Volume'].rolling(window=20, min_periods=20).mean()
    data['avgVolume_60'] = data['Volume'].rolling(window=60, min_periods=60).mean()
    data['avgVolume_250'] = data['Volume'].rolling(window=250, min_periods=250).mean()
    
    # Calculating the single-day logarithmic return involves taking the logarithm of close / open
    data['log1DayRet'] = np.log(data['Adj Close'] / data['Open'])
    data['logMA5_20'] = np.log(data['MA_5'] / data['MA_20'])
    data['logMA20_250'] = np.log(data['MA_20'] / data['MA_250'])
    data['logMA5_250'] = np.log(data['MA_5'] / data['MA_250'])
    
    # Calculate the absolute difference between 'High' and 'Low'
    absolute_diff = np.abs(data['High'] - data['Low'])

    # Apply the logarithm to the absolute difference 
    data['log1DayRange'] = np.log(absolute_diff)

    # Calculate HL_20_realVol_20 or any other desired calculations
    data['HL_20_realVol_20'] = data['log1DayRange'].rolling(window=20).std()
    data['HL_5_realVol_20'] = data['log1DayRange'].rolling(window=5).std()

    # Calculate two-day logarithmic difference
    absolute_diffD2 = np.abs(data['Adj Close'] - data['Adj Close'].shift(2))
    data['logD2'] = np.log(absolute_diffD2)

    # Calculate five-day logarithmic difference
    absolute_diffD5 = np.abs(data['Adj Close'] - data['Adj Close'].shift(5))
    data['logD5'] = np.log(absolute_diffD5)

    prefix = f'{ticker}_'
    data.columns = [prefix + col for col in data.columns]
    # Saving the updated data to a new CSV file
    output_file = os.path.join(output_directory, os.path.basename(file_path))
    data.to_csv(output_file, index=True)

# Define the directory containing the files
directory = 'Playground/stationary_index_data'

# Get all files ending with 'prices.csv' in the specified directory
files = [f for f in os.listdir(directory) if f.endswith('prices.csv')]

# Loop through each file and calculate indicators
for file in files:
    file_path = os.path.join(directory, file)
    calculate_indicators(file_path)