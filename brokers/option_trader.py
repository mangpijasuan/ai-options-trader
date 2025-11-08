# brokers/option_trader.py

from ib_insync import *
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def connect_ibkr():
    """
    Connect to Interactive Brokers TWS or IB Gateway
    
    Returns:
        IB: Connected IB instance
    
    Raises:
        Exception: If connection fails
    """
    ib = IB()
    try:
        ib.connect(config.IBKR_HOST, config.IBKR_PORT, clientId=config.IBKR_CLIENT_ID)
        print(f"✅ Connected to IBKR at {config.IBKR_HOST}:{config.IBKR_PORT}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise
    return ib

def place_option_trade(ib, symbol, right, strike, expiry, action='BUY', quantity=1):
    """
    Place an option trade through IBKR
    
    Args:
        ib: IB instance
        symbol: Underlying symbol (e.g., 'AAPL')
        right: 'C' for Call, 'P' for Put
        strike: Strike price
        expiry: Expiration date (YYYYMMDD format)
        action: 'BUY' or 'SELL'
        quantity: Number of contracts
    
    Returns:
        Trade: The placed trade object
    
    Raises:
        Exception: If order placement fails
    """
    try:
        contract = Option(
            symbol=symbol, 
            lastTradeDateOrContractMonth=expiry,
            strike=strike, 
            right=right, 
            exchange='SMART'
        )
        ib.qualifyContracts(contract)

        order = MarketOrder(action, quantity)
        trade = ib.placeOrder(contract, order)
        print(f"✅ Order placed: {action} {quantity} {right} {symbol} @ ${strike} exp {expiry}")
        return trade
    except Exception as e:
        print(f"❌ Failed to place order: {e}")
        raise
