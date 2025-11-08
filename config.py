# config.py
"""
Configuration file for AI Options Trader
Modify these parameters to customize trading behavior
"""

import os
from datetime import datetime

# ============== Trading Parameters ==============
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.8))
TRADE_QUANTITY = int(os.getenv('TRADE_QUANTITY', 1))
TRADING_INTERVAL_SEC = int(os.getenv('TRADING_INTERVAL_SEC', 300))  # 5 minutes

# ============== IBKR Connection ==============
IBKR_HOST = os.getenv('IBKR_HOST', '127.0.0.1')
IBKR_PORT = int(os.getenv('IBKR_PORT', 7497))  # 7497 for paper, 7496 for live
IBKR_CLIENT_ID = int(os.getenv('IBKR_CLIENT_ID', 1))

# ============== Option Parameters ==============
# Set to None for dynamic calculation, or specify a value
STATIC_STRIKE = None  # Will use ATM strike if None
DAYS_TO_EXPIRY = 7  # Default to weekly options

# ============== Greek Filters ==============
DELTA_MIN = 0.3
DELTA_MAX = 0.7
GAMMA_MAX = 0.2
VEGA_MIN = 0.1
THETA_MAX = -0.05

# ============== Symbols to Trade ==============
TRADING_SYMBOLS = ['AAPL', 'TSLA', 'MSFT', 'NVDA', 'SPY', 'QQQ']

# ============== Paths ==============
DATA_DIR = 'data'
MODEL_PATH = 'models/model.pkl'
HISTORICAL_DATA_PATH = 'data/historical_data.csv'
LIVE_INPUT_PATH = 'data/live_input.csv'
LOG_DIR = 'logs'

# ============== Model Parameters ==============
RANDOM_FOREST_ESTIMATORS = 200
RANDOM_FOREST_RANDOM_STATE = 42
TEST_SIZE = 0.2

# ============== Feature Columns ==============
FEATURE_COLUMNS = ['delta', 'gamma', 'vega', 'theta', 'iv', 'underlying_return_1d', 'volume']

# ============== Risk Management ==============
MAX_POSITION_SIZE = 10  # Maximum contracts per position
MAX_DAILY_LOSS = 1000  # Maximum daily loss in dollars
MAX_PORTFOLIO_DELTA = 100  # Maximum net portfolio delta

# ============== Logging ==============
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# ============== Dashboard ==============
DASHBOARD_REFRESH_INTERVAL = 30  # seconds
DASHBOARD_PORT = 8501
