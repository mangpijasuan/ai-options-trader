# models/predict.py

import pandas as pd
import joblib
from utils.feature_engineering import prepare_features

MODEL_PATH = 'models/model.pkl'

def load_model():
    return joblib.load(MODEL_PATH)

def predict_from_live_data(live_df):
    model = load_model()
    X = prepare_features(live_df)
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
