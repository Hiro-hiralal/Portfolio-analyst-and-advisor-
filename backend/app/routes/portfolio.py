from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, RiskProfile
from app.models.portfolio import Portfolio, PortfolioRecommendation
from app.models.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    PortfolioResponse,
    ScenarioRequest,
    ScenarioResult,
    MonteCarloRequest,
    MonteCarloResult,
)
from app.services.portfolio_service import (
    PortfolioRecommendationEngine,
    ScenarioAnalysisEngine,
)

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.post("/recommendation", response_model=RecommendationResponse)
def get_portfolio_recommendation(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate portfolio recommendation based on user profile"""

    # Get user's risk profile
    risk_profile = db.query(RiskProfile).filter(RiskProfile.user_id == current_user.id).first()
    if not risk_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please complete risk assessment questionnaire first"
        )

    # Get user's investable amount
    if not current_user.investable_amount or current_user.investable_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please set your investable amount in profile"
        )

    # Generate recommendation
    recommendation = PortfolioRecommendationEngine.generate_recommendation(
        risk_category=risk_profile.risk_category,
        investable_amount=current_user.investable_amount,
        preferences=None  # TODO: Add preferences support
    )

    # Save recommendation to database
    db_recommendation = PortfolioRecommendation(
        user_id=current_user.id,
        recommended_allocation=recommendation["recommended_allocation"],
        recommended_holdings=recommendation["recommended_holdings"],
        expected_return=recommendation["expected_return"],
        expected_volatility=recommendation["expected_volatility"],
        sharpe_ratio=recommendation["sharpe_ratio"],
        strategy=recommendation["strategy"],
        risk_category=recommendation["risk_category"],
        rationale=recommendation["rationale"],
    )
    db.add(db_recommendation)
    db.commit()

    return recommendation


@router.get("/recommendations", response_model=List[RecommendationResponse])
def get_user_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all recommendations for current user"""
    recommendations = db.query(PortfolioRecommendation).filter(
        PortfolioRecommendation.user_id == current_user.id
    ).order_by(PortfolioRecommendation.created_at.desc()).limit(10).all()

    return [
        {
            "recommended_allocation": rec.recommended_allocation,
            "recommended_holdings": rec.recommended_holdings,
            "expected_return": rec.expected_return,
            "expected_volatility": rec.expected_volatility,
            "sharpe_ratio": rec.sharpe_ratio,
            "strategy": rec.strategy,
            "risk_category": rec.risk_category,
            "rationale": rec.rationale,
        }
        for rec in recommendations
    ]


@router.get("/current", response_model=PortfolioResponse)
def get_current_portfolio(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's current portfolio"""
    portfolio = db.query(Portfolio).filter(
        Portfolio.user_id == current_user.id,
        Portfolio.is_active == 1
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active portfolio found"
        )

    return portfolio


@router.post("/scenario", response_model=ScenarioResult)
def run_scenario_analysis(
    request: ScenarioRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Run scenario analysis on portfolio"""

    # Get latest recommendation or use current values
    recommendation = db.query(PortfolioRecommendation).filter(
        PortfolioRecommendation.user_id == current_user.id
    ).order_by(PortfolioRecommendation.created_at.desc()).first()

    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please generate a portfolio recommendation first"
        )

    portfolio_value = current_user.investable_amount or 10000
    allocation = recommendation.recommended_allocation

    # Run scenario
    if request.scenario_type == "predefined":
        result = ScenarioAnalysisEngine.run_scenario(
            portfolio_value=portfolio_value,
            allocation=allocation,
            scenario_name=request.scenario_name
        )
    else:  # custom
        custom_returns = {
            "stocks": request.stock_return or 0,
            "bonds": request.bond_return or 0,
            "alternatives": 0,
            "cash": 0,
        }
        result = ScenarioAnalysisEngine.run_scenario(
            portfolio_value=portfolio_value,
            allocation=allocation,
            custom_returns=custom_returns
        )

    return result


@router.get("/scenarios")
def get_available_scenarios():
    """Get list of available predefined scenarios"""
    scenarios = []
    for key, value in ScenarioAnalysisEngine.PREDEFINED_SCENARIOS.items():
        scenarios.append({
            "id": key,
            "name": value["name"],
            "description": f"Stock: {value['stock_return']*100:+.0f}%, Bond: {value['bond_return']*100:+.0f}%"
        })
    return {"scenarios": scenarios}


@router.post("/monte-carlo", response_model=MonteCarloResult)
def run_monte_carlo_simulation(
    request: MonteCarloRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Run Monte Carlo simulation for portfolio projections"""

    # Get latest recommendation
    recommendation = db.query(PortfolioRecommendation).filter(
        PortfolioRecommendation.user_id == current_user.id
    ).order_by(PortfolioRecommendation.created_at.desc()).first()

    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please generate a portfolio recommendation first"
        )

    portfolio_value = current_user.investable_amount or 10000
    monthly_contribution = current_user.monthly_contribution or 0

    # Run Monte Carlo simulation
    result = ScenarioAnalysisEngine.monte_carlo_simulation(
        portfolio_value=portfolio_value,
        expected_return=recommendation.expected_return,
        volatility=recommendation.expected_volatility,
        years=request.time_horizon,
        num_simulations=request.num_simulations,
        monthly_contribution=monthly_contribution
    )

    return result
