from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Index, Boolean
from ..core.database import Base


class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String(255), nullable=True)
    
    __table_args__ = (
        Index('idx_courses_course_code', 'course_code'),
        Index('idx_courses_deleted_at', 'deleted_at'),
    )
    
    def __repr__(self):
        return f"<Course(id={self.id}, course_code={self.course_code}, name={self.course_name})>"
