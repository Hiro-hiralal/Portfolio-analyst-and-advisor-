from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User, RiskProfile
from app.models.schemas import RiskQuestionnaireResponse, RiskProfileResponse
from app.services.portfolio_service import PortfolioRecommendationEngine

router = APIRouter(prefix="/risk", tags=["risk-assessment"])


@router.post("/questionnaire", response_model=RiskProfileResponse)
def submit_risk_questionnaire(
    responses: RiskQuestionnaireResponse,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit risk assessment questionnaire and get risk profile"""

    # Convert responses to dict
    responses_dict = responses.model_dump()

    # Calculate risk score
    risk_score, risk_category = PortfolioRecommendationEngine.calculate_risk_score(responses_dict)

    # Check if user already has a risk profile
    existing_profile = db.query(RiskProfile).filter(RiskProfile.user_id == current_user.id).first()

    if existing_profile:
        # Update existing profile
        existing_profile.risk_score = risk_score
        existing_profile.risk_category = risk_category
        existing_profile.questionnaire_responses = responses_dict
        db_profile = existing_profile
    else:
        # Create new profile
        db_profile = RiskProfile(
            user_id=current_user.id,
            risk_score=risk_score,
            risk_category=risk_category,
            questionnaire_responses=responses_dict
        )
        db.add(db_profile)

    db.commit()
    db.refresh(db_profile)

    return db_profile


@router.get("/profile", response_model=RiskProfileResponse)
def get_risk_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's risk profile"""
    profile = db.query(RiskProfile).filter(RiskProfile.user_id == current_user.id).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk profile not found. Please complete the questionnaire."
        )

    return profile


@router.get("/questionnaire")
def get_questionnaire():
    """Get risk assessment questionnaire questions"""
    return {
        "questions": [
            {
                "id": "question_1",
                "text": "What is your investment time horizon?",
                "options": [
                    {"value": "less_than_3", "label": "Less than 3 years"},
                    {"value": "3_to_5", "label": "3-5 years"},
                    {"value": "5_to_10", "label": "5-10 years"},
                    {"value": "10_to_20", "label": "10-20 years"},
                    {"value": "more_than_20", "label": "More than 20 years"},
                ]
            },
            {
                "id": "question_2",
                "text": "How would you react if your portfolio lost 20% in one month?",
                "options": [
                    {"value": "sell_all", "label": "Sell everything immediately"},
                    {"value": "sell_some", "label": "Sell some holdings to reduce risk"},
                    {"value": "do_nothing", "label": "Do nothing and wait it out"},
                    {"value": "buy_more", "label": "Buy more while prices are low"},
                ]
            },
            {
                "id": "question_3",
                "text": "What is your primary investment goal?",
                "options": [
                    {"value": "preservation", "label": "Preserve capital"},
                    {"value": "income", "label": "Generate income"},
                    {"value": "balanced", "label": "Balanced growth"},
                    {"value": "growth", "label": "Long-term growth"},
                    {"value": "aggressive_growth", "label": "Aggressive growth"},
                ]
            },
            {
                "id": "question_4",
                "text": "What percentage loss can you tolerate in a year?",
                "options": [
                    {"value": "0_to_5", "label": "0-5%"},
                    {"value": "5_to_10", "label": "5-10%"},
                    {"value": "10_to_20", "label": "10-20%"},
                    {"value": "20_plus", "label": "20% or more"},
                ]
            },
            {
                "id": "question_5",
                "text": "What is your investment experience level?",
                "options": [
                    {"value": "none", "label": "No experience"},
                    {"value": "beginner", "label": "Beginner (< 2 years)"},
                    {"value": "intermediate", "label": "Intermediate (2-5 years)"},
                    {"value": "advanced", "label": "Advanced (> 5 years)"},
                ]
            },
            {
                "id": "question_6",
                "text": "Do you have an emergency fund covering 3-6 months of expenses?",
                "options": [
                    {"value": "no", "label": "No"},
                    {"value": "partial", "label": "Partially (1-3 months)"},
                    {"value": "yes", "label": "Yes (3-6+ months)"},
                ]
            },
            {
                "id": "question_7",
                "text": "How stable is your income?",
                "options": [
                    {"value": "unstable", "label": "Unstable or variable"},
                    {"value": "somewhat_stable", "label": "Somewhat stable"},
                    {"value": "stable", "label": "Very stable"},
                ]
            },
            {
                "id": "question_8",
                "text": "How would you rate your knowledge of financial markets?",
                "options": [
                    {"value": "low", "label": "Low - I'm still learning"},
                    {"value": "moderate", "label": "Moderate - I understand the basics"},
                    {"value": "high", "label": "High - I follow markets regularly"},
                ]
            },
        ]
    }
