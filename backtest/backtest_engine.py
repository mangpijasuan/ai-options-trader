# backtest/backtest_engine.py

import pandas as pd
import joblib
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feature_engineering import prepare_features
from sklearn.metrics import accuracy_score, classification_report
from backtest.metrics import compute_metrics
import config

def backtest(data_path=None, model_path=None):
    """
    Backtest the trading model on historical data
    
    Args:
        data_path: Path to historical data (defaults to config value)
        model_path: Path to trained model (defaults to config value)
    
    Returns:
        dict: Backtest results including accuracy and metrics
    """
    if data_path is None:
        data_path = config.HISTORICAL_DATA_PATH
    if model_path is None:
        model_path = config.MODEL_PATH
    
    print(f"📊 Running backtest on {data_path}...")
    
    try:
        data = pd.read_csv(data_path)
        data = data.dropna()
        print(f"✅ Loaded {len(data)} samples")
    except FileNotFoundError:
        print(f"❌ Error: {data_path} not found")
        return None
    
    # Prepare features
    X = prepare_features(data.copy())
    y_true = data['direction']
    
    # Load model
    try:
        model = joblib.load(model_path)
        print(f"✅ Loaded model from {model_path}")
    except FileNotFoundError:
        print(f"❌ Error: Model not found at {model_path}")
        print("Please train the model first: python models/train_model.py")
        return None
    
    # Make predictions
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)
    
    # Calculate accuracy
    acc = accuracy_score(y_true, y_pred)
    print(f"\n📈 Backtest Accuracy: {acc:.2%}")
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=['PUT', 'CALL']))
    
    # Simulate returns (simplified - assumes 10% return on correct predictions, -5% on wrong)
    returns = []
    for true_val, pred_val, proba in zip(y_true, y_pred, y_proba):
        confidence = max(proba)
        # Only trade if confidence is above threshold
        if confidence >= config.CONFIDENCE_THRESHOLD:
            if true_val == pred_val:
                returns.append(0.10)  # 10% gain on correct prediction
            else:
                returns.append(-0.05)  # 5% loss on wrong prediction
        else:
            returns.append(0.0)  # No trade
    
    # Calculate metrics
    if len(returns) > 0:
        print(f"\n📊 Trading Metrics (confidence ≥ {config.CONFIDENCE_THRESHOLD:.0%}):")
        print(f"Trades executed: {sum(1 for r in returns if r != 0)}")
        print(f"Trades skipped: {sum(1 for r in returns if r == 0)}")
        
        active_returns = [r for r in returns if r != 0]
        if len(active_returns) > 0:
            metrics = compute_metrics(active_returns)
            for key, value in metrics.items():
                print(f"{key}: {value}")
    
    return {
        'accuracy': acc,
        'returns': returns,
        'predictions': y_pred,
        'true_values': y_true
    }

if __name__ == "__main__":
    backtest()
