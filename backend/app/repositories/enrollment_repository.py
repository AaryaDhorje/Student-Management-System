from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete, update, func
from sqlalchemy.orm import selectinload
from ..models.enrollment import Enrollment
from ..models.student import Student
from ..models.course import Course


class EnrollmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, enrollment: Enrollment) -> Enrollment:
        self.db.add(enrollment)
        await self.db.commit()
        await self.db.refresh(enrollment)
        return enrollment
    
    async def get_by_id(self, enrollment_id: int, include_deleted: bool = False) -> Optional[Enrollment]:
        query = select(Enrollment).where(Enrollment.id == enrollment_id)
        
        if not include_deleted:
            query = query.where(Enrollment.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_student_courses(self, student_id: int, include_deleted: bool = False) -> List[dict]:
        query = (
            select(
                Course.id.label('course_id'),
                Course.course_name,
                Course.course_code,
                Enrollment.created_at.label('enrollment_date'),
                Enrollment.deleted_at.label('deleted_at'),
                Enrollment.deleted_by.label('deleted_by')
            )
            .select_from(Enrollment)
            .join(Course, Enrollment.course_id == Course.id)
            .where(Enrollment.student_id == student_id)
        )
        
        if not include_deleted:
            query = query.where(Enrollment.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        courses = result.all()
        
        return [dict(row._mapping) for row in courses]
    
    async def get_course_students(self, course_id: int, include_deleted: bool = False) -> List[dict]:
        query = (
            select(
                Student.id.label('student_id'),
                Student.first_name,
                Student.last_name,
                Student.email,
                Enrollment.created_at.label('enrollment_date'),
                Enrollment.deleted_at.label('deleted_at'),
                Enrollment.deleted_by.label('deleted_by')
            )
            .select_from(Enrollment)
            .join(Student, Enrollment.student_id == Student.id)
            .where(Enrollment.course_id == course_id)
        )
        
        if not include_deleted:
            query = query.where(Enrollment.deleted_at.is_(None))
        
        result = await self.db.execute(query)
        students = result.all()
        
        return [dict(row._mapping) for row in students]
    
    async def exists(self, student_id: int, course_id: int) -> bool:
        result = await self.db.execute(
            select(Enrollment).where(
                and_(
                    Enrollment.student_id == student_id,
                    Enrollment.course_id == course_id,
                    Enrollment.deleted_at.is_(None)
                )
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def soft_delete(self, enrollment_id: int, deleted_by: str = None) -> bool:
        stmt = update(Enrollment).where(Enrollment.id == enrollment_id).values(
            deleted_at=func.now(),
            deleted_by=deleted_by
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    async def soft_delete_by_student_course(self, student_id: int, course_id: int, deleted_by: str = None) -> bool:
        stmt = update(Enrollment).where(
            and_(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id,
                Enrollment.deleted_at.is_(None)
            )
        ).values(
            deleted_at=func.now(),
            deleted_by=deleted_by
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    async def restore(self, enrollment_id: int) -> Enrollment:
        stmt = update(Enrollment).where(Enrollment.id == enrollment_id).values(
            deleted_at=None,
            deleted_by=None
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        if result.rowcount == 0:
            return None
        
        # Return the restored enrollment
        return await self.get_by_id(enrollment_id)
    
    async def restore_by_student_course(self, student_id: int, course_id: int) -> Enrollment:
        stmt = update(Enrollment).where(
            and_(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id,
                Enrollment.deleted_at.is_not(None)
            )
        ).values(
            deleted_at=None,
            deleted_by=None
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        if result.rowcount == 0:
            return None
        
        # Return the restored enrollment
        enrollments = await self.get_student_courses(student_id, include_deleted=True)
        for enrollment in enrollments:
            if enrollment['course_id'] == course_id and not enrollment.get('deleted_at'):
                return Enrollment(
                    id=enrollment.get('id'),
                    student_id=student_id,
                    course_id=course_id
                )
        
        return None
    
    async def hard_delete(self, enrollment_id: int) -> bool:
        """Permanently delete an enrollment (use with caution)"""
        stmt = delete(Enrollment).where(Enrollment.id == enrollment_id)
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    async def hard_delete_by_student_course(self, student_id: int, course_id: int) -> bool:
        """Permanently delete enrollment by student and course (use with caution)"""
        stmt = delete(Enrollment).where(
            and_(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id
            )
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        
        return result.rowcount > 0
    
    async def get_deleted(
        self, 
        page: int = 1, 
        page_size: int = 10
    ) -> List[dict]:
        offset = (page - 1) * page_size
        
        query = (
            select(
                Enrollment.id,
                Enrollment.student_id,
                Enrollment.course_id,
                Enrollment.created_at,
                Enrollment.deleted_at,
                Enrollment.deleted_by,
                Student.first_name,
                Student.last_name,
                Student.email,
                Course.course_name,
                Course.course_code
            )
            .select_from(Enrollment)
            .join(Student, Enrollment.student_id == Student.id)
            .join(Course, Enrollment.course_id == Course.id)
            .where(Enrollment.deleted_at.is_not(None))
            .offset(offset)
            .limit(page_size)
        )
        
        result = await self.db.execute(query)
        enrollments = result.all()
        
        return [dict(row._mapping) for row in enrollments]
