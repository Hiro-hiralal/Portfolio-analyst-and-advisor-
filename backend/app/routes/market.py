from fastapi import APIRouter, HTTPException
from app.models.schemas import SecurityInfo, MarketOverview
from app.services.market_data_service import MarketDataService

router = APIRouter(prefix="/market", tags=["market-data"])


@router.get("/overview", response_model=MarketOverview)
def get_market_overview():
    """Get overview of major market indices"""
    try:
        overview = MarketDataService.get_market_overview()
        return {
            "indices": overview["indices"],
            "sectors": [],  # Can be expanded later
            "trending": [],  # Can be expanded later
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market data: {str(e)}")


@router.get("/security/{symbol}", response_model=SecurityInfo)
def get_security_info(symbol: str):
    """Get detailed information about a security"""
    try:
        info = MarketDataService.get_security_info(symbol)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching security data: {str(e)}")


@router.get("/price/{symbol}")
def get_price(symbol: str):
    """Get current price for a symbol"""
    try:
        price = MarketDataService.get_current_price(symbol)
        if price is None:
            raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")
        return {"symbol": symbol, "price": price}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching price: {str(e)}")
