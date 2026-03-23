import logging
from typing import List, Tuple
from ..repositories.user_repository import (
    UserRepository, 
    UserNotFoundError, 
    DuplicateEmailError, 
    DuplicateUsernameError
)
from ..models.user import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db):
        self.repository = UserRepository(db)

    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256"""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        import hashlib
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

    async def create_user(self, user_data: dict) -> User:
        """Create a new user with password hashing"""
        logger.info(f"Creating new user: {user_data['email']}")
        
        # Hash password
        password_hash = self.hash_password(user_data.pop('password'))
        
        return await self.repository.create(user_data, password_hash)

    async def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        user = await self.repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise UserNotFoundError()
        return user

    async def get_all_users(self, page: int = 1, page_size: int = 10) -> Tuple[List[User], int]:
        """Get all users with pagination"""
        logger.info(f"Fetching users page {page}")
        return await self.repository.get_all(page, page_size)

    async def get_deleted_users(self, page: int = 1, page_size: int = 10) -> Tuple[List[dict], int]:
        """Get all deleted users with pagination"""
        logger.info(f"Fetching deleted users page {page}")
        return await self.repository.get_deleted(page, page_size)

    async def update_user(self, user_id: int, update_data: dict) -> User:
        """Update user information"""
        logger.info(f"Updating user: {user_id}")
        
        # Hash password if it's being updated
        if 'password' in update_data:
            update_data['password_hash'] = self.hash_password(update_data.pop('password'))
        
        user = await self.repository.update(user_id, update_data)
        if not user:
            logger.warning(f"User not found for update: {user_id}")
            raise UserNotFoundError()
        
        return user

    async def soft_delete_user(self, user_id: int, deleted_by: str = None) -> None:
        """Soft delete a user"""
        logger.info(f"Soft deleting user: {user_id}")
        
        user = await self.repository.get_by_id(user_id)
        if not user:
            logger.warning(f"User not found for deletion: {user_id}")
            raise UserNotFoundError()
        
        await self.repository.soft_delete(user_id, deleted_by)
        logger.info(f"User soft deleted successfully: {user_id}")

    async def restore_user(self, user_id: int) -> User:
        """Restore a soft deleted user"""
        logger.info(f"Restoring user: {user_id}")
        
        existing_user = await self.repository.get_by_id(user_id, include_deleted=True)
        if not existing_user:
            logger.warning(f"User not found for restore: {user_id}")
            raise UserNotFoundError()
        
        if not existing_user.deleted_at:
            logger.warning(f"User is not deleted: {user_id}")
            from ..core.exceptions import ValidationError
            raise ValidationError("User is not deleted", "user_id")
        
        restored_user = await self.repository.restore(user_id)
        logger.info(f"User restored successfully: {user_id}")
        return restored_user

    async def hard_delete_user(self, user_id: int) -> None:
        """Permanently delete a user"""
        logger.warning(f"Hard deleting user: {user_id}")
        
        user = await self.repository.get_by_id(user_id, include_deleted=True)
        if not user:
            logger.warning(f"User not found for hard deletion: {user_id}")
            raise UserNotFoundError()
        
        await self.repository.hard_delete(user_id)
        logger.warning(f"User permanently deleted: {user_id}")

    async def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        logger.info(f"Authenticating user: {email}")
        
        user = await self.repository.get_by_email(email)
        if not user:
            logger.warning(f"Authentication failed - user not found: {email}")
            from ..core.exceptions import ValidationError
            raise ValidationError("Invalid credentials", "authentication")
        
        if not self.verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed - invalid password: {email}")
            from ..core.exceptions import ValidationError
            raise ValidationError("Invalid credentials", "authentication")
        
        if not user.is_active:
            logger.warning(f"Authentication failed - user inactive: {email}")
            from ..core.exceptions import ValidationError
            raise ValidationError("Account is inactive", "authentication")
        
        logger.info(f"User authenticated successfully: {email}")
        return user

    async def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        return await self.repository.get_by_email(email)

    async def get_user_by_username(self, username: str) -> User:
        """Get user by username"""
        return await self.repository.get_by_username(username)
