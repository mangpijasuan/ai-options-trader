# backtest/backtest_engine.py

import pandas as pd
from utils.feature_engineering import prepare_features
from sklearn.metrics import accuracy_score

def backtest(data_path='data/historical_data.csv', model_path='models/model.pkl'):
    data = pd.read_csv(data_path)
    data = data.dropna()
    X = prepare_features(data)
    y_true = data['direction']

    import joblib
    model = joblib.load(model_path)
    y_pred = model.predict(X)

    acc = accuracy_score(y_true, y_pred)
    print(f"📉 Backtest Accuracy: {acc:.2%}")
    # Add Sharpe, drawdown, etc. if needed
