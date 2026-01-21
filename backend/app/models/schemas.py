from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Authentication schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# User profile schemas
class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=18, le=100)
    investable_amount: Optional[float] = Field(None, ge=0)
    monthly_contribution: Optional[float] = Field(None, ge=0)
    time_horizon: Optional[int] = Field(None, ge=1, le=50)
    location: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    age: Optional[int]
    investable_amount: Optional[float]
    monthly_contribution: Optional[float]
    time_horizon: Optional[int]
    location: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Risk assessment schemas
class RiskQuestionnaireResponse(BaseModel):
    question_1: str  # Time horizon
    question_2: str  # Reaction to loss
    question_3: str  # Primary goal
    question_4: str  # Loss tolerance
    question_5: str  # Investment experience
    question_6: str  # Emergency savings
    question_7: str  # Income stability
    question_8: str  # Market knowledge


class RiskProfileResponse(BaseModel):
    id: int
    risk_score: int
    risk_category: str
    questionnaire_responses: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


# Preferences schemas
class UserPreferencesUpdate(BaseModel):
    primary_goal: Optional[str] = None
    secondary_goals: Optional[List[str]] = None
    esg_preference: Optional[bool] = None
    sector_preferences: Optional[List[str]] = None
    sector_exclusions: Optional[List[str]] = None
    international_exposure: Optional[bool] = None
    crypto_exposure: Optional[bool] = None
    max_single_position: Optional[float] = Field(None, ge=0.01, le=0.5)
    rebalancing_frequency: Optional[str] = None


class UserPreferencesResponse(BaseModel):
    id: int
    primary_goal: Optional[str]
    secondary_goals: Optional[List[str]]
    esg_preference: bool
    sector_preferences: Optional[List[str]]
    sector_exclusions: Optional[List[str]]
    international_exposure: bool
    crypto_exposure: bool
    max_single_position: float
    rebalancing_frequency: str

    class Config:
        from_attributes = True


# Portfolio schemas
class HoldingResponse(BaseModel):
    id: int
    symbol: str
    name: Optional[str]
    asset_class: Optional[str]
    sector: Optional[str]
    shares: float
    average_cost: float
    current_price: float
    current_value: float
    allocation_pct: float
    total_return: float
    total_return_pct: float
    day_return: float
    day_return_pct: float

    class Config:
        from_attributes = True


class PortfolioResponse(BaseModel):
    id: int
    name: str
    total_value: float
    total_return: float
    total_return_pct: float
    allocation: Optional[Dict[str, float]]
    target_allocation: Optional[Dict[str, float]]
    volatility: Optional[float]
    sharpe_ratio: Optional[float]
    beta: Optional[float]
    max_drawdown: Optional[float]
    holdings: List[HoldingResponse] = []

    class Config:
        from_attributes = True


# Recommendation schemas
class RecommendationRequest(BaseModel):
    """Request for portfolio recommendation"""
    pass  # Uses user's existing profile, risk, and preferences


class RecommendationResponse(BaseModel):
    recommended_allocation: Dict[str, float]
    recommended_holdings: List[Dict[str, Any]]
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    strategy: str
    risk_category: str
    rationale: Dict[str, Any]


# Market data schemas
class SecurityInfo(BaseModel):
    symbol: str
    name: str
    price: float
    change: float
    change_pct: float
    volume: Optional[int]
    market_cap: Optional[float]
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]


class MarketOverview(BaseModel):
    indices: List[Dict[str, Any]]
    sectors: List[Dict[str, Any]]
    trending: List[SecurityInfo]


# Scenario analysis schemas
class ScenarioRequest(BaseModel):
    scenario_type: str  # predefined or custom
    scenario_name: Optional[str] = None  # For predefined: market_crash, recession, etc.

    # For custom scenarios
    stock_return: Optional[float] = None
    bond_return: Optional[float] = None
    inflation_rate: Optional[float] = None
    time_period: Optional[int] = None  # months


class ScenarioResult(BaseModel):
    scenario_name: str
    projected_value: float
    expected_gain_loss: float
    expected_gain_loss_pct: float
    recovery_time_months: Optional[int]
    recommendations: List[str]


class MonteCarloRequest(BaseModel):
    num_simulations: int = Field(1000, ge=100, le=10000)
    time_horizon: int = Field(10, ge=1, le=50)  # years


class MonteCarloResult(BaseModel):
    simulations: int
    percentiles: Dict[str, float]  # 10th, 25th, 50th, 75th, 90th
    probability_of_goal: float
    expected_value: float
    worst_case: float
    best_case: float
