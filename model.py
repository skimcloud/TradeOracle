import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, recall_score
import matplotlib.pyplot as plt
from xgboost import plot_tree
import seaborn as sns

# Load the dataset
data = pd.read_csv('processed_dataset.csv')

# Define features and target variable
features = data.drop('success', axis=1)
target = data['success']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# Initialize the XGBoost Classifier with hyperparameters
clf = XGBClassifier(random_state=42, max_depth=5, min_child_weight=1, learning_rate=0.1, n_estimators=100)

# Fit the classifier to the training data
clf.fit(X_train, y_train)

# Cross-validation
cv_scores = cross_val_score(clf, features, target, cv=5)
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean CV Accuracy: {cv_scores.mean() * 100:.2f}%")

# Predict on the test data
predictions = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Get feature importances
feature_importances = clf.feature_importances_

# Create a DataFrame to hold features and their importance scores
feature_importance_df = pd.DataFrame({'Feature': features.columns, 'Importance': feature_importances})

# Sort features by importance score in descending order
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Print top N important features
top_n = 10  # Change this value to print more or fewer top features
print(f"Top {top_n} Important Features:")
print(feature_importance_df.head(top_n))

# Calculate and print recall
recall = recall_score(y_test, predictions)
print(f"Recall: {recall * 100:.2f}%")

# Visualize the XGBoost Decision Tree
plt.figure(figsize=(12, 8))
plot_tree(clf, num_trees=0, ax=plt.gca())
plt.show()


