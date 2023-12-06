import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('prices_with_order.csv')

# Ensure 'order_execution_datetime' is in datetime format
df['order_execution_datetime'] = pd.to_datetime(df['order_execution_datetime'])

# Convert 'order_execution_datetime' to Unix timestamp (numeric value)
df['order_execution_datetime'] = (df['order_execution_datetime'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')


# Encode ticker as a numeric value
label_encoder = LabelEncoder()
df['ticker'] = label_encoder.fit_transform(df['ticker'])

# Encode expiration as numeric value
df['expiration'] = df['expiration'].apply(lambda x: int(x.replace('/', '')))

# Encode contract details with a numeric value
df['contract_details'] = label_encoder.fit_transform(df['contract_details'])

# Encode timeframe as numeric value (0 for scalp, 1 for swing)
df['timeframe'] = df['timeframe'].map({'SCALP': 0, 'SWING': 1})

# Encode 'success' column to integer
df['success'] = df['success'].map({0.0: 0, 1.0: 1})

# Normalize 'open', 'high', 'low', 'volume' columns
columns_to_normalize = ['open_' + str(i) for i in range(1, 181)] + ['high_' + str(i) for i in range(1, 181)] + ['low_' + str(i) for i in range(1, 181)] + ['volume_' + str(i) for i in range(1, 181)]
scaler = MinMaxScaler()
df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])

# Drop 'direction' column
df.drop(['direction'], axis=1, inplace=True)

# Drop 'trader' and 'comment' columns
df.drop(['trader', 'comment'], axis=1, inplace=True)

# Display the modified DataFrame
print(df.head())

# Save the modified DataFrame to a new CSV file
df.to_csv('processed_dataset.csv', index=False)