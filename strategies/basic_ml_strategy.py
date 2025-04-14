# strategies/basic_ml_strategy.py

import pandas as pd
import joblib

MODEL_PATH = 'models/model.pkl'
FEATURES = ['delta', 'gamma', 'vega', 'theta', 'iv', 'underlying_return_1d', 'volume']

def load_model():
    return joblib.load(MODEL_PATH)

def generate_trade_signal(latest_data: pd.DataFrame):
    model = load_model()
    X = latest_data[FEATURES]
    pred = model.predict(X)

    # 1 = up → buy CALL; 0 = down → buy PUT
    signals = []
    for i, direction in enumerate(pred):
        row = latest_data.iloc[i]
        signals.append({
            "symbol": row['symbol'],
            "signal": "CALL" if direction == 1 else "PUT",
            "confidence": max(model.predict_proba(X)[i])  # max prob
        })
    return signals

# Example usage:
# test_data = pd.read_csv('data/live_input.csv')
# print(generate_trade_signal(test_data))
