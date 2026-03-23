from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class StudentBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    enrollment_date: date


class StudentCreateSchema(StudentBaseSchema):
    pass


class StudentUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    enrollment_date: Optional[date] = None


class StudentResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    enrollment_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[str] = None

    class Config:
        from_attributes = True


class StudentListResponseSchema(BaseModel):
    data: list[StudentResponseSchema]
    meta: dict
