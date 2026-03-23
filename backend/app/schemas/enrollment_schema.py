from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EnrollmentCreateSchema(BaseModel):
    course_id: int


class EnrollmentResponseSchema(BaseModel):
    id: int
    student_id: int
    course_id: int
    created_at: datetime
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None

    class Config:
        from_attributes = True


class StudentCourseResponseSchema(BaseModel):
    course_id: int
    course_name: str
    course_code: str
    enrollment_date: datetime
    grade: int = None

    class Config:
        from_attributes = True


class StudentCoursesResponseSchema(BaseModel):
    data: list[StudentCourseResponseSchema]
    meta: dict
