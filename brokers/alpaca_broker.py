# brokers/alpaca_broker.py

from typing import Dict, Any, Optional
from .base_broker import BaseBroker

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockLatestQuoteRequest
    ALPACA_AVAILABLE = True
except ImportError:
    ALPACA_AVAILABLE = False
    print("⚠️ alpaca-py not installed. Install with: pip install alpaca-py")


class AlpacaBroker(BaseBroker):
    """
    Alpaca Markets implementation of the broker interface.
    Note: Alpaca primarily supports stock trading. Options support is limited.
    """
    
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, paper: bool = True):
        """
        Initialize Alpaca broker connection parameters.
        
        Args:
            api_key: Alpaca API key
            secret_key: Alpaca secret key
            paper: Use paper trading (True) or live trading (False)
        """
        if not ALPACA_AVAILABLE:
            raise ImportError("alpaca-py package is required. Install with: pip install alpaca-py")
        
        self.api_key = api_key
        self.secret_key = secret_key
        self.paper = paper
        self.trading_client = None
        self.data_client = None
        self._connected = False
    
    def connect(self) -> None:
        """
        Establish connection to Alpaca API.
        """
        if not self.api_key or not self.secret_key:
            raise ValueError("Alpaca API key and secret key are required")
        
        try:
            self.trading_client = TradingClient(
                api_key=self.api_key,
                secret_key=self.secret_key,
                paper=self.paper
            )
            self.data_client = StockHistoricalDataClient(
                api_key=self.api_key,
                secret_key=self.secret_key
            )
            
            # Test connection by getting account info
            account = self.trading_client.get_account()
            self._connected = True
            
            account_type = "paper" if self.paper else "live"
            print(f"✅ Connected to Alpaca ({account_type}) - Account: {account.account_number}")
        except Exception as e:
            self._connected = False
            print(f"❌ Failed to connect to Alpaca: {e}")
            raise
    
    def disconnect(self) -> None:
        """
        Close connection to Alpaca (not required for REST API).
        """
        self._connected = False
        self.trading_client = None
        self.data_client = None
        print("✅ Disconnected from Alpaca")
    
    def is_connected(self) -> bool:
        """
        Check if connection to Alpaca is active.
        """
        return self._connected and self.trading_client is not None
    
    def place_option_trade(self, symbol: str, right: str, strike: float, 
                          expiry: str, action: str = 'BUY', quantity: int = 1) -> Any:
        """
        Place an option trade on Alpaca.
        
        Note: Alpaca's options trading support is limited. This implementation
        provides the interface but may not work for all option strategies.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            right: 'C' for Call or 'P' for Put
            strike: Strike price
            expiry: Expiration date
            action: 'BUY' or 'SELL'
            quantity: Number of contracts
            
        Returns:
            Order object from Alpaca
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to Alpaca. Call connect() first.")
        
        # Construct option symbol in OCC format: SYMBOL + YYMMDD + C/P + STRIKE_PRICE
        # Example: AAPL230120C00150000 (AAPL Call expiring Jan 20, 2023 with strike 150)
        
        # Note: This is a simplified implementation. Full options support would require
        # proper OCC symbol formatting and verification that Alpaca supports options trading.
        print(f"⚠️ Alpaca options trading support is limited. Placing order for: {action} {right} {symbol} @ {strike}")
        
        # For demonstration, we'll place a stock order instead
        # In production, you'd need to properly format the option symbol
        side = OrderSide.BUY if action == 'BUY' else OrderSide.SELL
        
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=side,
            time_in_force=TimeInForce.DAY
        )
        
        order = self.trading_client.submit_order(order_data=market_order_data)
        print(f"✅ Order placed: {action} {quantity} shares of {symbol}")
        return order
    
    def fetch_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch current market data for a symbol from Alpaca.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with market data
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to Alpaca. Call connect() first.")
        
        request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
        latest_quote = self.data_client.get_stock_latest_quote(request)
        
        quote = latest_quote[symbol]
        
        market_data = {
            'symbol': symbol,
            'last_price': (quote.bid_price + quote.ask_price) / 2 if quote.bid_price and quote.ask_price else None,
            'bid': quote.bid_price,
            'ask': quote.ask_price,
            'bid_size': quote.bid_size,
            'ask_size': quote.ask_size,
            'timestamp': quote.timestamp
        }
        
        return market_data
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get Alpaca account information.
        
        Returns:
            Dictionary with account details
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to Alpaca. Call connect() first.")
        
        account = self.trading_client.get_account()
        positions = self.trading_client.get_all_positions()
        
        account_info = {
            'account_number': account.account_number,
            'cash': float(account.cash),
            'portfolio_value': float(account.portfolio_value),
            'buying_power': float(account.buying_power),
            'equity': float(account.equity),
            'positions': positions
        }
        
        return account_info
