from typing import List, Optional, Tuple
from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..core.exceptions import BaseCustomException


class UserNotFoundError(BaseCustomException):
    def __init__(self):
        super().__init__("USER_NOT_FOUND", "User not found")


class DuplicateEmailError(BaseCustomException):
    def __init__(self):
        super().__init__("DUPLICATE_EMAIL", "Email already exists")


class DuplicateUsernameError(BaseCustomException):
    def __init__(self):
        super().__init__("DUPLICATE_USERNAME", "Username already exists")


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: dict, password_hash: str) -> User:
        # Check for existing email
        existing_email = await self.email_exists(user_data['email'])
        if existing_email:
            raise DuplicateEmailError()
        
        # Check for existing username
        existing_username = await self.username_exists(user_data['username'])
        if existing_username:
            raise DuplicateUsernameError()
        
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=password_hash,
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data.get('role', 'staff'),
            phone=user_data.get('phone'),
            department=user_data.get('department')
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int, include_deleted: bool = False) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        
        if not include_deleted:
            query = query.where(User.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, page: int = 1, page_size: int = 10) -> Tuple[List[User], int]:
        offset = (page - 1) * page_size
        
        # Get total count
        count_query = select(func.count(User.id)).where(User.deleted_at.is_(None))
        total_count = await self.db.scalar(count_query)
        
        # Get paginated results
        query = (
            select(User)
            .where(User.deleted_at.is_(None))
            .offset(offset)
            .limit(page_size)
            .order_by(User.created_at.desc())
        )
        
        result = await self.db.execute(query)
        users = result.scalars().all()
        
        return list(users), total_count

    async def get_deleted(self, page: int = 1, page_size: int = 10) -> Tuple[List[dict], int]:
        offset = (page - 1) * page_size
        
        # Get total count
        count_query = select(func.count(User.id)).where(User.deleted_at.is_not(None))
        total_count = await self.db.scalar(count_query)
        
        # Get paginated results
        query = (
            select(
                User.id,
                User.username,
                User.email,
                User.first_name,
                User.last_name,
                User.role,
                User.phone,
                User.department,
                User.is_active,
                User.created_at,
                User.updated_at,
                User.deleted_at,
                User.deleted_by
            )
            .where(User.deleted_at.is_not(None))
            .offset(offset)
            .limit(page_size)
            .order_by(User.deleted_at.desc())
        )
        
        result = await self.db.execute(query)
        users = []
        
        for row in result:
            users.append({
                'id': row.id,
                'username': row.username,
                'email': row.email,
                'first_name': row.first_name,
                'last_name': row.last_name,
                'role': row.role,
                'phone': row.phone,
                'department': row.department,
                'is_active': row.is_active,
                'created_at': row.created_at,
                'updated_at': row.updated_at,
                'deleted_at': row.deleted_at,
                'deleted_by': row.deleted_by
            })
        
        return users, total_count

    async def update(self, user_id: int, update_data: dict) -> User:
        # Check for existing email (if being updated)
        if 'email' in update_data:
            existing_email = await self.email_exists(update_data['email'], exclude_id=user_id)
            if existing_email:
                raise DuplicateEmailError()
        
        # Check for existing username (if being updated)
        if 'username' in update_data:
            existing_username = await self.username_exists(update_data['username'], exclude_id=user_id)
            if existing_username:
                raise DuplicateUsernameError()
        
        update_data["updated_at"] = func.now()
        
        stmt = update(User).where(User.id == user_id).values(**update_data).returning(User)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.scalar_one_or_none()

    async def soft_delete(self, user_id: int, deleted_by: str = None) -> bool:
        stmt = update(User).where(User.id == user_id).values(
            deleted_at=func.now(),
            deleted_by=deleted_by,
            is_active=False,
            updated_at=func.now()
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0

    async def restore(self, user_id: int) -> User:
        stmt = update(User).where(User.id == user_id).values(
            deleted_at=None,
            deleted_by=None,
            is_active=True,
            updated_at=func.now()
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        if result.rowcount == 0:
            return None
        
        # Return the restored user
        return await self.get_by_id(user_id)

    async def hard_delete(self, user_id: int) -> bool:
        """Permanently delete a user (use with caution)"""
        stmt = delete(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0

    async def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        query = select(User).where(User.email == email)
        
        if exclude_id:
            query = query.where(User.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def username_exists(self, username: str, exclude_id: Optional[int] = None) -> bool:
        query = select(User).where(User.username == username)
        
        if exclude_id:
            query = query.where(User.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(
            and_(
                User.email == email,
                User.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(
            and_(
                User.username == username,
                User.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
