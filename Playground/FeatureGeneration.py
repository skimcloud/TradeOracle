import pandas as pd

# Function to calculate 20-day risk-adjusted volatility
def calculate_20_day_volatility(data):
    data['Log_Returns'] = data['Close'].apply(lambda x: pd.np.log(x / x.shift(1)))
    volatility = data['Log_Returns'].tail(20).std()
    annualized_volatility = volatility * pd.np.sqrt(252)
    return annualized_volatility

# Function to calculate moving average delta
def calculate_ma_delta(data, short_window, long_window):
    short_ma = data['Close'].rolling(window=short_window).mean()
    long_ma = data['Close'].rolling(window=long_window).mean()
    return pd.np.log(short_ma / long_ma)

# Function to calculate delta of two volatilities
def calculate_volatility_delta(volatility_1, volatility_2):
    return volatility_1 - volatility_2

# Function to create specified features for a ticker
# Function to create specified features for a ticker
def create_features_for_ticker(ticker):
    file_path = f"Playground/stationary_index_data/{ticker}_data.csv"
    data = pd.read_csv(file_path)

    features = {
        'SPX_HL_20_realVol_20': calculate_20_day_volatility(data['SPX_logDayRange_20']),
        f'{ticker}_logMA5_250': calculate_ma_delta(data, 5, 250),
        'SKEW_MA5': data['SKEW'].rolling(window=5).mean(),
        f'{ticker}_logMA5_20': calculate_ma_delta(data, 5, 20),
        'SKEW_MA20': data['SKEW'].rolling(window=20).mean(),
        f'{ticker}_realVolatility_20': data['Log_Returns'].rolling(window=20).std(),
        f'{ticker}_realVolatility_20_60': calculate_volatility_delta(data['Log_Returns'].rolling(window=20).std(),
                                                                     data['Log_Returns'].rolling(window=60).std()),
        'RUT_logMA5_20': calculate_ma_delta(data, 5, 20),
        'TR10_logMA5_20': calculate_ma_delta(data, 5, 20),
        f'{ticker}_realVolatility_20_60': calculate_volatility_delta(data['Log_Returns'].rolling(window=20).std(),
                                                                      data['Log_Returns'].rolling(window=60).std()),
        f'{ticker}_logD2': data['Close'].apply(lambda x: pd.np.log(x) - pd.np.log(x.shift(2))),
        'SPY_volumeRatio_20': data['Volume'].rolling(window=20).mean(),
        f'{ticker}_logD5': data['Close'].apply(lambda x: pd.np.log(x) - pd.np.log(x.shift(5))),
        f'{ticker}_realVolatility_20_60': calculate_volatility_delta(data['Log_Returns'].rolling(window=20).std(),
                                                                      data['Log_Returns'].rolling(window=60).std()),
        f'{ticker}_logMA20_250': calculate_ma_delta(data, 20, 250),
        f'{ticker}_volumeRatio_250': data['Volume'].rolling(window=250).mean(),
        'TR10_TR1': data['TR10Y_Close'] - data['TR1Y_Close'],
        f'{ticker}_dayRangeRatio_250': (data['High'] - data['Low']).rolling(window=250).mean(),
        # Additional features for specific tickers
        'GLD_logMA5_250': calculate_ma_delta(data, 5, 250),  # Example additional feature
        'GLD_logMA5_20': calculate_ma_delta(data, 5, 20),  # Additional feature
        'GLD_realVolatility_20': data['GLD_logD1'].rolling(window=20).std(),  # Additional feature
        'GLD_realVolatility_20_60': calculate_volatility_delta(data['GLD_logD1'].rolling(window=20).std(),
                                                               data['GLD_logD1'].rolling(window=60).std()),  # Additional feature
        'GLD_logDayRet': data['GLD_Close'].apply(lambda x: pd.np.log(x) - pd.np.log(x.shift(1))),  # Additional feature
        'GLD_volumeRatio_250': data['Volume'].rolling(window=250).mean(),  # Additional feature
        'GLD_logD5': data['GLD_Close'].apply(lambda x: pd.np.log(x) - pd.np.log(x.shift(5))),  # Additional feature
        'GLD_realVolatility_20_60': calculate_volatility_delta(data['GLD_logD1'].rolling(window=20).std(),
                                                               data['GLD_logD1'].rolling(window=60).std()),  # Additional feature
        # Continue adding other features as needed
    }

    return features

# List of tickers
raw_orders = pd.read_csv('raw_orders.csv')
# Iterate through unique tickers
unique_tickers = raw_orders['ticker'].unique()
all_features = {}
# Generating features for each ticker
for ticker in unique_tickers:
    all_features[ticker] = create_features_for_ticker(ticker)

# 'all_features' will contain dictionaries of features for each ticker
# You can access them like: all_features['SPX']['SPX_HL_20_realVol_20']
for ticker, features in all_features.items():
    print(f"Ticker: {ticker}")
    for key, value in features.items():
        print(f"Key: {key}")
        print(f"Value: {value}")
        print("-" * 20)  # Separating each key-value pair for clarity
    print("=" * 30)  # Separating each ticker's features

