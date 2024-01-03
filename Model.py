import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load the dataset
FILE_PATH = 'merged_dataset.csv'  # Replace with your dataset path
data = pd.read_csv(FILE_PATH)

# Dropping specified columns
data = data.drop(columns=['comment', 'trader', 'exit_price', 'comment', 'profit', 'entry_price', 'DT_OPEX'])

# Encoding 'order_execution_datetime' and 'expiration' as ordinal values
data['order_execution_datetime'] = pd.to_datetime(data['order_execution_datetime']).astype('int64')
data['expiration'] = pd.to_datetime(data['expiration']).astype('int64')

# Applying One-Hot Encoding to 'ticker'
column_transformer = ColumnTransformer(
    [("ticker_ohe", OneHotEncoder(sparse=False, handle_unknown='ignore'), ['ticker'])],
    remainder='passthrough'
)

# Prepare data for modeling
X = data.drop(columns=['success'])  # Replace 'target_column' with your target column
y = data['success']  # Replace 'target_column' with your target column

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Applying the Column Transformer to the dataset
X_train = column_transformer.fit_transform(X_train)
X_test = column_transformer.transform(X_test)

# Training the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions and performance evaluation
y_pred = model.predict(X_test)

# Print the confusion matrix
confusion = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(confusion)

# Print classification report and accuracy
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))
