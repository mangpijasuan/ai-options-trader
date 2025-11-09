# Broker Setup Guide

This AI Options Trader now supports multiple brokers. You can choose between Interactive Brokers (IBKR) and Alpaca Markets.

## Supported Brokers

### 1. Interactive Brokers (IBKR)

Interactive Brokers provides full options trading support through their TWS (Trader Workstation) or IB Gateway.

**Setup Steps:**

1. Install TWS or IB Gateway
2. Configure your connection settings in `.env` file:
   ```bash
   BROKER_TYPE=ibkr
   IBKR_HOST=127.0.0.1
   IBKR_PORT=7497  # Paper trading port
   IBKR_CLIENT_ID=1
   ```

**Port Configuration:**
- `7497` - TWS Paper Trading
- `7496` - TWS Live Trading
- `4002` - IB Gateway Paper Trading
- `4001` - IB Gateway Live Trading

**Features:**
- Full options trading support
- Real-time market data
- Greeks calculation
- Multiple order types

### 2. Alpaca Markets

Alpaca provides commission-free stock and limited options trading through their REST API.

**Setup Steps:**

1. Sign up at [Alpaca Markets](https://alpaca.markets/)
2. Get your API keys from the dashboard
3. Configure your connection settings in `.env` file:
   ```bash
   BROKER_TYPE=alpaca
   ALPACA_API_KEY=your_api_key_here
   ALPACA_SECRET_KEY=your_secret_key_here
   ALPACA_PAPER=true
   ```

**Features:**
- Commission-free trading
- REST API access
- Paper trading support
- Primary focus on stocks

**Note:** Alpaca's options trading support is limited compared to IBKR. Check their documentation for current capabilities.

## Usage

### Using Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your broker credentials

3. Run the application:
   ```bash
   python main.py
   ```

### Using Command Line Arguments

Override the broker type with a command line argument:

```bash
# Use IBKR
python main.py ibkr

# Use Alpaca
python main.py alpaca
```

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

### Broker-Specific Dependencies

- **IBKR**: Requires `ib_insync` package (included in requirements.txt)
- **Alpaca**: Requires `alpaca-py` package (included in requirements.txt)

## Programmatic Usage

You can also use the broker abstraction in your own code:

```python
from brokers import BrokerFactory

# Create a broker instance
broker = BrokerFactory.create_broker('ibkr')
# or
broker = BrokerFactory.create_broker('alpaca', 
                                     api_key='your_key',
                                     secret_key='your_secret')

# Connect to the broker
broker.connect()

# Place a trade
broker.place_option_trade(
    symbol='AAPL',
    right='C',  # 'C' for Call, 'P' for Put
    strike=150.0,
    expiry='20231215',
    action='BUY',
    quantity=1
)

# Get market data
data = broker.fetch_market_data('AAPL')

# Disconnect when done
broker.disconnect()
```

## Security Best Practices

1. **Never commit your `.env` file** - It contains sensitive credentials
2. Use paper trading accounts for testing
3. Start with small position sizes
4. Review all trades before going live
5. Keep your API keys secure and rotate them regularly

## Troubleshooting

### IBKR Connection Issues

- Ensure TWS/Gateway is running
- Check that the correct port is configured
- Verify API connections are enabled in TWS settings
- Make sure client ID is unique

### Alpaca Connection Issues

- Verify API keys are correct
- Check that you're using the right environment (paper vs live)
- Ensure you have sufficient buying power
- Review Alpaca's rate limits

## Support

For broker-specific issues:
- IBKR: [Interactive Brokers Support](https://www.interactivebrokers.com/en/support/support.php)
- Alpaca: [Alpaca Documentation](https://alpaca.markets/docs/)
