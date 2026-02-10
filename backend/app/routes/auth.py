from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.schemas import UserCreate, UserLogin, Token, UserResponse, RefreshTokenRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    user = AuthService.create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get access + refresh tokens"""
    user = AuthService.authenticate_user(db, credentials.email, credentials.password)
    token = AuthService.create_token(user)
    return token


@router.post("/refresh", response_model=Token)
def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Exchange a refresh token for new access + refresh tokens"""
    return AuthService.refresh_access_token(body.refresh_token, db)


@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.post("/logout")
def logout():
    """Logout (client-side token removal)"""
    return {"message": "Successfully logged out"}
