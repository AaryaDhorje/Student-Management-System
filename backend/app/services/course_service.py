import logging
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.course import Course
from ..schemas.course_schema import CourseCreateSchema, CourseUpdateSchema
from ..repositories.course_repository import CourseRepository
from ..core.exceptions import ValidationError

logger = logging.getLogger(__name__)


class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = CourseRepository(db)
    
    async def create_course(self, course_data: CourseCreateSchema) -> Course:
        logger.info(f"Creating course with code: {course_data.course_code}")
        
        existing_course = await self.repository.get_by_code(course_data.course_code)
        if existing_course:
            logger.warning(f"Duplicate course code attempt: {course_data.course_code}")
            raise ValidationError("Course code already exists", "course_code")
        
        course = Course(
            course_name=course_data.course_name,
            course_code=course_data.course_code,
            description=course_data.description
        )
        
        created_course = await self.repository.create(course)
        logger.info(f"Course created successfully: {created_course.id}")
        return created_course
    
    async def get_course(self, course_id: int) -> Course:
        course = await self.repository.get_by_id(course_id)
        if not course:
            logger.warning(f"Course not found: {course_id}")
            raise ValidationError("Course not found", "course_id")
        
        return course
    
    async def get_courses(self, page: int = 1, page_size: int = 10) -> Tuple[List[Course], int]:
        if page < 1:
            raise ValidationError("Page must be greater than 0", "page")
        if page_size < 1 or page_size > 100:
            raise ValidationError("Page size must be between 1 and 100", "page_size")
        
        courses, total_count = await self.repository.get_all(page, page_size)
        logger.info(f"Retrieved {len(courses)} courses, page {page}")
        return courses, total_count
    
    async def update_course(self, course_id: int, course_data: CourseUpdateSchema) -> Course:
        existing_course = await self.repository.get_by_id(course_id)
        if not existing_course:
            logger.warning(f"Course not found for update: {course_id}")
            raise ValidationError("Course not found", "course_id")
        
        if course_data.course_code and course_data.course_code != existing_course.course_code:
            code_exists = await self.repository.get_by_code(course_data.course_code)
            if code_exists:
                logger.warning(f"Duplicate course code attempt during update: {course_data.course_code}")
                raise ValidationError("Course code already exists", "course_code")
        
        update_data = course_data.model_dump(exclude_unset=True)
        updated_course = await self.repository.update(course_id, update_data)
        logger.info(f"Course updated successfully: {course_id}")
        return updated_course
    
    async def delete_course(self, course_id: int) -> None:
        existing_course = await self.repository.get_by_id(course_id)
        if not existing_course:
            logger.warning(f"Course not found for deletion: {course_id}")
            raise ValidationError("Course not found", "course_id")
        
        await self.repository.delete(course_id)
        logger.info(f"Course deleted successfully: {course_id}")
    
    async def soft_delete_course(self, course_id: int, deleted_by: str = None) -> None:
        existing_course = await self.repository.get_by_id(course_id)
        if not existing_course:
            logger.warning(f"Course not found for soft deletion: {course_id}")
            raise ValidationError("Course not found", "course_id")
        
        await self.repository.soft_delete(course_id, deleted_by)
        logger.info(f"Course soft deleted successfully: {course_id}")
    
    async def restore_course(self, course_id: int) -> Course:
        existing_course = await self.repository.get_by_id(course_id, include_deleted=True)
        if not existing_course:
            logger.warning(f"Course not found for restore: {course_id}")
            raise ValidationError("Course not found", "course_id")
        
        if not existing_course.deleted_at:
            logger.warning(f"Course is not deleted: {course_id}")
            raise ValidationError("Course is not deleted", "course_id")
        
        restored_course = await self.repository.restore(course_id)
        logger.info(f"Course restored successfully: {course_id}")
        return restored_course
    
    async def get_deleted_courses(self, page: int = 1, page_size: int = 10) -> Tuple[List[Course], int]:
        if page < 1:
            raise ValidationError("Page must be greater than 0", "page")
        if page_size < 1 or page_size > 100:
            raise ValidationError("Page size must be between 1 and 100", "page_size")
        
        courses, total_count = await self.repository.get_deleted(page, page_size)
        logger.info(f"Retrieved {len(courses)} deleted courses, page {page}")
        return courses, total_count
    
    async def hard_delete_course(self, course_id: int) -> None:
        existing_course = await self.repository.get_by_id(course_id, include_deleted=True)
        if not existing_course:
            logger.warning(f"Course not found for hard deletion: {course_id}")
            raise ValidationError("Course not found", "course_id")
        
        await self.repository.hard_delete(course_id)
        logger.warning(f"Course permanently deleted: {course_id}")
