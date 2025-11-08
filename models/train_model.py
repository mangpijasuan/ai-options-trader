# models/train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feature_engineering import prepare_features
import config

def train_model():
    """
    Train the Random Forest model on historical data
    
    Returns:
        RandomForestClassifier: Trained model
    """
    print("📊 Loading historical data...")
    try:
        data = pd.read_csv(config.HISTORICAL_DATA_PATH)
        print(f"✅ Loaded {len(data)} samples from {config.HISTORICAL_DATA_PATH}")
    except FileNotFoundError:
        print(f"❌ Error: {config.HISTORICAL_DATA_PATH} not found")
        print("Please ensure historical data exists before training.")
        return None
    
    # Compute ML features
    print("🔧 Preparing features...")
    X = prepare_features(data.copy())
    y = data['direction']
    
    print(f"Features: {list(X.columns)}")
    print(f"Target distribution: {y.value_counts().to_dict()}")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=config.TEST_SIZE, 
        random_state=config.RANDOM_FOREST_RANDOM_STATE
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")

    # Train model
    print("\n🤖 Training Random Forest model...")
    clf = RandomForestClassifier(
        n_estimators=config.RANDOM_FOREST_ESTIMATORS, 
        random_state=config.RANDOM_FOREST_RANDOM_STATE,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    # Evaluate
    print("\n📈 Evaluating model...")
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nAccuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['PUT', 'CALL']))

    # Feature importance
    print("\n📊 Feature Importance:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.to_string(index=False))

    # Save model
    print(f"\n💾 Saving model to {config.MODEL_PATH}...")
    os.makedirs(os.path.dirname(config.MODEL_PATH), exist_ok=True)
    joblib.dump(clf, config.MODEL_PATH)
    print(f"✅ Model saved successfully")
    
    return clf

if __name__ == "__main__":
    train_model()
