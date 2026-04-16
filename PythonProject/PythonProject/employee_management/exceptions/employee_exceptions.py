class EmployeeException(Exception):
    """Base exception cho hệ thống nhân viên."""


class EmployeeNotFoundError(EmployeeException):
    """Lỗi không tìm thấy nhân viên."""

    def __init__(self, employee_id):
        self.employee_id = employee_id
        super().__init__(f"Không tìm thấy nhân viên có ID: {employee_id}")


class InvalidSalaryError(EmployeeException):
    """Lỗi lương không hợp lệ."""


class InvalidAgeError(EmployeeException):
    """Lỗi tuổi không hợp lệ (phải 18-65)."""


class ProjectAllocationError(EmployeeException):
    """Lỗi phân công dự án."""


class DuplicateEmployeeError(EmployeeException):
    """Lỗi trùng mã nhân viên."""
