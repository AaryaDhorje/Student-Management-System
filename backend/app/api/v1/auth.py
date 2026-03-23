from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from typing import Optional

from ...core.database import get_db
from ...core.config import settings
from ...services.auth_service import auth_service
from ...models.user import User

router = APIRouter()

# Pydantic models for authentication
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str  # Can be username or email
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    phone: Optional[str] = None
    department: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

@router.post("/auth/login", response_model=Token)
async def login(login_data: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    """Authenticate user and return access token"""
    # Authenticate user
    user = await auth_service.authenticate_user(db, login_data.username, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    # Return token and user info
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": auth_service.access_token_expire_minutes * 60,  # Convert to seconds
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_active": user.is_active,
            "phone": user.phone,
            "department": user.department,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
    }

@router.post("/auth/login-form", response_model=Token)
async def login_form(db: Annotated[AsyncSession, Depends(get_db)], form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user using form data (for OAuth2 compatibility)"""
    # Authenticate user
    user = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    # Return token and user info
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": auth_service.access_token_expire_minutes * 60,  # Convert to seconds
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_active": user.is_active,
            "phone": user.phone,
            "department": user.department,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        }
    }

@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(auth_service.get_current_active_user)):
    """Get current user information"""
    return current_user

@router.post("/auth/logout")
async def logout():
    """Logout user (client-side token removal)"""
    # In a stateless JWT system, logout is handled client-side
    # This endpoint can be used for logging or to invalidate tokens in a blacklist system
    return {"message": "Successfully logged out"}

@router.get("/auth/verify-token")
async def verify_token(current_user: User = Depends(auth_service.get_current_user)):
    """Verify if the current token is valid"""
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role,
            "email": current_user.email,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
        }
    }
