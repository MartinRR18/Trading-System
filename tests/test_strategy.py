"""Tests for strategy module"""

import pytest
import pandas as pd
import numpy as np
from src.strategy import SMAStrategy


class TestSMAStrategy:
    """Test cases for SMA strategy"""

    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data"""
        dates = pd.date_range('2024-01-01', periods=100, freq='1h')
        close_prices = 100 + np.cumsum(np.random.randn(100))
        
        df = pd.DataFrame({
            'timestamp': dates,
            'open': close_prices - 0.5,
            'high': close_prices + 1,
            'low': close_prices - 1,
            'close': close_prices,
            'volume': np.random.randint(1000, 10000, 100)
        })
        return df

    def test_sma_strategy_initialization(self):
        """Test SMA strategy initialization"""
        strategy = SMAStrategy('test', 'BTC/USDT', short_window=20, long_window=50)
        assert strategy.name == 'test'
        assert strategy.symbol == 'BTC/USDT'
        assert strategy.short_window == 20
        assert strategy.long_window == 50

    def test_calculate_signals(self, sample_data):
        """Test signal calculation"""
        strategy = SMAStrategy('test', 'BTC/USDT')
        strategy.load_data(sample_data)
        
        signals = strategy.calculate_signals()
        assert signals is not None
        assert 'signal' in signals.columns
        assert 'SMA_short' in signals.columns
        assert 'SMA_long' in signals.columns

    def test_generate_orders(self, sample_data):
        """Test order generation"""
        strategy = SMAStrategy('test', 'BTC/USDT')
        strategy.load_data(sample_data)
        
        orders = strategy.generate_orders()
        assert isinstance(orders, list)
        
        for order in orders:
            assert 'type' in order
            assert 'symbol' in order
            assert order['symbol'] == 'BTC/USDT'
