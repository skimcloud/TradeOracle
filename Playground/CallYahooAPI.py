import os
import pandas as pd
import yfinance as yf

# Create a subfolder if it doesn't exist
if not os.path.exists('Playground/raw_index_data'):
    os.makedirs('Playground/raw_index_data')


# Iterate through unique tickers
#unique_tickers = ['^VIX', '^VVIX', '^RVX', 'HYG', 'SPY', '^SKEW', 'GLD', 'HYG', 'QQQ', 'EURUSD=X', 'ES=F', 'YM=F', 'UVXY', '^MXX', '^XAX', '^GDAXI', '^BUK100P', '^KS11', 'LE=F', 'GBPUSD=X', 'BTC-USD', '^N225', 'JPY=X', '^SPX', '^DJI', '^NYA', '^IXIC', '^NDX', '^RUI', '^RUT', '^RUA', '^GSPC', '^GSPTSE', '^FTSE', '^FTMC', '^FTAS', 'DAX', '^AFLI', '^AORD', '^HSI', '^STI', '^KLSE', '^NSEI', '^NSMIDCP', '^CRSLDX', 'GC=F', 'CL=F', 'HO=F', 'BZ=F', 'BOIL', 'QM=F', 'NG=F', 'LE=F', '^TNX', 'UGA', 'CT=F', 'RB=F', 'ZW=F', 'SI=F', 'PL=F', 'HG=F', 'ZC=F']
unique_tickers = ['^VIX', '^VVIX']
for ticker in unique_tickers:
    # Specify the date range
    start_date = '2019-11-18'
    end_date = '2023-12-17'
    
    # Retrieve historical price data using yfinance
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Save stock data to indicator_data subfolder
    stock_data.to_csv(f'Playground/raw_index_data/{ticker}_data.csv')
