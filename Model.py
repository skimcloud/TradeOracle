import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('final_dataset.csv')

# Calculate the correlation matrix
correlation_matrix = data.drop(['direction'], axis=1).corr()

# Plotting the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 8})
plt.title("Pearson Correlation Matrix Heatmap")
plt.tight_layout()
plt.show()

# Define features and target variable
features = data.drop(['success'], axis=1)
target = data['success']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# Initialize the Random Forest classifier with hyperparameters
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Fit the classifier to the training data
clf.fit(X_train, y_train)

# Cross-validation
cv_scores = cross_val_score(clf, features, target, cv=6)
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean CV Accuracy: {cv_scores.mean() * 100:.2f}%")

# Predict on the test data
predictions = clf.predict(X_test)

# Calculate and print accuracy, recall, and precision
accuracy = accuracy_score(y_test, predictions)
recall = recall_score(y_test, predictions)
precision = precision_score(y_test, predictions)

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")

# Confusion matrix
conf_matrix = confusion_matrix(y_test, predictions)
print("Confusion Matrix:")
print(conf_matrix)

# Classification report
class_report = classification_report(y_test, predictions)
print("Classification Report:")
print(class_report)

# Get feature importances from the trained model
feature_importances = clf.feature_importances_

# Create a DataFrame with feature names and their importances
feature_importance_df = pd.DataFrame({'Feature': features.columns, 'Importance': feature_importances})

# Sort the features based on their importance in descending order
top_10_features = feature_importance_df.sort_values(by='Importance', ascending=False).head(10)

# Print the top 10 features
print("Top 10 Features:")
print(top_10_features)