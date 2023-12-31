import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np

# Load the dataset
FILE_PATH = 'merged_dataset.csv'  # Replace with your dataset path
data = pd.read_csv(FILE_PATH)

# Dropping specified columns
data = data.drop(columns=['trader', 'exit_price', 'contract_details', 'profit', 'entry_price'])

# Encoding 'order_execution_datetime' and 'expiration' as ordinal values
data['order_execution_datetime'] = pd.to_datetime(data['order_execution_datetime']).astype('int64')
data['expiration'] = pd.to_datetime(data['expiration']).astype('int64')

# Applying One-Hot Encoding to 'ticker'
column_transformer = ColumnTransformer(
    [("ticker_ohe", OneHotEncoder(sparse=False, handle_unknown='ignore'), ['ticker'])],
    remainder='passthrough'
)

# Prepare data for modeling
X = data.drop('success', axis=1)
y = data['success'].astype(int)

X_transformed = column_transformer.fit_transform(X)

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.3, random_state=42)

# Random Forest Classifier
rf = RandomForestClassifier(n_estimators=100)

# Training the model
rf.fit(X_train, y_train)

# Making predictions
y_pred = rf.predict(X_test)

# Evaluating the model
report = classification_report(y_test, y_pred)
print(report)

# Get feature importances
feature_importances = rf.feature_importances_

# Get feature names after transformation
ohe_feature_names = column_transformer.named_transformers_['ticker_ohe'].get_feature_names_out()
other_feature_names = [col for col in data.columns if col != 'ticker' and col != 'success']
feature_names = np.concatenate((ohe_feature_names, other_feature_names))

# Match features with their names and sort
feature_weights = sorted(zip(feature_names, feature_importances), key=lambda x: x[1], reverse=True)

# Print top 10 features
print("Top 10 Features:")
for feature, weight in feature_weights[:10]:
    print(f"{feature}: {weight}")