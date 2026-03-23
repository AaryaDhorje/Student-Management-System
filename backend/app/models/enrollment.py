from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from ..core.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(String(255), nullable=True)
    
    student = relationship("Student", backref="enrollments")
    course = relationship("Course", backref="enrollments")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='uq_student_course'),
        Index('idx_enrollments_student_id', 'student_id'),
        Index('idx_enrollments_course_id', 'course_id'),
        Index('idx_enrollments_deleted_at', 'deleted_at'),
    )
    
    def __repr__(self):
        return f"<Enrollment(id={self.id}, student_id={self.student_id}, course_id={self.course_id})>"
