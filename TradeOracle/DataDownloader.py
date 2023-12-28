import os
import pandas as pd
import yfinance as yf
import datetime
import logging

INDEX_OUTPUT_DIRECTORY = 'raw_index_data'
STOCK_OUTPUT_DIRECTORY = 'raw_stock_data'
TRADE_DATA_DIRECTORY = 'processed_trade_data.csv'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def download_ticker_data(tickers, start_date, end_date, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            data.to_csv(f'{folder}/{ticker}.csv')
            logging.info(f"Data for {ticker} downloaded successfully.")
        except Exception as e:
            logging.error(f"Error downloading data for {ticker}: {e}")

if __name__ == "__main__":
    indexes = ['SPY', '^RUT', 'GLD', '^VIX', '^VVIX', '^SKEW', '^TNX']
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365*5)).strftime('%Y-%m-%d')
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    download_ticker_data(indexes, start_date, end_date, INDEX_OUTPUT_DIRECTORY)

    trades = pd.read_csv(TRADE_DATA_DIRECTORY)
    stocks = trades['ticker'].unique()
    download_ticker_data(stocks, start_date, end_date, STOCK_OUTPUT_DIRECTORY)