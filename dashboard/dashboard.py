# dashboard/dashboard.py

import streamlit as st
import pandas as pd
import time
import os
import sys

# Make project root accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.predict import predict_from_live_data

st.set_page_config(page_title="AI Options Trading Dashboard", layout="wide")
st.title("📈 AI Options Trading Dashboard")

st.markdown("Auto-loading `data/live_input.csv` every 30 seconds. No manual upload needed.")

DATA_PATH = "data/live_input.csv"

# Set up auto-refresh
refresh_interval = 30  # seconds
st_autorefresh = st.empty()

while True:
    st_autorefresh.empty()

    if not os.path.exists(DATA_PATH):
        st.warning("Waiting for live_input.csv to be created...")
        time.sleep(refresh_interval)
        continue

    # Load the live input
    df = pd.read_csv(DATA_PATH)

    # Generate predictions
    predictions = predict_from_live_data(df)

    # Display predictions
    st.subheader("🔮 Model Predictions")
    st.dataframe(pd.DataFrame(predictions))

    # Display raw features
    st.subheader("📊 Raw Live Input")
    st.dataframe(df)

    # Wait and refresh
    time.sleep(refresh_interval)
    st_autorefresh.empty()
