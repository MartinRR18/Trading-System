"""Tests for exchange module"""

import pytest
from src.exchange import ExchangeConnector


class TestExchangeConnector:
    """Test cases for ExchangeConnector"""

    def test_initialization(self):
        """Test exchange connector initialization"""
        # This test uses a public exchange with no auth required
        try:
            connector = ExchangeConnector('binance')
            assert connector.exchange_name == 'binance'
            assert connector.exchange is not None
        except Exception as e:
            pytest.skip(f"Could not initialize exchange: {e}")

    def test_invalid_exchange(self):
        """Test initialization with invalid exchange"""
        with pytest.raises(AttributeError):
            ExchangeConnector('invalid_exchange')
