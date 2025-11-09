# Migration Guide: Multi-Broker Support

This guide helps existing users migrate to the new multi-broker architecture.

## What Changed?

The AI Options Trader now supports multiple brokers through a unified abstraction layer. You can now choose between:
- Interactive Brokers (IBKR) - default
- Alpaca Markets

## Breaking Changes

### Old Code (IBKR-only)

```python
from brokers.option_trader import connect_ibkr, place_option_trade
from brokers.ibkr_data_fetcher import fetch_live_option_data

ib = connect_ibkr()
place_option_trade(ib, 'AAPL', 'C', 150, '20231215', 'BUY', 1)
fetch_live_option_data(['AAPL', 'TSLA'])
```

### New Code (Multi-broker)

```python
from brokers import BrokerFactory
from brokers.data_fetcher import fetch_live_option_data

broker = BrokerFactory.create_broker('ibkr')  # or 'alpaca'
broker.connect()
broker.place_option_trade('AAPL', 'C', 150, '20231215', 'BUY', 1)
fetch_live_option_data(broker, ['AAPL', 'TSLA'])
```

## Migration Steps

### 1. Update Your Imports

**Before:**
```python
from brokers.option_trader import connect_ibkr, place_option_trade
from brokers.ibkr_data_fetcher import fetch_live_option_data
```

**After:**
```python
from brokers import BrokerFactory
from brokers.data_fetcher import fetch_live_option_data
```

### 2. Update Broker Connection

**Before:**
```python
ib = connect_ibkr()
```

**After:**
```python
broker = BrokerFactory.create_broker('ibkr')
broker.connect()
```

### 3. Update Trade Execution

**Before:**
```python
place_option_trade(ib, symbol='AAPL', right='C', strike=150, 
                   expiry='20231215', action='BUY', quantity=1)
```

**After:**
```python
broker.place_option_trade(symbol='AAPL', right='C', strike=150,
                          expiry='20231215', action='BUY', quantity=1)
```

### 4. Update Data Fetching

**Before:**
```python
fetch_live_option_data(['AAPL', 'TSLA'])  # Implicitly used IBKR
```

**After:**
```python
fetch_live_option_data(broker, ['AAPL', 'TSLA'])  # Pass broker instance
```

### 5. Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` to set your broker preference:

```bash
# For IBKR (default)
BROKER_TYPE=ibkr
IBKR_HOST=127.0.0.1
IBKR_PORT=7497
IBKR_CLIENT_ID=1

# For Alpaca
# BROKER_TYPE=alpaca
# ALPACA_API_KEY=your_key
# ALPACA_SECRET_KEY=your_secret
# ALPACA_PAPER=true
```

## Backwards Compatibility

The old broker files are still present but deprecated:
- `brokers/ibkr_connection.py` (deprecated)
- `brokers/ibkr_data_fetcher.py` (deprecated)
- `brokers/option_trader.py` (deprecated)

**These files are no longer used by the main application.** If you have custom scripts using these files, please migrate them to use the new broker abstraction.

## Benefits of Migration

1. **Flexibility**: Switch between brokers without code changes
2. **Consistency**: Same API for all brokers
3. **Extensibility**: Easy to add new brokers in the future
4. **Better Testing**: Isolated broker logic with clear interfaces
5. **Configuration**: Manage broker settings via environment variables

## Need Help?

- See [BROKER_SETUP.md](BROKER_SETUP.md) for detailed broker configuration
- See [README.md](README.md) for usage examples
- Check [examples/](examples/) for code samples

## Quick Test

Run this to verify your migration:

```python
from brokers import BrokerFactory

# Test broker creation
broker = BrokerFactory.create_broker('ibkr')
print(f"✅ Successfully created {type(broker).__name__}")
```

If this works, your migration is complete!
