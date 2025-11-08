# dashboard/dashboard.py

import streamlit as st
import pandas as pd
import time
import os
import sys
from datetime import datetime

# Make project root accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.predict import predict_from_live_data
import config

st.set_page_config(page_title="AI Options Trading Dashboard", layout="wide")
st.title("📈 AI Options Trading Dashboard")

# Add auto-refresh capability
st.markdown(f"Auto-refreshing every {config.DASHBOARD_REFRESH_INTERVAL} seconds")

# Create a placeholder for the refresh button
refresh_placeholder = st.empty()

# Display last update time
last_update = st.empty()

def load_and_display_data():
    """Load data and display predictions"""
    if not os.path.exists(config.LIVE_INPUT_PATH):
        st.warning(f"⏳ Waiting for {config.LIVE_INPUT_PATH} to be created...")
        st.info("Start the trading system with: `python main.py`")
        return
    
    try:
        # Load the live input
        df = pd.read_csv(config.LIVE_INPUT_PATH)
        
        # Generate predictions
        predictions = predict_from_live_data(df)
        pred_df = pd.DataFrame(predictions)
        
        # Display predictions
        st.subheader("🔮 Model Predictions")
        
        # Add color coding for confidence
        def color_confidence(val):
            if val >= config.CONFIDENCE_THRESHOLD:
                return 'background-color: lightgreen'
            elif val >= 0.6:
                return 'background-color: lightyellow'
            else:
                return 'background-color: lightcoral'
        
        styled_df = pred_df.style.applymap(color_confidence, subset=['confidence'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Trading decisions
        high_conf = pred_df[pred_df['confidence'] >= config.CONFIDENCE_THRESHOLD]
        if len(high_conf) > 0:
            st.success(f"✅ {len(high_conf)} signals above threshold ({config.CONFIDENCE_THRESHOLD:.0%})")
            st.dataframe(high_conf, use_container_width=True)
        else:
            st.info(f"ℹ️ No signals above threshold ({config.CONFIDENCE_THRESHOLD:.0%})")
        
        # Display raw features
        st.subheader("📊 Raw Live Input Data")
        st.dataframe(df, use_container_width=True)
        
        # Summary statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Symbols Tracked", len(df))
        with col2:
            st.metric("Avg Confidence", f"{pred_df['confidence'].mean():.1%}")
        with col3:
            st.metric("High Conf Signals", len(high_conf))
        
        last_update.info(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        import traceback
        st.code(traceback.format_exc())

# Main display
load_and_display_data()

# Auto-refresh using Streamlit's native rerun
# Note: For production, consider using streamlit-autorefresh package
if st.button("🔄 Refresh Now"):
    st.rerun()

# Add instructions
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    ### Dashboard Features
    
    - **Auto-refresh**: Page refreshes automatically every 30 seconds
    - **Color Coding**: 
      - 🟢 Green: High confidence (≥80%)
      - 🟡 Yellow: Medium confidence (60-80%)
      - 🔴 Red: Low confidence (<60%)
    
    ### Getting Started
    
    1. Train the model: `python models/train_model.py`
    2. Start trading: `python main.py`
    3. Monitor here: `streamlit run dashboard/dashboard.py`
    
    ### Configuration
    
    Adjust settings in `config.py`
    """)

# JavaScript for auto-refresh (alternative method)
st.markdown(
    f"""
    <script>
        setTimeout(function(){{
            window.location.reload();
        }}, {config.DASHBOARD_REFRESH_INTERVAL * 1000});
    </script>
    """,
    unsafe_allow_html=True
)
