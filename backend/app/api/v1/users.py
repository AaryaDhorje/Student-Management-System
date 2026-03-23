import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...core.responses import success_response, handle_custom_exception
from ...core.exceptions import BaseCustomException
from ...schemas.user_schema import (
    UserCreateSchema, 
    UserUpdateSchema, 
    UserResponseSchema,
    UserListResponseSchema
)
from ...services.user_service import UserService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=dict, status_code=201)
async def create_user(
    user_data: UserCreateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"POST /api/v1/users - Creating user: {user_data.email}")
    
    try:
        service = UserService(db)
        user = await service.create_user(user_data.dict())
        
        return success_response(
            data=UserResponseSchema.model_validate(user),
            message="User created successfully"
        )
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
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
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10
):
    logger.info(f"GET /api/v1/users - Fetching users page {page}")
    
    try:
        service = UserService(db)
        users, total_count = await service.get_all_users(page, page_size)
        
        return success_response(
            data=[
                UserResponseSchema.model_validate(user) 
                for user in users
            ],
            meta={
                "page": page,
                "page_size": page_size,
                "total_records": total_count
            }
        )
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"GET /api/v1/users/{user_id} - Fetching user")
    
    try:
        service = UserService(db)
        user = await service.get_user_by_id(user_id)
        
        return success_response(
            data=UserResponseSchema.model_validate(user),
            message="User retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: int,
    user_data: UserUpdateSchema,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"PUT /api/v1/users/{user_id} - Updating user")
    
    try:
        service = UserService(db)
        user = await service.update_user(user_id, user_data.dict(exclude_unset=True))
        
        return success_response(
            data=UserResponseSchema.model_validate(user),
            message="User updated successfully"
        )
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"DELETE /api/v1/users/{user_id} - Soft deleting user")
    
    try:
        service = UserService(db)
        await service.soft_delete_user(user_id)
        
        return success_response(
            message="User deleted successfully"
        )
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.post("/{user_id}/restore", response_model=dict)
async def restore_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"POST /api/v1/users/{user_id}/restore - Restoring user")
    
    try:
        service = UserService(db)
        user = await service.restore_user(user_id)
        
        # Handle validation errors gracefully
        try:
            user_data = UserResponseSchema.model_validate(user)
        except Exception as validation_error:
            logger.error(f"Validation error when restoring user {user_id}: {str(validation_error)}")
            # Create a manual response if validation fails
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "is_active": user.is_active,
                "phone": user.phone,
                "department": user.department,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "deleted_at": getattr(user, 'deleted_at', None),
                "deleted_by": getattr(user, 'deleted_by', None)
            }
        
        return success_response(
            data=user_data,
            message="User restored successfully"
        )
    except Exception as e:
        logger.error(f"Error restoring user {user_id}: {str(e)}")
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
async def get_deleted_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10
):
    logger.info(f"GET /api/v1/users/deleted/list - Fetching deleted users page {page}")
    
    try:
        service = UserService(db)
        users, total_count = await service.get_deleted_users(page, page_size)
        
        return success_response(
            data=users,
            meta={
                "page": page,
                "page_size": page_size,
                "total_records": total_count
            },
            message="Deleted users retrieved successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching deleted users: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )


@router.delete("/{user_id}/hard", response_model=dict)
async def hard_delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    logger.info(f"DELETE /api/v1/users/{user_id}/hard - Hard deleting user")
    
    try:
        service = UserService(db)
        await service.hard_delete_user(user_id)
        
        return success_response(
            message="User permanently deleted"
        )
    except Exception as e:
        logger.error(f"Error hard deleting user {user_id}: {str(e)}")
        if hasattr(e, 'code') and isinstance(e, BaseCustomException):
            raise handle_custom_exception(e)
        else:
            from ...core.responses import error_response
            raise error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred",
                status_code=500
            )
