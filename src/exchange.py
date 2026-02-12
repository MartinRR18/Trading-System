"""Exchange connector using CCXT"""

import ccxt
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ExchangeConnector:
    """Wrapper for CCXT exchange connections"""

    def __init__(self, exchange_name: str, api_key: str = None, api_secret: str = None):
        """
        Initialize exchange connector.

        Args:
            exchange_name: Name of the exchange (e.g., 'binance', 'kraken')
            api_key: API key for authentication
            api_secret: API secret for authentication
        """
        self.exchange_name = exchange_name
        self.api_key = api_key
        self.api_secret = api_secret
        self.exchange = self._initialize_exchange()

    def _initialize_exchange(self):
        """Initialize CCXT exchange instance"""
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            exchange_config = {
                'enableRateLimit': True,
            }
            if self.api_key and self.api_secret:
                exchange_config['apiKey'] = self.api_key
                exchange_config['secret'] = self.api_secret

            exchange = exchange_class(exchange_config)
            logger.info(f"Connected to {self.exchange_name}")
            return exchange
        except Exception as e:
            logger.error(f"Failed to initialize {self.exchange_name}: {e}")
            raise

    def get_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> List[List[Any]]:
        """
        Fetch OHLCV (candlestick) data.

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Candlestick interval (e.g., '1h', '4h', '1d')
            limit: Number of candles to fetch

        Returns:
            List of OHLCV candles
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        except Exception as e:
            logger.error(f"Failed to fetch OHLCV for {symbol}: {e}")
            raise

    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get current ticker information"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            logger.error(f"Failed to fetch ticker for {symbol}: {e}")
            raise

    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            logger.error(f"Failed to fetch balance: {e}")
            raise
