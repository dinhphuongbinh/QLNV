from abc import ABC, abstractmethod

from employee_management.exceptions import InvalidSalaryError, ProjectAllocationError
from employee_management.utils.validators import (
    validate_age,
    validate_email,
    validate_performance_score,
    validate_salary,
)


class Employee(ABC):
    role_name = "Employee"

    def __init__(
        self,
        employee_id,
        name,
        age,
        email,
        department,
        base_salary,
        projects=None,
        performance_score=0,
    ):
        self.employee_id = str(employee_id).strip()
        self.name = str(name).strip()
        self.age = validate_age(age)
        self.email = validate_email(email)
        self.department = str(department).strip() or "Chưa phân phòng"
        self.base_salary = validate_salary(base_salary)
        self.projects = list(projects or [])
        self.performance_score = validate_performance_score(performance_score)

        if len(self.projects) > 5:
            raise ProjectAllocationError("Một nhân viên chỉ được tham gia tối đa 5 dự án.")

    @abstractmethod
    def calculate_salary(self):
        """Tính lương theo từng chức vụ."""

    def assign_project(self, project_name):
        project_name = str(project_name).strip()
        if not project_name:
            raise ProjectAllocationError("Tên dự án không được để trống.")
        if len(self.projects) >= 5:
            raise ProjectAllocationError("Nhân viên đã đạt giới hạn 5 dự án.")
        if project_name in self.projects:
            raise ProjectAllocationError("Nhân viên đã có trong dự án này.")
        self.projects.append(project_name)

    def remove_project(self, project_name):
        project_name = str(project_name).strip()
        if project_name not in self.projects:
            raise ProjectAllocationError("Nhân viên không thuộc dự án này.")
        self.projects.remove(project_name)

    def update_performance(self, score):
        self.performance_score = validate_performance_score(score)

    def increase_base_salary(self, amount):
        try:
            amount = float(amount)
        except (TypeError, ValueError) as error:
            raise InvalidSalaryError("Mức tăng lương phải là số.") from error

        if amount <= 0:
            raise InvalidSalaryError("Mức tăng lương phải lớn hơn 0.")
        self.base_salary = validate_salary(self.base_salary + amount)

    def performance_rank(self):
        if self.performance_score >= 8:
            return "Xuất sắc"
        if self.performance_score >= 6.5:
            return "Tốt"
        if self.performance_score >= 5:
            return "Đạt yêu cầu"
        return "Cần cải thiện"

    def additional_info(self):
        return {}
