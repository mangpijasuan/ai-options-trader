# brokers/ibkr_broker.py

from ib_insync import IB, Option, Stock, MarketOrder
from typing import Dict, Any
from .base_broker import BaseBroker


class IBKRBroker(BaseBroker):
    """
    Interactive Brokers implementation of the broker interface.
    """
    
    def __init__(self, host: str = '127.0.0.1', port: int = 7497, client_id: int = 1):
        """
        Initialize IBKR broker connection parameters.
        
        Args:
            host: TWS/Gateway host address
            port: TWS/Gateway port (7497 for TWS paper, 7496 for TWS live, 4002 for Gateway paper, 4001 for Gateway live)
            client_id: Unique client identifier
        """
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()
    
    def connect(self) -> None:
        """
        Establish connection to IBKR TWS/Gateway.
        """
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            print(f"✅ Connected to IBKR at {self.host}:{self.port}")
        except Exception as e:
            print(f"❌ Failed to connect to IBKR: {e}")
            raise
    
    def disconnect(self) -> None:
        """
        Close connection to IBKR.
        """
        if self.ib.isConnected():
            self.ib.disconnect()
            print("✅ Disconnected from IBKR")
    
    def is_connected(self) -> bool:
        """
        Check if connection to IBKR is active.
        """
        return self.ib.isConnected()
    
    def place_option_trade(self, symbol: str, right: str, strike: float, 
                          expiry: str, action: str = 'BUY', quantity: int = 1) -> Any:
        """
        Place an option trade on IBKR.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            right: 'C' for Call or 'P' for Put
            strike: Strike price
            expiry: Expiration date in YYYYMMDD format
            action: 'BUY' or 'SELL'
            quantity: Number of contracts
            
        Returns:
            Trade object from ib_insync
        """
        contract = Option(
            symbol=symbol, 
            lastTradeDateOrContractMonth=expiry,
            strike=strike, 
            right=right, 
            exchange='SMART'
        )
        self.ib.qualifyContracts(contract)
        
        order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(contract, order)
        print(f"✅ Order placed: {action} {right} {symbol} @ {strike}")
        return trade
    
    def fetch_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch current market data for a symbol from IBKR.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with market data
        """
        stock = Stock(symbol, 'SMART', 'USD')
        self.ib.qualifyContracts(stock)
        
        ticker = self.ib.reqMktData(stock, "", False, False)
        self.ib.sleep(2)  # Give IBKR time to respond
        
        # Fallback in case ticker.last is None
        last_price = ticker.last if ticker.last is not None else (ticker.close if ticker.close else None)
        
        market_data = {
            'symbol': symbol,
            'last_price': last_price,
            'close': ticker.close,
            'bid': ticker.bid,
            'ask': ticker.ask,
            'volume': ticker.volume
        }
        
        # Cancel the market data request to avoid resource lock
        self.ib.cancelMktData(ticker)
        
        return market_data
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get IBKR account information.
        
        Returns:
            Dictionary with account details
        """
        account_values = self.ib.accountValues()
        positions = self.ib.positions()
        
        account_info = {
            'account_values': account_values,
            'positions': positions,
            'portfolio': self.ib.portfolio()
        }
        
        return account_info
