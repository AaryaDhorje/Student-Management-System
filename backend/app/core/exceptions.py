from typing import Optional


class BaseCustomException(Exception):
    def __init__(self, code: str, message: str, field: Optional[str] = None):
        self.code = code
        self.message = message
        self.field = field
        super().__init__(self.message)


class ValidationError(BaseCustomException):
    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__("VALIDATION_ERROR", message, field)


class DuplicateEmailError(BaseCustomException):
    def __init__(self):
        super().__init__("DUPLICATE_EMAIL", "Student email already exists")


class StudentNotFoundError(BaseCustomException):
    def __init__(self):
        super().__init__("STUDENT_NOT_FOUND", "Provided UUID does not match any record")


class CourseNotFoundError(BaseCustomException):
    def __init__(self):
        super().__init__("COURSE_NOT_FOUND", "Provided course UUID does not match any record")


class AlreadyEnrolledError(BaseCustomException):
    def __init__(self):
        super().__init__("ALREADY_ENROLLED", "Student is already enrolled in that course")


class EnrollmentNotFoundError(BaseCustomException):
    def __init__(self):
        super().__init__("ENROLLMENT_NOT_FOUND", "Enrollment record not found")
