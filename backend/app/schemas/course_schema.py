from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CourseBaseSchema(BaseModel):
    course_name: str
    course_code: str
    description: Optional[str] = None


class CourseCreateSchema(CourseBaseSchema):
    pass


class CourseUpdateSchema(BaseModel):
    course_name: Optional[str] = None
    course_code: Optional[str] = None
    description: Optional[str] = None


class CourseResponseSchema(BaseModel):
    id: int
    course_name: str
    course_code: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None

    class Config:
        from_attributes = True


class CourseListResponseSchema(BaseModel):
    data: list[CourseResponseSchema]
    meta: dict
