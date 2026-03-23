import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.responses import success_response, handle_custom_exception
from ...core.exceptions import BaseCustomException
from ...schemas.course_schema import (
    CourseCreateSchema, 
    CourseUpdateSchema, 
    CourseResponseSchema
)
from ...services.course_service import CourseService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=dict, status_code=201)
async def create_course(
    course_data: CourseCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"POST /api/v1/courses - Creating course: {course_data.course_code}")
    
    try:
        service = CourseService(db)
        course = await service.create_course(course_data)
        
        return success_response(
            data=CourseResponseSchema.model_validate(course),
            message="Course created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating course: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.get("/", response_model=dict)
async def get_courses(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10
):
    logger.info(f"GET /api/v1/courses - Fetching courses page {page}")
    
    try:
        service = CourseService(db)
        courses, total_count = await service.get_courses(page, page_size)
        
        return success_response(
            data=[
                CourseResponseSchema.model_validate(course) 
                for course in courses
            ],
            meta={
                "page": page,
                "page_size": page_size,
                "total_records": total_count
            }
        )
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.get("/{course_id}", response_model=dict)
async def get_course(
    course_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"GET /api/v1/courses/{course_id} - Fetching course")
    
    try:
        service = CourseService(db)
        course = await service.get_course(course_id)
        
        return success_response(
            data=CourseResponseSchema.model_validate(course),
            message="Course retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching course {course_id}: {str(e)}")
        raise handle_custom_exception(e)


@router.put("/{course_id}", response_model=dict)
async def update_course(
    course_id: int,
    course_data: CourseUpdateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"PUT /api/v1/courses/{course_id} - Updating course")
    
    try:
        service = CourseService(db)
        course = await service.update_course(course_id, course_data)
        
        return success_response(
            data=CourseResponseSchema.model_validate(course),
            message="Course updated successfully"
        )
    except Exception as e:
        logger.error(f"Error updating course {course_id}: {str(e)}")
        raise handle_custom_exception(e)


@router.delete("/{course_id}", response_model=dict)
async def delete_course(
    course_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"DELETE /api/v1/courses/{course_id} - Soft deleting course")
    
    try:
        service = CourseService(db)
        await service.soft_delete_course(course_id)
        
        return success_response(
            message="Course deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting course {course_id}: {str(e)}")
        raise handle_custom_exception(e)


@router.post("/{course_id}/restore", response_model=dict)
async def restore_course(
    course_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"POST /api/v1/courses/{course_id}/restore - Restoring course")
    
    try:
        service = CourseService(db)
        course = await service.restore_course(course_id)
        
        return success_response(
            data=CourseResponseSchema.model_validate(course),
            message="Course restored successfully"
        )
    except Exception as e:
        logger.error(f"Error restoring course {course_id}: {str(e)}")
        raise handle_custom_exception(e)


@router.get("/deleted/list", response_model=dict)
async def get_deleted_courses(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10
):
    logger.info(f"GET /api/v1/courses/deleted/list - Fetching deleted courses page {page}")
    
    try:
        service = CourseService(db)
        courses, total_count = await service.get_deleted_courses(page, page_size)
        
        return success_response(
            data=[
                CourseResponseSchema.model_validate(course) 
                for course in courses
            ],
            meta={
                "page": page,
                "page_size": page_size,
                "total_records": total_count
            },
            message="Deleted courses retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching deleted courses: {str(e)}")
        raise handle_custom_exception(e)


@router.delete("/{course_id}/hard", response_model=dict)
async def hard_delete_course(
    course_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"DELETE /api/v1/courses/{course_id}/hard - Hard deleting course")
    
    try:
        service = CourseService(db)
        await service.hard_delete_course(course_id)
        
        return success_response(
            message="Course permanently deleted"
        )
    except Exception as e:
        logger.error(f"Error hard deleting course {course_id}: {str(e)}")
        raise handle_custom_exception(e)
