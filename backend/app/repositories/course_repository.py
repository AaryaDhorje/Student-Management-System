from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete
from ..models.course import Course


class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, course: Course) -> Course:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course
    
    async def get_by_id(self, course_id: int, include_deleted: bool = False) -> Optional[Course]:
        query = select(Course).where(Course.id == course_id)
        
        if not include_deleted:
            query = query.where(Course.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_code(self, course_code: str, include_deleted: bool = False) -> Optional[Course]:
        query = select(Course).where(Course.course_code == course_code)
        
        if not include_deleted:
            query = query.where(Course.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(
        self, 
        page: int = 1, 
        page_size: int = 10,
        include_deleted: bool = False
    ) -> Tuple[List[Course], int]:
        offset = (page - 1) * page_size
        
        count_query = select(func.count()).select_from(Course)
        if not include_deleted:
            count_query = count_query.where(Course.deleted_at.is_(None))
        
        total_count = await self.db.scalar(count_query)
        
        query = select(Course).offset(offset).limit(page_size)
        if not include_deleted:
            query = query.where(Course.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        courses = result.scalars().all()
        
        return list(courses), total_count
    
    async def get_deleted(
        self, 
        page: int = 1, 
        page_size: int = 10
    ) -> Tuple[List[Course], int]:
        offset = (page - 1) * page_size
        
        count_query = select(func.count()).select_from(Course).where(Course.deleted_at.is_not(None))
        total_count = await self.db.scalar(count_query)
        
        query = select(Course).where(Course.deleted_at.is_not(None)).offset(offset).limit(page_size)
        result = await self.db.execute(query)
        courses = result.scalars().all()
        
        return list(courses), total_count
    
    async def update(self, course_id: int, update_data: Dict[str, Any]) -> Optional[Course]:
        update_data["updated_at"] = func.now()
        
        stmt = update(Course).where(Course.id == course_id).values(**update_data).returning(Course)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.scalar_one_or_none()
    
    async def soft_delete(self, course_id: int, deleted_by: str = None) -> bool:
        stmt = update(Course).where(Course.id == course_id).values(
            deleted_at=func.now(),
            deleted_by=deleted_by,
            updated_at=func.now()
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    async def restore(self, course_id: int) -> Course:
        stmt = update(Course).where(Course.id == course_id).values(
            deleted_at=None,
            deleted_by=None,
            updated_at=func.now()
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        if result.rowcount == 0:
            return None
        
        # Return the restored course
        return await self.get_by_id(course_id)
    
    async def hard_delete(self, course_id: int) -> bool:
        """Permanently delete a course (use with caution)"""
        stmt = delete(Course).where(Course.id == course_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    async def course_code_exists(self, course_code: str, exclude_id: Optional[int] = None) -> bool:
        query = select(Course).where(Course.course_code == course_code, Course.deleted_at.is_(None))
        
        if exclude_id:
            query = query.where(Course.id != exclude_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
