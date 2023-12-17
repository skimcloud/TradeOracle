import os
import pandas as pd

# Directory containing CSV files
data_directory = 'stationary_index_data'
# Loop through CSV files in the data directory
for filename in os.listdir(data_directory):
    if filename.endswith('prices.csv'):
        file_path = os.path.join(data_directory, filename)
        ticker = filename.split('_diff_prices')[0]  # Extract ticker from filename
        
        # Load CSV file
        data = pd.read_csv(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        
        # Calculate moving averages (33, 89, 125, 233) based on the 'Close' price
        close_prices = data['Adj Close']
        data['MA_33'] = close_prices.rolling(window=33).mean()
        data['MA_89'] = close_prices.rolling(window=89).mean()
        data['MA_233'] = close_prices.rolling(window=233).mean()
        
        # Update the CSV file with the moving averages
        data.to_csv(file_path)