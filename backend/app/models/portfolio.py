from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Portfolio(Base):
    """User portfolio with holdings and allocations"""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, default="My Portfolio")
    is_active = Column(Integer, default=1)

    # Portfolio metrics
    total_value = Column(Float, default=0.0)
    total_return = Column(Float, default=0.0)
    total_return_pct = Column(Float, default=0.0)

    # Allocation
    allocation = Column(JSON)  # {"stocks": 60, "bonds": 30, "cash": 10}
    target_allocation = Column(JSON)

    # Risk metrics
    volatility = Column(Float)
    sharpe_ratio = Column(Float)
    beta = Column(Float)
    max_drawdown = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="portfolios")
    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")


class Holding(Base):
    """Individual holdings within a portfolio"""
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    # Security info
    symbol = Column(String, nullable=False)
    name = Column(String)
    asset_class = Column(String)  # equity, bond, reit, commodity, crypto, cash
    sector = Column(String)

    # Position info
    shares = Column(Float, default=0.0)
    average_cost = Column(Float, default=0.0)
    current_price = Column(Float, default=0.0)
    current_value = Column(Float, default=0.0)
    allocation_pct = Column(Float, default=0.0)

    # Performance
    total_return = Column(Float, default=0.0)
    total_return_pct = Column(Float, default=0.0)
    day_return = Column(Float, default=0.0)
    day_return_pct = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    portfolio = relationship("Portfolio", back_populates="holdings")


class PortfolioRecommendation(Base):
    """Portfolio recommendations generated for users"""
    __tablename__ = "portfolio_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Recommendation details
    recommended_allocation = Column(JSON)
    recommended_holdings = Column(JSON)  # List of securities with amounts
    expected_return = Column(Float)
    expected_volatility = Column(Float)
    sharpe_ratio = Column(Float)

    # Strategy used
    strategy = Column(String)  # mpt, risk_parity, black_litterman
    risk_category = Column(String)

    # Metadata
    rationale = Column(JSON)  # Explanation for recommendations
    created_at = Column(DateTime, default=datetime.utcnow)

    # Note: No direct relationship to User to keep it simple
