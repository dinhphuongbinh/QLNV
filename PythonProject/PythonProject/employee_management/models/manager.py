from employee_management.models.employee import Employee


class Manager(Employee):
    role_name = "Manager"

    def __init__(
        self,
        employee_id,
        name,
        age,
        email,
        department,
        base_salary,
        team_size,
        management_allowance=5000000,
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
        self.team_size = max(0, int(team_size))
        self.management_allowance = float(management_allowance)

    def calculate_salary(self):
        team_bonus = self.team_size * 300000
        performance_bonus = self.base_salary * (self.performance_score / 20)
        return self.base_salary + self.management_allowance + team_bonus + performance_bonus

    def additional_info(self):
        return {
            "Quy mô đội nhóm": self.team_size,
            "Phụ cấp quản lý": self.management_allowance,
        }
