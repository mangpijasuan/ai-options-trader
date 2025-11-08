# models/predict.py

import pandas as pd
import joblib
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feature_engineering import prepare_features
import config

def load_model():
    """
    Load the trained model from disk
    
    Returns:
        RandomForestClassifier: Loaded model
    
    Raises:
        FileNotFoundError: If model file doesn't exist
    """
    if not os.path.exists(config.MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {config.MODEL_PATH}. "
            "Please train the model first using: python models/train_model.py"
        )
    return joblib.load(config.MODEL_PATH)

def predict_from_live_data(live_df):
    """
    Generate predictions for live market data
    
    Args:
        live_df: DataFrame with live market data
    
    Returns:
        list: List of prediction dictionaries with symbol, prediction, and confidence
    """
    model = load_model()
    X = prepare_features(live_df.copy())
    probs = model.predict_proba(X)
    predictions = model.predict(X)

    results = []
    for i, row in live_df.iterrows():
        results.append({
            'symbol': row['symbol'],
            'prediction': 'CALL' if predictions[i] == 1 else 'PUT',
            'confidence': max(probs[i])
        })

    return results
