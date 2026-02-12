# Trading System

A Python-based cryptocurrency trading system using CCXT, pandas, and numpy for algorithmic trading on multiple exchanges.

## Overview

This project provides a framework for developing, backtesting, and deploying cryptocurrency trading strategies. It includes:

- **Exchange Integration**: Connect to multiple cryptocurrency exchanges using CCXT
- **Strategy Framework**: Flexible base classes for implementing custom trading strategies
- **Data Analysis**: Built-in support for OHLCV data processing with pandas and numpy
- **Unit Tests**: Comprehensive test suite for strategy validation

## Project Structure

```
Trading_System/
├── src/
│   ├── __init__.py
│   ├── exchange.py          # CCXT exchange wrapper
│   └── strategy.py          # Base strategy classes
├── tests/
│   ├── __init__.py
│   ├── test_exchange.py     # Exchange connector tests
│   └── test_strategy.py     # Strategy tests
├── data/
│   ├── raw/                 # Raw market data
│   └── processed/           # Processed data
├── config/
│   └── .env                 # Environment variables (git ignored)
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Installation

1. **Clone or create the project**:
   ```bash
   cd Trading_System
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Getting Started

### Basic Usage

```python
from src.exchange import ExchangeConnector
from src.strategy import SMAStrategy
import pandas as pd

# Connect to an exchange (public data only)
exchange = ExchangeConnector('binance')

# Fetch OHLCV data
ohlcv = exchange.get_ohlcv('BTC/USDT', '1h', limit=100)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Create and run a strategy
strategy = SMAStrategy('my_strategy', 'BTC/USDT', short_window=20, long_window=50)
strategy.load_data(df)
signals = strategy.calculate_signals()
orders = strategy.generate_orders()

print(orders)
```

### Using API Keys

For trading functionality, set environment variables:

```bash
# In config/.env
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

Then load them in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv('config/.env')

exchange = ExchangeConnector(
    'binance',
    api_key=os.getenv('BINANCE_API_KEY'),
    api_secret=os.getenv('BINANCE_API_SECRET')
)
```

## Strategy Development

Create a custom strategy by extending `BaseStrategy`:

```python
from src.strategy import BaseStrategy
import pandas as pd

class MyStrategy(BaseStrategy):
    def calculate_signals(self) -> pd.DataFrame:
        # Implement your signal logic
        df = self.data.copy()
        df['signal'] = 0  # -1 = sell, 0 = hold, 1 = buy
        return df
    
    def generate_orders(self):
        # Implement your order generation logic
        return []
```

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage report
pytest --cov=src tests/
```

## Supported Exchanges

CCXT supports 140+ exchanges including:
- Binance
- Kraken
- Coinbase
- Bybit
- Kucoin
- And many more...

See [CCXT documentation](https://docs.ccxt.com/) for the complete list.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| ccxt | 4.0.100 | Cryptocurrency exchange API |
| pandas | 2.1.3 | Data analysis and manipulation |
| numpy | 1.26.2 | Numerical computing |
| python-dotenv | 1.0.0 | Environment variable management |
| requests | 2.31.0 | HTTP library for API calls |
| pandas-ta | 0.3.14b0 | Technical analysis indicators |

## Advanced Features

### Optional Dependencies

For advanced backtesting:

```bash
# Install backtesting frameworks
pip install vectorbtpro backtrader

# Or use development dependencies
pip install -e ".[backtesting,dev]"
```

## Configuration

Key environment variables:

- `BINANCE_API_KEY`: Binance API key
- `BINANCE_API_SECRET`: Binance API secret
- Other exchange credentials following the same pattern

## Development

### Code Style

This project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

### Contributing

1. Create a new branch for features
2. Write tests for new functionality
3. Ensure all tests pass
4. Follow PEP 8 style guidelines

## Important Notes

⚠️ **Risk Disclaimer**: 
- This is a development framework for educational purposes
- Never run trading with real money until thoroughly tested
- Always use small amounts for production testing
- Test strategies extensively with paper trading first

## Known Limitations

- Backtesting framework not yet integrated (planned feature)
- Rate limiting depends on exchange API
- Requires active internet connection for live trading

## Troubleshooting

### Connection Issues
```python
# Enable rate limiting for stability
exchange = ExchangeConnector('binance')
# Rate limiting is enabled by default
```

### Data Gaps
- Some exchanges have limited historical data
- Use `limit` parameter to adjust data retrieval

## Roadmap

- [ ] Integrate vectorbt for backtesting
- [ ] Add portfolio management tools
- [ ] Create web dashboard
- [ ] Add machine learning strategies
- [ ] Automated risk management

## Resources

- [CCXT Documentation](https://docs.ccxt.com/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NumPy Documentation](https://numpy.org/)

## License

This project is for educational purposes. Modify as needed for your use case.

## Support

For issues and questions:
1. Check existing issues in the project
2. Review exchange API documentation
3. Test with minimal amounts first

---

**Last Updated**: February 2026

