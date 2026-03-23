import logging
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.enrollment import Enrollment
from ..schemas.enrollment_schema import EnrollmentCreateSchema
from ..repositories.enrollment_repository import EnrollmentRepository
from ..repositories.student_repository import StudentRepository
from ..repositories.course_repository import CourseRepository
from ..core.exceptions import (
    StudentNotFoundError, 
    CourseNotFoundError, 
    AlreadyEnrolledError,
    ValidationError
)

logger = logging.getLogger(__name__)


class EnrollmentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.enrollment_repository = EnrollmentRepository(db)
        self.student_repository = StudentRepository(db)
        self.course_repository = CourseRepository(db)
    
    async def enroll_student(self, student_id: int, enrollment_data: EnrollmentCreateSchema) -> Enrollment:
        logger.info(f"Enrolling student {student_id} in course {enrollment_data.course_id}")
        
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            logger.warning(f"Student not found for enrollment: {student_id}")
            raise StudentNotFoundError()
        
        course = await self.course_repository.get_by_id(enrollment_data.course_id)
        if not course:
            logger.warning(f"Course not found for enrollment: {enrollment_data.course_id}")
            raise CourseNotFoundError()
        
        existing_enrollment = await self.enrollment_repository.exists(
            student_id, enrollment_data.course_id
        )
        if existing_enrollment:
            logger.warning(f"Student {student_id} already enrolled in course {enrollment_data.course_id}")
            raise AlreadyEnrolledError()
        
        enrollment = Enrollment(
            student_id=student_id,
            course_id=enrollment_data.course_id
        )
        
        created_enrollment = await self.enrollment_repository.create(enrollment)
        logger.info(f"Student {student_id} enrolled successfully in course {enrollment_data.course_id}")
        return created_enrollment
    
    async def get_student_courses(self, student_id: int) -> List[Dict[str, Any]]:
        logger.info(f"Getting courses for student {student_id}")
        
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            logger.warning(f"Student not found: {student_id}")
            raise StudentNotFoundError()
        
        courses = await self.enrollment_repository.get_student_courses(student_id)
        logger.info(f"Retrieved {len(courses)} courses for student {student_id}")
        return courses
    
    async def get_course_students(self, course_id: int):
        course = await self.course_repository.get_by_id(course_id)
        if not course:
            logger.warning(f"Course not found when fetching students: {course_id}")
            raise CourseNotFoundError()
        
        students = await self.enrollment_repository.get_course_students(course_id)
        logger.info(f"Retrieved {len(students)} students for course {course_id}")
        return students
    
    async def remove_enrollment(self, student_id: int, course_id: int) -> None:
        logger.info(f"Removing enrollment for student {student_id} in course {course_id}")
        
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            logger.warning(f"Student not found for enrollment removal: {student_id}")
            raise StudentNotFoundError()
        
        course = await self.course_repository.get_by_id(course_id)
        if not course:
            logger.warning(f"Course not found for enrollment removal: {course_id}")
            raise CourseNotFoundError()
        
        enrollment_exists = await self.enrollment_repository.exists(student_id, course_id)
        if not enrollment_exists:
            logger.warning(f"Enrollment not found for student {student_id}, course {course_id}")
            raise ValidationError("Enrollment not found", "enrollment")
        
        await self.enrollment_repository.delete_by_student_course(student_id, course_id)
        logger.info(f"Enrollment removed successfully for student {student_id}, course {course_id}")
    
    async def soft_remove_enrollment(self, student_id: int, course_id: int, deleted_by: str = None) -> None:
        logger.info(f"Soft removing enrollment for student {student_id} in course {course_id}")
        
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            logger.warning(f"Student not found for enrollment removal: {student_id}")
            raise StudentNotFoundError()
        
        course = await self.course_repository.get_by_id(course_id)
        if not course:
            logger.warning(f"Course not found for enrollment removal: {course_id}")
            raise CourseNotFoundError()
        
        enrollment_exists = await self.enrollment_repository.exists(student_id, course_id)
        if not enrollment_exists:
            logger.warning(f"Enrollment not found for student {student_id}, course {course_id}")
            raise ValidationError("Enrollment not found", "enrollment")
        
        await self.enrollment_repository.soft_delete_by_student_course(student_id, course_id, deleted_by)
        logger.info(f"Enrollment soft removed successfully for student {student_id}, course {course_id}")
    
    async def restore_enrollment(self, student_id: int, course_id: int) -> Enrollment:
        logger.info(f"Restoring enrollment for student {student_id} in course {course_id}")
        
        student = await self.student_repository.get_by_id(student_id)
        if not student:
            logger.warning(f"Student not found for enrollment restore: {student_id}")
            raise StudentNotFoundError()
        
        course = await self.course_repository.get_by_id(course_id)
        if not course:
            logger.warning(f"Course not found for enrollment restore: {course_id}")
            raise CourseNotFoundError()
        
        restored_enrollment = await self.enrollment_repository.restore_by_student_course(student_id, course_id)
        if not restored_enrollment:
            logger.warning(f"No deleted enrollment found for student {student_id}, course {course_id}")
            raise ValidationError("No deleted enrollment found to restore", "enrollment")
        
        logger.info(f"Enrollment restored successfully for student {student_id}, course {course_id}")
        
        # Return the enrollment object
        enrollments = await self.enrollment_repository.get_student_courses(student_id, include_deleted=True)
        for enrollment in enrollments:
            if enrollment['course_id'] == course_id and not enrollment.get('deleted_at'):
                return Enrollment(
                    id=enrollment.get('id'),
                    student_id=student_id,
                    course_id=course_id
                )
        
        raise ValidationError("Failed to restore enrollment", "enrollment")
    
    async def get_deleted_enrollments(self, page: int = 1, page_size: int = 10) -> List[Dict[str, Any]]:
        logger.info(f"Getting deleted enrollments page {page}")
        
        if page < 1:
            raise ValidationError("Page must be greater than 0", "page")
        if page_size < 1 or page_size > 100:
            raise ValidationError("Page size must be between 1 and 100", "page_size")
        
        enrollments = await self.enrollment_repository.get_deleted(page, page_size)
        logger.info(f"Retrieved {len(enrollments)} deleted enrollments")
        return enrollments
    
    async def hard_remove_enrollment(self, student_id: int, course_id: int) -> None:
        logger.warning(f"Hard removing enrollment for student {student_id} in course {course_id}")
        
        student = await self.student_repository.get_by_id(student_id, include_deleted=True)
        if not student:
            logger.warning(f"Student not found for enrollment removal: {student_id}")
            raise StudentNotFoundError()
        
        course = await self.course_repository.get_by_id(course_id, include_deleted=True)
        if not course:
            logger.warning(f"Course not found for enrollment removal: {course_id}")
            raise CourseNotFoundError()
        
        await self.enrollment_repository.hard_delete_by_student_course(student_id, course_id)
        logger.warning(f"Enrollment permanently removed for student {student_id}, course {course_id}")
