import os
import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.tsa.arima.model import ARIMA

# Define the function fracDiff_FFD
def getWeights_FFD(d, thres):
    w = [1.]
    for k in range(1, 100):
        w_ = -w[-1] * (d - k + 1) / k
        if abs(w_) < thres:
            break
        w.append(w_)
    w = np.array(w[::-1]).reshape(-1, 1)
    return w

def fracDiff_FFD(series, d, thres=1e-5):
    w = getWeights_FFD(d, thres)
    width = len(w) - 1
    df = {}
    for name in series.columns:
        seriesF, df_ = series[[name]].fillna(method='ffill').dropna(), pd.Series()
        for iloc1 in range(width, seriesF.shape[0]):
            loc0, loc1 = seriesF.index[iloc1 - width], seriesF.index[iloc1]
            if not np.isfinite(series.loc[loc1, name]):
                continue  # exclude NAs
            df_[loc1] = np.dot(w.T, seriesF.loc[loc0:loc1])[0, 0]
        df[name] = df_.copy(deep=True)
    df = pd.concat(df, axis=1)
    return df

# Directory containing CSV files
data_directory = 'Playground/three_year_stock_data'
output_directory = 'Playground/stationary_stock_data'

# Create a new directory for output if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through CSV files in the data directory
for filename in os.listdir(data_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_directory, filename)
        ticker = filename.split('_data')[0]  # Extract ticker from filename
        
        # Load CSV file
        data = pd.read_csv(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        
        # Perform fractional differentiation for 'Open', 'Adj Close', 'Volume', 'High', and 'Low' columns
        frac_diff_order = 0.5  # Set the fractional differencing order
        columns_to_diff = ['Open', 'Adj Close', 'Volume', 'High', 'Low']
        result = fracDiff_FFD(data[columns_to_diff], frac_diff_order)
        
        # Make sure the lengths match after fractional differentiation
        min_length = min(len(data), len(result))
        data = data[:min_length]
        result = result[:min_length]
        
        # Include the 'Date' column in the fractionally differentiated DataFrame
        result.insert(0, 'Date', data.index)
        
        # Save fractionally differentiated columns to a new CSV file
        output_filename = f"{ticker}_diff_prices.csv"
        output_path = os.path.join(output_directory, output_filename)
        result.to_csv(output_path, index=False)  # Avoid saving the index
        
        # Fit probability distributions (normal and log-normal) to fractionally differentiated columns
        distributions_info = {}
        for col in columns_to_diff:
            values = result[col].dropna()
            
            # Convert values to float if possible
            values = pd.to_numeric(values, errors='coerce')
            values = values[np.isfinite(values)]
            
            if len(values) > 0:
                # Fit a normal distribution
                params_norm = stats.norm.fit(values)
                mean_norm, std_dev_norm = params_norm[:2]
                
                # Fit a log-normal distribution
                positive_values = values[values > 0]
                if len(positive_values) > 0:
                    params_lognorm = stats.lognorm.fit(positive_values)
                    shape_lognorm, loc_lognorm, scale_lognorm = params_lognorm
                    
                    # Store distribution parameters in a dictionary
                    distributions_info[col] = {
                        'Mean': mean_norm,
                        'Variance': std_dev_norm ** 2,
                        'Skewness': stats.skew(values),
                        'Kurtosis': stats.kurtosis(values),
                        'Shape': shape_lognorm,
                        'Location': loc_lognorm,
                        'Scale': scale_lognorm
                    }
        # Save distribution parameters to a new file
        output_dist_filename = f"{ticker}_distribution.csv"
        output_dist_path = os.path.join(output_directory, output_dist_filename)
        pd.DataFrame(distributions_info).to_csv(output_dist_path)

        # Extract 'Adj Close' prices
        close_prices = data['Adj Close'].dropna()
        
        # Fit ARIMA model to 'Adj Close' prices
        model = ARIMA(close_prices, order=(1, 0, 1))  # Example ARIMA order (p, d, q)
        model_fit = model.fit()
        
        # Save ARIMA model coefficients to a CSV file
        output_arima_filename = f"{ticker}_arima_coeffients.csv"
        output_arima_path = os.path.join(output_directory, output_arima_filename)
        pd.DataFrame(model_fit.params).to_csv(output_arima_path)