from typing import Any, Dict, Optional
from fastapi import HTTPException
from .exceptions import BaseCustomException


def success_response(
    data: Any = None,
    message: str = "operation successful",
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    response = {
        "success": True,
        "data": data,
        "message": message
    }
    
    if meta:
        response["meta"] = meta
    
    return response


def error_response(
    code: str,
    message: str,
    field: Optional[str] = None,
    status_code: int = 400
) -> HTTPException:
    error_detail = {
        "code": code,
        "message": message,
        "field": field
    }
    
    response = {
        "success": False,
        "error": error_detail
    }
    
    return HTTPException(
        status_code=status_code,
        detail=response
    )


def handle_custom_exception(exc: BaseCustomException) -> HTTPException:
    status_code_map = {
        "VALIDATION_ERROR": 422,
        "DUPLICATE_EMAIL": 409,
        "STUDENT_NOT_FOUND": 404,
        "COURSE_NOT_FOUND": 404,
        "ALREADY_ENROLLED": 409,
        "ENROLLMENT_NOT_FOUND": 404
    }
    
    status_code = status_code_map.get(exc.code, 400)
    
    return error_response(
        code=exc.code,
        message=exc.message,
        field=exc.field,
        status_code=status_code
    )
