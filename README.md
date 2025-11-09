# AI Options Trader

An AI-powered options trading system that uses machine learning to predict option trade opportunities and execute them automatically.

## Features

- 🤖 **AI-Powered Predictions**: Uses machine learning models to analyze market data and predict profitable trades
- 📊 **Real-time Market Data**: Fetches live market data from connected brokers
- 🔄 **Automated Trading**: Executes trades automatically based on ML predictions
- 📈 **Multiple Brokers**: Support for Interactive Brokers (IBKR) and Alpaca Markets
- 🎯 **Greeks Optimization**: Analyzes option Greeks (Delta, Gamma, Vega, Theta) for better trade selection
- 📉 **Backtesting**: Test strategies on historical data before going live
- 📊 **Dashboard**: Streamlit-based dashboard for monitoring and analysis

## Multi-Broker Support

This system now supports multiple brokers:

- **Interactive Brokers (IBKR)** - Full options trading support
- **Alpaca Markets** - Commission-free trading with limited options support

### Quick Start - Broker Selection

```bash
# Use IBKR (default)
python main.py ibkr

# Use Alpaca
python main.py alpaca
```

For detailed broker setup instructions, see [BROKER_SETUP.md](BROKER_SETUP.md).

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mangpijasuan/ai-options-trader.git
cd ai-options-trader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your broker credentials:
```bash
cp .env.example .env
# Edit .env with your broker credentials
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Choose your broker
BROKER_TYPE=ibkr  # or 'alpaca'

# IBKR Settings
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
IBKR_CLIENT_ID=1

# Alpaca Settings
ALPACA_API_KEY=your_key_here
ALPACA_SECRET_KEY=your_secret_here
ALPACA_PAPER=true
```

## Usage

### Running the Automated Trader

```bash
# Start with default broker (from .env)
python main.py

# Specify broker explicitly
python main.py ibkr
python main.py alpaca
```

### Using the Broker API Programmatically

```python
from brokers import BrokerFactory

# Create a broker instance
broker = BrokerFactory.create_broker('ibkr')
broker.connect()

# Place an option trade
broker.place_option_trade(
    symbol='AAPL',
    right='C',  # 'C' for Call, 'P' for Put
    strike=150.0,
    expiry='20231215',
    action='BUY',
    quantity=1
)

# Fetch market data
data = broker.fetch_market_data('AAPL')
print(data)

broker.disconnect()
```

### Running the Dashboard

```bash
streamlit run dashboard/dashboard.py
```

## Project Structure

```
ai-options-trader/
├── brokers/              # Broker integrations
│   ├── base_broker.py    # Abstract broker interface
│   ├── ibkr_broker.py    # IBKR implementation
│   ├── alpaca_broker.py  # Alpaca implementation
│   ├── broker_factory.py # Factory for creating brokers
│   └── data_fetcher.py   # Broker-agnostic data fetcher
├── models/               # ML models
│   ├── train_model.py    # Model training
│   └── predict.py        # Prediction logic
├── strategies/           # Trading strategies
│   ├── basic_ml_strategy.py
│   └── greeks_optimizer.py
├── execution/            # Trade execution
│   └── scheduler.py      # Automated trading scheduler
├── backtest/             # Backtesting engine
├── portfolio/            # Portfolio tracking
├── dashboard/            # Streamlit dashboard
├── utils/                # Utility functions
├── data/                 # Data storage
├── examples/             # Example scripts
└── main.py              # Main entry point
```

## Architecture

### Broker Abstraction Layer

The system uses a broker abstraction layer that allows seamless switching between different brokers:

```
BaseBroker (Abstract)
    ├── IBKRBroker (Interactive Brokers)
    └── AlpacaBroker (Alpaca Markets)
```

All brokers implement the same interface:
- `connect()` / `disconnect()`
- `place_option_trade()`
- `fetch_market_data()`
- `get_account_info()`

## Development

### Running Examples

```bash
# Broker abstraction demo
python examples/broker_example.py
```

### Adding a New Broker

1. Create a new broker class inheriting from `BaseBroker`
2. Implement all abstract methods
3. Add broker creation logic to `BrokerFactory`
4. Update documentation

## Safety & Risk Management

⚠️ **Important Safety Notes:**

- Always start with **paper trading** accounts
- Test thoroughly before using real money
- Set appropriate confidence thresholds
- Monitor your trades regularly
- Understand the risks of automated trading
- Keep your API credentials secure

## Requirements

- Python 3.8+
- Interactive Brokers TWS/Gateway (for IBKR) or Alpaca account
- See `requirements.txt` for Python packages

## Documentation

- [Broker Setup Guide](BROKER_SETUP.md) - Detailed broker configuration instructions
- [Examples](examples/) - Code examples for using the broker API

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Disclaimer

This software is for educational purposes only. Use at your own risk. The authors are not responsible for any financial losses incurred through the use of this software. Always understand the risks involved in options trading and automated trading systems.
