import uuid
import logging
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.student import Student
from ..schemas.student_schema import StudentCreateSchema, StudentUpdateSchema
from ..repositories.student_repository import StudentRepository
from ..core.exceptions import DuplicateEmailError, StudentNotFoundError, ValidationError

logger = logging.getLogger(__name__)


class StudentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = StudentRepository(db)
    
    async def create_student(self, student_data: StudentCreateSchema) -> Student:
        logger.info(f"Creating student with email: {student_data.email}")
        
        existing_student = await self.repository.get_by_email(student_data.email)
        if existing_student:
            logger.warning(f"Duplicate email attempt: {student_data.email}")
            raise DuplicateEmailError()
        
        student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            email=student_data.email,
            enrollment_date=student_data.enrollment_date
        )
        
        created_student = await self.repository.create(student)
        logger.info(f"Student created successfully: {created_student.id}")
        return created_student
    
    async def get_student(self, student_id: int) -> Student:
        student = await self.repository.get_by_id(student_id)
        if not student:
            logger.warning(f"Student not found: {student_id}")
            raise StudentNotFoundError()
        
        return student
    
    async def get_students(self, page: int = 1, page_size: int = 10) -> Tuple[List[Student], int]:
        if page < 1:
            raise ValidationError("Page must be greater than 0", "page")
        if page_size < 1 or page_size > 100:
            raise ValidationError("Page size must be between 1 and 100", "page_size")
        
        students, total_count = await self.repository.get_all(page, page_size)
        logger.info(f"Retrieved {len(students)} students, page {page}")
        return students, total_count
    
    async def update_student(self, student_id: int, student_data: StudentUpdateSchema) -> Student:
        existing_student = await self.repository.get_by_id(student_id)
        if not existing_student:
            logger.warning(f"Student not found for update: {student_id}")
            raise StudentNotFoundError()
        
        if student_data.email and student_data.email != existing_student.email:
            email_exists = await self.repository.get_by_email(student_data.email)
            if email_exists:
                logger.warning(f"Duplicate email attempt during update: {student_data.email}")
                raise DuplicateEmailError()
        
        update_data = student_data.model_dump(exclude_unset=True)
        updated_student = await self.repository.update(student_id, update_data)
        logger.info(f"Student updated successfully: {student_id}")
        return updated_student
    
    async def delete_student(self, student_id: int) -> None:
        existing_student = await self.repository.get_by_id(student_id)
        if not existing_student:
            logger.warning(f"Student not found for deletion: {student_id}")
            raise StudentNotFoundError()
        
        await self.repository.soft_delete(student_id)
        logger.info(f"Student soft deleted successfully: {student_id}")
    
    async def soft_delete_student(self, student_id: int, deleted_by: str = None) -> None:
        existing_student = await self.repository.get_by_id(student_id)
        if not existing_student:
            logger.warning(f"Student not found for soft deletion: {student_id}")
            raise StudentNotFoundError()
        
        await self.repository.soft_delete(student_id, deleted_by)
        logger.info(f"Student soft deleted successfully: {student_id}")
    
    async def restore_student(self, student_id: int) -> Student:
        existing_student = await self.repository.get_by_id(student_id, include_deleted=True)
        if not existing_student:
            logger.warning(f"Student not found for restore: {student_id}")
            raise StudentNotFoundError()
        
        if not existing_student.deleted_at:
            logger.warning(f"Student is not deleted: {student_id}")
            raise ValidationError("Student is not deleted", "student_id")
        
        restored_student = await self.repository.restore(student_id)
        logger.info(f"Student restored successfully: {student_id}")
        return restored_student
    
    async def get_deleted_students(self, page: int = 1, page_size: int = 10) -> Tuple[List[Student], int]:
        if page < 1:
            raise ValidationError("Page must be greater than 0", "page")
        if page_size < 1 or page_size > 100:
            raise ValidationError("Page size must be between 1 and 100", "page_size")
        
        students, total_count = await self.repository.get_deleted(page, page_size)
        logger.info(f"Retrieved {len(students)} deleted students, page {page}")
        return students, total_count
    
    async def hard_delete_student(self, student_id: int) -> None:
        existing_student = await self.repository.get_by_id(student_id, include_deleted=True)
        if not existing_student:
            logger.warning(f"Student not found for hard deletion: {student_id}")
            raise StudentNotFoundError()
        
        await self.repository.hard_delete(student_id)
        logger.warning(f"Student permanently deleted: {student_id}")
