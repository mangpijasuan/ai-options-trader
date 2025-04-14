# models/train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from utils.feature_engineering import prepare_features

# Load dataset
data = pd.read_csv('data/historical_data.csv')

# Compute ML features
X = prepare_features(data)
y = data['direction']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, 'models/model.pkl')
print("✅ Model saved to models/model.pkl")
