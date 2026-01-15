import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class MarketDataService:
    """Service for fetching financial market data"""

    # Common market indices
    INDICES = {
        "^GSPC": "S&P 500",
        "^DJI": "Dow Jones",
        "^IXIC": "NASDAQ",
        "^RUT": "Russell 2000",
    }

    # Common ETFs for different asset classes
    ASSET_CLASS_ETFS = {
        "us_large_cap": "SPY",
        "us_mid_cap": "IJH",
        "us_small_cap": "IWM",
        "international_developed": "EFA",
        "emerging_markets": "EEM",
        "us_bonds": "AGG",
        "corporate_bonds": "LQD",
        "treasury_bonds": "TLT",
        "reits": "VNQ",
        "commodities": "DBC",
        "gold": "GLD",
    }

    @staticmethod
    def get_current_price(symbol: str) -> Optional[float]:
        """Get current price for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None

    @staticmethod
    def get_security_info(symbol: str) -> Dict:
        """Get detailed information about a security"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="5d")

            current_price = float(hist['Close'].iloc[-1]) if not hist.empty else 0
            prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
            change = current_price - prev_close
            change_pct = (change / prev_close * 100) if prev_close > 0 else 0

            return {
                "symbol": symbol,
                "name": info.get("longName", symbol),
                "price": current_price,
                "change": change,
                "change_pct": change_pct,
                "volume": info.get("volume"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
            }
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return {
                "symbol": symbol,
                "name": symbol,
                "price": 0,
                "change": 0,
                "change_pct": 0,
            }

    @staticmethod
    def get_historical_data(symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical price data for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_market_overview() -> Dict:
        """Get overview of major market indices"""
        indices_data = []
        for symbol, name in MarketDataService.INDICES.items():
            info = MarketDataService.get_security_info(symbol)
            indices_data.append({
                "symbol": symbol,
                "name": name,
                "price": info["price"],
                "change": info["change"],
                "change_pct": info["change_pct"],
            })

        return {
            "indices": indices_data,
            "last_updated": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_returns(symbol: str, period_days: int = 365) -> float:
        """Calculate annualized returns for a symbol"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period_days)

            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)

            if len(data) < 2:
                return 0.0

            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]

            total_return = (end_price - start_price) / start_price
            years = period_days / 365
            annualized_return = (1 + total_return) ** (1 / years) - 1

            return annualized_return
        except Exception as e:
            print(f"Error calculating returns for {symbol}: {e}")
            return 0.0

    @staticmethod
    def get_volatility(symbol: str, period: str = "1y") -> float:
        """Calculate annualized volatility for a symbol"""
        try:
            data = MarketDataService.get_historical_data(symbol, period)
            if data.empty:
                return 0.0

            # Calculate daily returns
            returns = data['Close'].pct_change().dropna()

            # Annualized volatility (252 trading days)
            volatility = returns.std() * (252 ** 0.5)
            return volatility
        except Exception as e:
            print(f"Error calculating volatility for {symbol}: {e}")
            return 0.0

    @staticmethod
    def get_correlation_matrix(symbols: List[str], period: str = "1y") -> pd.DataFrame:
        """Get correlation matrix for multiple symbols"""
        try:
            # Download data for all symbols
            data = yf.download(symbols, period=period, progress=False)['Close']

            # Calculate returns
            returns = data.pct_change().dropna()

            # Calculate correlation matrix
            corr_matrix = returns.corr()
            return corr_matrix
        except Exception as e:
            print(f"Error calculating correlation matrix: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_asset_class_returns() -> Dict[str, float]:
        """Get expected returns for different asset classes"""
        returns = {}
        for asset_class, symbol in MarketDataService.ASSET_CLASS_ETFS.items():
            returns[asset_class] = MarketDataService.get_returns(symbol, period_days=365)
        return returns

    @staticmethod
    def batch_get_prices(symbols: List[str]) -> Dict[str, float]:
        """Get current prices for multiple symbols"""
        prices = {}
        for symbol in symbols:
            price = MarketDataService.get_current_price(symbol)
            if price:
                prices[symbol] = price
        return prices
