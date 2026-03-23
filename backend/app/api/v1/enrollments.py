import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.responses import success_response, handle_custom_exception
from ...core.exceptions import BaseCustomException
from ...schemas.enrollment_schema import (
    EnrollmentCreateSchema,
    StudentCourseResponseSchema,
    StudentCoursesResponseSchema
)
from ...services.enrollment_service import EnrollmentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["enrollments"])


@router.post("/{student_id}/courses", response_model=dict, status_code=201)
async def enroll_student(
    student_id: int,
    enrollment_data: EnrollmentCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"POST /api/v1/students/{student_id}/courses - Enrolling student")
    
    try:
        service = EnrollmentService(db)
        enrollment = await service.enroll_student(student_id, enrollment_data)
        
        return success_response(
            data={
                "enrollment_id": enrollment.id,
                "student_id": enrollment.student_id,
                "course_id": enrollment.course_id
            },
            message="Student enrolled successfully"
        )
    except Exception as e:
        logger.error(f"Error enrolling student {student_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.get("/{student_id}/courses", response_model=dict)
async def get_student_courses(
    student_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"GET /api/v1/students/{student_id}/courses - Fetching student courses")
    
    try:
        service = EnrollmentService(db)
        courses = await service.get_student_courses(student_id)
        
        formatted_courses = []
        for course in courses:
            formatted_course = {
                "course_id": course["course_id"],
                "course_name": course["course_name"],
                "course_code": course["course_code"],
                "enrollment_date": course["enrollment_date"].isoformat(),
                "grade": None
            }
            formatted_courses.append(formatted_course)
        
        return success_response(
            data=formatted_courses,
            message="Student courses retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching courses for student {student_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.delete("/{student_id}/courses/{course_id}", response_model=dict)
async def remove_enrollment(
    student_id: int,
    course_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"DELETE /api/v1/students/{student_id}/courses/{course_id} - Soft removing enrollment")
    
    try:
        service = EnrollmentService(db)
        await service.soft_remove_enrollment(student_id, course_id)
        
        return success_response(
            message="Enrollment removed successfully"
        )
    except Exception as e:
        logger.error(f"Error removing enrollment for student {student_id}, course {course_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.post("/{student_id}/courses/{course_id}/restore", response_model=dict)
async def restore_enrollment(
    student_id: int,
    course_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"POST /api/v1/students/{student_id}/courses/{course_id}/restore - Restoring enrollment")
    
    try:
        service = EnrollmentService(db)
        enrollment = await service.restore_enrollment(student_id, course_id)
        
        return success_response(
            data={
                "enrollment_id": enrollment.id,
                "student_id": enrollment.student_id,
                "course_id": enrollment.course_id
            },
            message="Enrollment restored successfully"
        )
    except Exception as e:
        logger.error(f"Error restoring enrollment for student {student_id}, course {course_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.get("/enrollments/deleted/list", response_model=dict)
async def get_deleted_enrollments(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10
):
    logger.info(f"GET /api/v1/students/enrollments/deleted/list - Fetching deleted enrollments page {page}")
    
    try:
        service = EnrollmentService(db)
        enrollments = await service.get_deleted_enrollments(page, page_size)
        
        return success_response(
            data=enrollments,
            message="Deleted enrollments retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching deleted enrollments: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.delete("/{student_id}/courses/{course_id}/hard", response_model=dict)
async def hard_remove_enrollment(
    student_id: int,
    course_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"DELETE /api/v1/students/{student_id}/courses/{course_id}/hard - Hard removing enrollment")
    
    try:
        service = EnrollmentService(db)
        await service.hard_remove_enrollment(student_id, course_id)
        
        return success_response(
            message="Enrollment permanently removed"
        )
    except Exception as e:
        logger.error(f"Error hard removing enrollment for student {student_id}, course {course_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )
