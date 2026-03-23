import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.config import settings
from ..models.user import User
from ..core.database import get_db

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token
security = HTTPBearer()

class AuthService:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except:
            # Fallback to SHA-256 if bcrypt fails
            return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        try:
            return pwd_context.hash(password)
        except:
            # Fallback to SHA-256 if bcrypt fails
            return hashlib.sha256(password.encode()).hexdigest()

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def authenticate_user(self, db: AsyncSession, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password"""
        stmt = select(User).where(
            (User.username == username) | (User.email == username),
            User.is_active == True,
            User.deleted_at.is_(None)
        )
        
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        return user

    async def get_current_user(
        self, 
        db: AsyncSession = Depends(get_db),
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        """Get the current authenticated user"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = self.verify_token(credentials.credentials)
            user_id: int = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        stmt = select(User).where(
            User.id == user_id,
            User.is_active == True,
            User.deleted_at.is_(None)
        )
        
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user is None:
            raise credentials_exception
        
        return user

    def get_current_active_user(
        self, 
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get the current active user"""
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    def get_current_admin_user(
        self, 
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        """Get the current admin user (admin only)"""
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions - Admin access required"
            )
        return current_user

    def get_current_staff_or_admin_user(
        self, 
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        """Get the current staff or admin user"""
        if current_user.role not in ["staff", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions - Staff or Admin access required"
            )
        return current_user

# Create singleton instance
auth_service = AuthService()

# Dependency functions
get_current_user = auth_service.get_current_user
get_current_active_user = auth_service.get_current_active_user
get_current_admin_user = auth_service.get_current_admin_user
get_current_staff_or_admin_user = auth_service.get_current_staff_or_admin_user
