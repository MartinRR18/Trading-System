"""Base strategy framework"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class BaseStrategy(ABC):
    """Abstract base class for trading strategies"""

    def __init__(self, name: str, symbol: str):
        """
        Initialize strategy.

        Args:
            name: Strategy name
            symbol: Trading pair
        """
        self.name = name
        self.symbol = symbol
        self.data = None

    def load_data(self, df: pd.DataFrame) -> None:
        """Load market data for analysis"""
        self.data = df

    @abstractmethod
    def calculate_signals(self) -> pd.DataFrame:
        """
        Calculate trading signals.

        Returns:
            DataFrame with 'signal' column (-1, 0, or 1)
        """
        pass

    @abstractmethod
    def generate_orders(self) -> List[Dict[str, Any]]:
        """Generate orders based on signals"""
        pass

    def validate_data(self) -> bool:
        """Validate data integrity"""
        if self.data is None or self.data.empty:
            logger.warning(f"No data loaded for {self.name}")
            return False
        return True


class SMAStrategy(BaseStrategy):
    """Simple Moving Average crossover strategy"""

    def __init__(self, name: str, symbol: str, short_window: int = 20, long_window: int = 50):
        """
        Initialize SMA strategy.

        Args:
            name: Strategy name
            symbol: Trading pair
            short_window: Short-term SMA period
            long_window: Long-term SMA period
        """
        super().__init__(name, symbol)
        self.short_window = short_window
        self.long_window = long_window
        self.signals = None

    def calculate_signals(self) -> pd.DataFrame:
        """Calculate SMA crossover signals"""
        if not self.validate_data():
            return None

        df = self.data.copy()
        df['SMA_short'] = df['close'].rolling(window=self.short_window).mean()
        df['SMA_long'] = df['close'].rolling(window=self.long_window).mean()

        df['signal'] = 0
        df.loc[df['SMA_short'] > df['SMA_long'], 'signal'] = 1  # Buy signal
        df.loc[df['SMA_short'] < df['SMA_long'], 'signal'] = -1  # Sell signal

        self.signals = df
        return df

    def generate_orders(self) -> List[Dict[str, Any]]:
        """Generate orders from SMA signals"""
        if self.signals is None:
            self.calculate_signals()

        orders = []
        for idx in range(1, len(self.signals)):
            prev_signal = self.signals.iloc[idx - 1]['signal']
            curr_signal = self.signals.iloc[idx]['signal']

            # Buy signal: transition from -1 or 0 to 1
            if prev_signal <= 0 and curr_signal == 1:
                orders.append({
                    'type': 'buy',
                    'timestamp': self.signals.iloc[idx]['timestamp'],
                    'price': self.signals.iloc[idx]['close'],
                    'symbol': self.symbol,
                })

            # Sell signal: transition from 1 to -1 or 0
            elif prev_signal == 1 and curr_signal <= 0:
                orders.append({
                    'type': 'sell',
                    'timestamp': self.signals.iloc[idx]['timestamp'],
                    'price': self.signals.iloc[idx]['close'],
                    'symbol': self.symbol,
                })

        return orders
