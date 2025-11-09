# brokers/broker_factory.py

import os
from typing import Optional
from .base_broker import BaseBroker
from .ibkr_broker import IBKRBroker
from .alpaca_broker import AlpacaBroker


class BrokerFactory:
    """
    Factory class to create broker instances based on configuration.
    """
    
    @staticmethod
    def create_broker(broker_type: str = 'ibkr', **kwargs) -> BaseBroker:
        """
        Create and return a broker instance.
        
        Args:
            broker_type: Type of broker ('ibkr' or 'alpaca')
            **kwargs: Additional parameters for broker initialization
            
        Returns:
            BaseBroker instance
            
        Raises:
            ValueError: If broker_type is not supported
        """
        broker_type = broker_type.lower()
        
        if broker_type == 'ibkr':
            return BrokerFactory._create_ibkr_broker(**kwargs)
        elif broker_type == 'alpaca':
            return BrokerFactory._create_alpaca_broker(**kwargs)
        else:
            raise ValueError(f"Unsupported broker type: {broker_type}. Supported: 'ibkr', 'alpaca'")
    
    @staticmethod
    def _create_ibkr_broker(**kwargs) -> IBKRBroker:
        """
        Create IBKR broker instance with defaults from environment variables.
        """
        host = kwargs.get('host', os.getenv('IBKR_HOST', '127.0.0.1'))
        port = kwargs.get('port', int(os.getenv('IBKR_PORT', '7497')))
        client_id = kwargs.get('client_id', int(os.getenv('IBKR_CLIENT_ID', '1')))
        
        return IBKRBroker(host=host, port=port, client_id=client_id)
    
    @staticmethod
    def _create_alpaca_broker(**kwargs) -> AlpacaBroker:
        """
        Create Alpaca broker instance with defaults from environment variables.
        """
        api_key = kwargs.get('api_key', os.getenv('ALPACA_API_KEY'))
        secret_key = kwargs.get('secret_key', os.getenv('ALPACA_SECRET_KEY'))
        paper = kwargs.get('paper', os.getenv('ALPACA_PAPER', 'true').lower() == 'true')
        
        if not api_key or not secret_key:
            raise ValueError(
                "Alpaca API credentials required. Set ALPACA_API_KEY and ALPACA_SECRET_KEY "
                "environment variables or pass api_key and secret_key parameters."
            )
        
        return AlpacaBroker(api_key=api_key, secret_key=secret_key, paper=paper)
    
    @staticmethod
    def get_default_broker() -> BaseBroker:
        """
        Get default broker instance based on BROKER_TYPE environment variable.
        Defaults to IBKR if not specified.
        
        Returns:
            BaseBroker instance
        """
        broker_type = os.getenv('BROKER_TYPE', 'ibkr').lower()
        return BrokerFactory.create_broker(broker_type)
