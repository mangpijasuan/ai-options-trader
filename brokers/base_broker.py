# brokers/base_broker.py

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class BaseBroker(ABC):
    """
    Abstract base class for broker implementations.
    All broker connectors must implement these methods.
    """
    
    @abstractmethod
    def connect(self) -> None:
        """
        Establish connection to the broker.
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """
        Close connection to the broker.
        """
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if connection to broker is active.
        """
        pass
    
    @abstractmethod
    def place_option_trade(self, symbol: str, right: str, strike: float, 
                          expiry: str, action: str = 'BUY', quantity: int = 1) -> Any:
        """
        Place an option trade.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            right: 'C' for Call or 'P' for Put
            strike: Strike price
            expiry: Expiration date
            action: 'BUY' or 'SELL'
            quantity: Number of contracts
            
        Returns:
            Trade object/confirmation
        """
        pass
    
    @abstractmethod
    def fetch_market_data(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch current market data for a symbol.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with market data (last_price, volume, etc.)
        """
        pass
    
    @abstractmethod
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.
        
        Returns:
            Dictionary with account details (balance, positions, etc.)
        """
        pass
