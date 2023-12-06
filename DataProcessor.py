import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Load the CSV file
data = pd.read_csv('indicators_added.csv')

# Drop the 'trader' column
data.drop('trader', axis=1, inplace=True)

# Numerically encode non-numeric columns
non_numeric_columns = data.select_dtypes(exclude=['number']).columns
label_encoders = {}
for col in non_numeric_columns:
    label_encoders[col] = LabelEncoder()
    data[col] = label_encoders[col].fit_transform(data[col])

# Normalize numeric columns
numeric_columns = data.select_dtypes(include=['number']).columns
scaler = MinMaxScaler()
data[numeric_columns] = scaler.fit_transform(data[numeric_columns])

# Output the final dataset to a new CSV file
data.to_csv('final_dataset.csv', index=False)
