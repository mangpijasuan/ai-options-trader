# 🤖 AI Options Trader

An automated options trading system that uses machine learning to predict market direction and execute trades through Interactive Brokers (IBKR).

## 📋 Features

- **Machine Learning Prediction**: Uses Random Forest classifier to predict market direction (CALL/PUT)
- **Live Trading**: Automated trading with Interactive Brokers API
- **Greek-Based Filtering**: Filters trades based on option Greeks (delta, gamma, vega, theta)
- **Real-time Dashboard**: Streamlit dashboard for monitoring predictions and live data
- **Backtesting**: Backtest strategies on historical data
- **Risk Management**: Portfolio tracking and risk engine (in development)

## 🏗️ Project Structure

```
ai-options-trader/
├── backtest/           # Backtesting engine and metrics
├── brokers/            # IBKR connection and data fetching
├── dashboard/          # Streamlit dashboard
├── data/               # Historical and live market data
├── execution/          # Trading scheduler and execution logic
├── models/             # ML model training and prediction
├── portfolio/          # Portfolio tracking and risk management
├── strategies/         # Trading strategies and signal generation
├── utils/              # Helper functions and feature engineering
├── cpp_modules/        # C++ performance modules (planned)
├── main.py             # Main entry point
└── requirements.txt    # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Interactive Brokers TWS or IB Gateway (for live trading)
- IBKR account with API access enabled

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mangpijasuan/ai-options-trader.git
cd ai-options-trader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure IBKR connection:
   - Start TWS or IB Gateway
   - Enable API connections (port 7497 for paper trading, 7496 for live)
   - Set client ID to 1

### Training the Model

Before running the trader, train the ML model on historical data:

```bash
python models/train_model.py
```

This will:
- Load historical options data from `data/historical_data.csv`
- Train a Random Forest classifier
- Save the model to `models/model.pkl`
- Print classification metrics

### Running the Trader

Start the automated trading system:

```bash
python main.py
```

The system will:
- Connect to IBKR
- Fetch live market data every 5 minutes
- Generate predictions using the trained model
- Place trades when confidence threshold is met (≥80%)

### Running the Dashboard

Monitor live predictions and data:

```bash
streamlit run dashboard/dashboard.py
```

The dashboard displays:
- Real-time model predictions
- Confidence scores
- Raw market data and features

### Backtesting

Evaluate strategy performance on historical data:

```bash
python -c "from backtest.backtest_engine import backtest; backtest()"
```

## 🎯 Trading Strategy

### Signal Generation

1. **Data Collection**: Fetch live option Greeks and underlying prices
2. **Feature Engineering**: Calculate technical indicators and returns
3. **ML Prediction**: Random Forest predicts market direction
4. **Greek Filtering**: Apply Greek-based risk filters
5. **Execution**: Place trades via IBKR API

### Default Parameters

- **Confidence Threshold**: 0.8 (80%)
- **Trade Quantity**: 1 contract
- **Trading Interval**: 300 seconds (5 minutes)
- **Expiration**: Next Friday
- **Strike**: 180 (static, should be dynamic)

### Greek Filters

- **Delta**: 0.3 - 0.7 (moderate directional exposure)
- **Gamma**: < 0.2 (avoid explosive sensitivity)
- **Vega**: > 0.1 (some volatility exposure)
- **Theta**: > -0.05 (limit time decay)

## 📊 Data Format

Historical data should be in CSV format with these columns:

```
symbol, delta, gamma, vega, theta, iv, underlying_close, volume, direction
```

- `direction`: 1 = bullish (CALL), 0 = bearish (PUT)

## ⚙️ Configuration

Key parameters can be modified in:
- `execution/scheduler.py`: Trading intervals, thresholds
- `strategies/greeks_optimizer.py`: Greek filter ranges
- `brokers/option_trader.py`: IBKR connection settings

## 🔒 Security

- Never commit API credentials or sensitive data
- Use environment variables for configuration
- Test with paper trading account before live trading
- Monitor positions regularly

## ⚠️ Disclaimer

This software is for educational purposes only. Options trading carries significant risk. Use at your own risk. Past performance does not guarantee future results.

## 🛠️ Development Status

- ✅ Core ML prediction engine
- ✅ IBKR integration
- ✅ Basic backtesting
- ✅ Dashboard visualization
- 🚧 Portfolio tracking (in progress)
- 🚧 Risk management (in progress)
- 🚧 Advanced strategies (in progress)
- 🚧 C++ performance modules (planned)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
