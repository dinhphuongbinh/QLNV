from employee_management.models.employee import Employee


class Intern(Employee):
    role_name = "Intern"

    def __init__(
        self,
        employee_id,
        name,
        age,
        email,
        department,
        base_salary,
        mentor_name,
        support_allowance=1000000,
        projects=None,
        performance_score=0,
    ):
        super().__init__(
            employee_id=employee_id,
            name=name,
            age=age,
            email=email,
            department=department,
            base_salary=base_salary,
            projects=projects,
            performance_score=performance_score,
        )
        self.mentor_name = str(mentor_name).strip() or "Chưa cập nhật"
        self.support_allowance = float(support_allowance)

    def calculate_salary(self):
        performance_bonus = self.base_salary * (self.performance_score / 40)
        return self.base_salary + self.support_allowance + performance_bonus

    def additional_info(self):
        return {
            "Người hướng dẫn": self.mentor_name,
            "Phụ cấp thực tập": self.support_allowance,
        }
