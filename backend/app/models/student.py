from datetime import datetime, date
from sqlalchemy import Column, String, Boolean, DateTime, Date, Integer, Index
from ..core.database import Base


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    enrollment_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String(100), nullable=True)
    
    __table_args__ = (
        Index('idx_students_email', 'email'),
        Index('idx_students_deleted_at', 'deleted_at'),
    )
    
    def __repr__(self):
        return f"<Student(id={self.id}, email={self.email}, is_active={self.is_active}, deleted_at={self.deleted_at})>"
    
    def soft_delete(self, deleted_by: str = None):
        """Mark the student as deleted"""
        self.deleted_at = datetime.utcnow()
        self.deleted_by = deleted_by
        self.is_active = False
    
    def restore(self):
        """Restore the soft-deleted student"""
        self.deleted_at = None
        self.deleted_by = None
        self.is_active = True
