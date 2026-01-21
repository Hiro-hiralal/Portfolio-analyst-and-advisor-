from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Profile information
    age = Column(Integer)
    investable_amount = Column(Float)
    monthly_contribution = Column(Float)
    time_horizon = Column(Integer)  # in years
    location = Column(String)

    # Relationships
    risk_profile = relationship("RiskProfile", back_populates="user", uselist=False)
    portfolios = relationship("Portfolio", back_populates="user")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False)


class RiskProfile(Base):
    """Risk profile based on questionnaire responses"""
    __tablename__ = "risk_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)
    risk_score = Column(Integer)  # 0-100
    risk_category = Column(String)  # Conservative, Moderate, Aggressive
    questionnaire_responses = Column(JSON)  # Store all responses
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="risk_profile")


class UserPreferences(Base):
    """User investment preferences and constraints"""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)

    # Goals
    primary_goal = Column(String)  # retirement, home_purchase, education, wealth_building
    secondary_goals = Column(JSON)

    # Preferences
    esg_preference = Column(Boolean, default=False)
    sector_preferences = Column(JSON)  # List of preferred sectors
    sector_exclusions = Column(JSON)  # List of excluded sectors
    international_exposure = Column(Boolean, default=True)
    crypto_exposure = Column(Boolean, default=False)

    # Constraints
    max_single_position = Column(Float, default=0.15)  # Max 15% in single position
    rebalancing_frequency = Column(String, default="quarterly")  # monthly, quarterly, annually

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = relationship("User", back_populates="preferences")
