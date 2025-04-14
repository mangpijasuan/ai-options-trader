# brokers/option_trader.py

from ib_insync import *

def connect_ibkr():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    return ib

def place_option_trade(ib, symbol, right, strike, expiry, action='BUY', quantity=1):
    contract = Option(symbol=symbol, lastTradeDateOrContractMonth=expiry,
                      strike=strike, right=right, exchange='SMART')
    ib.qualifyContracts(contract)

    order = MarketOrder(action, quantity)
    trade = ib.placeOrder(contract, order)
    print(f"✅ Order placed: {action} {right} {symbol} @ {strike}")
    return trade
