import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.responses import success_response, handle_custom_exception
from ...core.exceptions import BaseCustomException
from ...schemas.student_schema import (
    StudentCreateSchema, 
    StudentUpdateSchema, 
    StudentResponseSchema,
    StudentListResponseSchema
)
from ...services.student_service import StudentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=dict, status_code=201)
async def create_student(
    student_data: StudentCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"POST /api/v1/students - Creating student: {student_data.email}")
    
    try:
        service = StudentService(db)
        student = await service.create_student(student_data)
        
        return success_response(
            data=StudentResponseSchema.model_validate(student),
            message="Student created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
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
async def get_students(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10
):
    logger.info(f"GET /api/v1/students - Fetching students page {page}")
    
    try:
        service = StudentService(db)
        students, total_count = await service.get_students(page, page_size)
        
        return success_response(
            data=[
                StudentResponseSchema.model_validate(student) 
                for student in students
            ],
            meta={
                "page": page,
                "page_size": page_size,
                "total_records": total_count
            }
        )
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.get("/{student_id}", response_model=dict)
async def get_student(
    student_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"GET /api/v1/students/{student_id} - Fetching student")
    
    try:
        service = StudentService(db)
        student = await service.get_student(student_id)
        
        return success_response(
            data=StudentResponseSchema.model_validate(student),
            message="Student retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching student {student_id}: {str(e)}")
        raise handle_custom_exception(e)


@router.put("/{student_id}", response_model=dict)
async def update_student(
    student_id: int,
    student_data: StudentUpdateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"PUT /api/v1/students/{student_id} - Updating student")
    
    try:
        service = StudentService(db)
        student = await service.update_student(student_id, student_data)
        
        return success_response(
            data=StudentResponseSchema.model_validate(student),
            message="Student updated successfully"
        )
    except Exception as e:
        logger.error(f"Error updating student {student_id}: {str(e)}")
        raise handle_custom_exception(e)


@router.delete("/{student_id}", response_model=dict)
async def delete_student(
    student_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"DELETE /api/v1/students/{student_id} - Soft deleting student")
    
    try:
        service = StudentService(db)
        await service.soft_delete_student(student_id)
        
        return success_response(
            message="Student deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {str(e)}")
        raise handle_custom_exception(e)


@router.post("/{student_id}/restore", response_model=dict)
async def restore_student(
    student_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"POST /api/v1/students/{student_id}/restore - Restoring student")
    
    try:
        service = StudentService(db)
        student = await service.restore_student(student_id)
        
        # Handle validation errors gracefully
        try:
            student_data = StudentResponseSchema.model_validate(student)
        except Exception as validation_error:
            logger.error(f"Validation error when restoring student {student_id}: {str(validation_error)}")
            # Create a manual response if validation fails
            student_data = {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "enrollment_date": student.enrollment_date,
                "is_active": student.is_active,
                "created_at": student.created_at,
                "updated_at": student.updated_at,
                "deleted_at": getattr(student, 'deleted_at', None),
                "deleted_by": getattr(student, 'deleted_by', None)
            }
        
        return success_response(
            data=student_data,
            message="Student restored successfully"
        )
    except Exception as e:
        logger.error(f"Error restoring student {student_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.get("/deleted/list", response_model=dict)
async def get_deleted_students(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10
):
    logger.info(f"GET /api/v1/students/deleted/list - Fetching deleted students page {page}")
    
    try:
        service = StudentService(db)
        students, total_count = await service.get_deleted_students(page, page_size)
        
        return success_response(
            data=[
                StudentResponseSchema.model_validate(student) 
                for student in students
            ],
            meta={
                "page": page,
                "page_size": page_size,
                "total_records": total_count
            },
            message="Deleted students retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching deleted students: {str(e)}")
        raise handle_custom_exception(e)


@router.delete("/{student_id}/hard", response_model=dict)
async def hard_delete_student(
    student_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"DELETE /api/v1/students/{student_id}/hard - Hard deleting student")
    
    try:
        service = StudentService(db)
        await service.hard_delete_student(student_id)
        
        return success_response(
            message="Student permanently deleted"
        )
    except Exception as e:
        logger.error(f"Error hard deleting student {student_id}: {str(e)}")
        raise handle_custom_exception(e)
