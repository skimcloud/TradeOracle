import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import logging

INDEX_INPUT_DIRECTORY = 'raw_index_data'
INDEX_OUTPUT_DIRECTORY = 'processed_index_data'

STOCK_INPUT_DIRECTORY = 'raw_stock_data'
STOCK_OUTPUT_DIRECTORY = 'processed_stock_data'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_weights_ffd(d, thres):
    w = [1.]
    for k in range(1, 100):
        w_ = -w[-1] * (d - k + 1) / k
        if abs(w_) < thres:
            break
        w.append(w_)
    w = np.array(w[::-1]).reshape(-1, 1)
    return w

def frac_diff_ffd(series, d, thres=1e-5):
    w = get_weights_ffd(d, thres)
    width = len(w) - 1
    df = {}
    for name in series.columns:
        seriesF, df_ = series[[name]].ffill().dropna(), pd.Series()
        for iloc1 in range(width, seriesF.shape[0]):
            loc0, loc1 = seriesF.index[iloc1 - width], seriesF.index[iloc1]
            if not np.isfinite(series.loc[loc1, name]):
                continue  # exclude NAs
            df_[loc1] = np.dot(w.T, seriesF.loc[loc0:loc1])[0, 0]
        df[name] = df_.copy(deep=True)
    df = pd.concat(df, axis=1)
    return df

def differentiate_prices(file_path, directory):
    """
    Process stock data by performing fractional differentiation.
    """
    try:
        ticker = os.path.basename(file_path).split('.')[0]

        # Load CSV file
        data = pd.read_csv(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        # Perform fractional differentiation
        frac_diff_order = 0.5
        columns_to_diff = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        result = frac_diff_ffd(data[columns_to_diff], frac_diff_order)

        # Add the 'Date' column to the left side
        result.insert(0, 'Date', result.index)

        # Reset the index to make 'Date' a column again
        result.reset_index(drop=True, inplace=True)

        # Save fractionally differentiated data
        result.to_csv(os.path.join(directory, f"{ticker}.csv"), index=False)

        logging.info(f"Processed and saved data for {ticker}")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")

# Process each Index and Stock CSV file
if __name__ == "__main__":
    if not os.path.exists(INDEX_OUTPUT_DIRECTORY):
        os.makedirs(INDEX_OUTPUT_DIRECTORY)
    for filename in os.listdir(INDEX_INPUT_DIRECTORY):
        if filename.endswith('.csv'):
            file_path = os.path.join(INDEX_INPUT_DIRECTORY, filename)
            differentiate_prices(file_path, INDEX_OUTPUT_DIRECTORY)

    if not os.path.exists(STOCK_OUTPUT_DIRECTORY):
        os.makedirs(STOCK_OUTPUT_DIRECTORY)
    for filename in os.listdir(STOCK_INPUT_DIRECTORY):
        if filename.endswith('.csv'):
            file_path = os.path.join(STOCK_INPUT_DIRECTORY, filename)
            differentiate_prices(file_path, STOCK_OUTPUT_DIRECTORY)