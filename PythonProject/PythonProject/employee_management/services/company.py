from employee_management.exceptions import (
    DuplicateEmployeeError,
    EmployeeException,
    EmployeeNotFoundError,
)
from employee_management.models import Developer, Intern, Manager


class Company:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def _ensure_not_empty(self):
        if not self.employees:
            raise IndexError("Chưa có dữ liệu.")

    def _assert_unique_id(self, employee_id):
        if any(employee.employee_id == employee_id for employee in self.employees):
            raise DuplicateEmployeeError(f"Mã nhân viên đã tồn tại: {employee_id}")

    def generate_employee_id(self, role_name):
        prefixes = {
            "Manager": "MGR",
            "Developer": "DEV",
            "Intern": "INT",
        }
        prefix = prefixes.get(role_name, "EMP")
        max_number = 0
        for employee in self.employees:
            if employee.employee_id.startswith(prefix):
                suffix = employee.employee_id.replace(prefix, "", 1)
                if suffix.isdigit():
                    max_number = max(max_number, int(suffix))
        return f"{prefix}{max_number + 1:03d}"

    def add_employee(self, employee):
        auto_generated = False
        try:
            self._assert_unique_id(employee.employee_id)
        except DuplicateEmployeeError:
            auto_generated = True
            employee.employee_id = self.generate_employee_id(employee.role_name)
        self.employees.append(employee)
        return employee.employee_id, auto_generated

    def get_all_employees(self):
        self._ensure_not_empty()
        return list(self.employees)

    def get_employees_by_role(self, role_name):
        self._ensure_not_empty()
        filtered = [
            employee
            for employee in self.employees
            if employee.role_name.lower() == role_name.lower()
        ]
        if not filtered:
            raise IndexError("Chưa có dữ liệu.")
        return filtered

    def get_employees_sorted_by_performance(self):
        self._ensure_not_empty()
        return sorted(
            self.employees,
            key=lambda employee: employee.performance_score,
            reverse=True,
        )

    def find_employee_by_id(self, employee_id):
        for employee in self.employees:
            if employee.employee_id.lower() == str(employee_id).lower():
                return employee
        raise EmployeeNotFoundError(employee_id)

    def search_by_name(self, keyword):
        self._ensure_not_empty()
        keyword = str(keyword).strip().lower()
        results = [employee for employee in self.employees if keyword in employee.name.lower()]
        if not results:
            raise IndexError("Chưa có dữ liệu.")
        return results

    def search_developers_by_language(self, language):
        self._ensure_not_empty()
        language = str(language).strip().lower()
        results = [
            employee
            for employee in self.employees
            if isinstance(employee, Developer)
            and language in employee.programming_language.lower()
        ]
        if not results:
            raise IndexError("Chưa có dữ liệu.")
        return results

    def remove_employee(self, employee_id):
        employee = self.find_employee_by_id(employee_id)
        self.employees.remove(employee)
        return employee

    def assign_project(self, employee_id, project_name):
        employee = self.find_employee_by_id(employee_id)
        employee.assign_project(project_name)
        return employee

    def remove_project(self, employee_id, project_name):
        employee = self.find_employee_by_id(employee_id)
        employee.remove_project(project_name)
        return employee

    def update_performance(self, employee_id, score):
        employee = self.find_employee_by_id(employee_id)
        employee.update_performance(score)
        return employee

    def get_excellent_employees(self):
        self._ensure_not_empty()
        results = [employee for employee in self.employees if employee.performance_score > 8]
        if not results:
            raise IndexError("Chưa có dữ liệu.")
        return results

    def get_employees_need_improvement(self):
        self._ensure_not_empty()
        results = [employee for employee in self.employees if employee.performance_score < 5]
        if not results:
            raise IndexError("Chưa có dữ liệu.")
        return results

    def increase_salary(self, employee_id, amount):
        employee = self.find_employee_by_id(employee_id)
        employee.increase_base_salary(amount)
        return employee

    def promote_employee(self, employee_id, **kwargs):
        employee = self.find_employee_by_id(employee_id)
        employee_index = self.employees.index(employee)

        if isinstance(employee, Intern):
            promoted_employee = Developer(
                employee_id=employee.employee_id,
                name=employee.name,
                age=employee.age,
                email=employee.email,
                department=kwargs.get("department", employee.department),
                base_salary=kwargs.get("base_salary", employee.base_salary + 2000000),
                programming_language=kwargs.get("programming_language", "Python"),
                overtime_hours=kwargs.get("overtime_hours", 0),
                projects=employee.projects,
                performance_score=employee.performance_score,
            )
        elif isinstance(employee, Developer):
            promoted_employee = Manager(
                employee_id=employee.employee_id,
                name=employee.name,
                age=employee.age,
                email=employee.email,
                department=kwargs.get("department", employee.department),
                base_salary=kwargs.get("base_salary", employee.base_salary + 3000000),
                team_size=kwargs.get("team_size", 0),
                management_allowance=kwargs.get("management_allowance", 5000000),
                projects=employee.projects,
                performance_score=employee.performance_score,
            )
        else:
            raise EmployeeException("Manager đã là cấp cao nhất trong hệ thống hiện tại.")

        self.employees[employee_index] = promoted_employee
        return promoted_employee

    def count_employees_by_role(self):
        self._ensure_not_empty()
        report = {}
        for employee in self.employees:
            report[employee.role_name] = report.get(employee.role_name, 0) + 1
        return report

    def total_salary_by_department(self):
        self._ensure_not_empty()
        report = {}
        for employee in self.employees:
            report[employee.department] = report.get(employee.department, 0) + employee.calculate_salary()
        return report

    def average_projects_per_employee(self):
        self._ensure_not_empty()
        total_projects = sum(len(employee.projects) for employee in self.employees)
        return total_projects / len(self.employees)
