from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, update
from sqlalchemy.orm import selectinload
from ..models.student import Student


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, student: Student) -> Student:
        self.db.add(student)
        await self.db.commit()
        await self.db.refresh(student)
        return student
    
    async def get_by_id(self, student_id: int, include_deleted: bool = False) -> Optional[Student]:
        query = select(Student).where(Student.id == student_id)
        
        if not include_deleted:
            query = query.where(Student.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str, include_deleted: bool = False) -> Optional[Student]:
        query = select(Student).where(Student.email == email)
        
        if not include_deleted:
            query = query.where(Student.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        page: int = 1, 
        page_size: int = 10,
        include_deleted: bool = False
    ) -> Tuple[List[Student], int]:
        offset = (page - 1) * page_size
        
        count_query = select(func.count()).select_from(Student)
        if not include_deleted:
            count_query = count_query.where(Student.deleted_at.is_(None))
        
        total_count = await self.db.scalar(count_query)
        
        query = select(Student).offset(offset).limit(page_size)
        if not include_deleted:
            query = query.where(Student.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        students = result.scalars().all()
        
        return list(students), total_count
    
    async def get_deleted(
        self, 
        page: int = 1, 
        page_size: int = 10
    ) -> Tuple[List[Student], int]:
        offset = (page - 1) * page_size
        
        count_query = select(func.count()).select_from(Student).where(Student.deleted_at.is_not(None))
        total_count = await self.db.scalar(count_query)
        
        query = select(Student).where(Student.deleted_at.is_not(None)).offset(offset).limit(page_size)
        result = await self.db.execute(query)
        students = result.scalars().all()
        
        return list(students), total_count
    
    async def update(self, student_id: int, update_data: Dict[str, Any]) -> Optional[Student]:
        update_data["updated_at"] = func.now()
        
        stmt = update(Student).where(Student.id == student_id).values(**update_data).returning(Student)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.scalar_one_or_none()
    
    async def soft_delete(self, student_id: int, deleted_by: str = None) -> bool:
        stmt = update(Student).where(Student.id == student_id).values(
            deleted_at=func.now(),
            deleted_by=deleted_by,
            is_active=False,
            updated_at=func.now()
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    async def restore(self, student_id: int) -> Student:
        stmt = update(Student).where(Student.id == student_id).values(
            deleted_at=None,
            deleted_by=None,
            is_active=True,
            updated_at=func.now()
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        if result.rowcount == 0:
            return None
        
        # Return the restored student
        return await self.get_by_id(student_id)
    
    async def hard_delete(self, student_id: int) -> bool:
        """Permanently delete a student (use with caution)"""
        from sqlalchemy import delete
        stmt = delete(Student).where(Student.id == student_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    async def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        query = select(Student).where(Student.email == email, Student.deleted_at.is_(None))
        
        if exclude_id:
            query = query.where(Student.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
