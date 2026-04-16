from employee_management.models.employee import Employee


class Developer(Employee):
    role_name = "Developer"

    def __init__(
        self,
        employee_id,
        name,
        age,
        email,
        department,
        base_salary,
        programming_language,
        overtime_hours=0,
        overtime_rate=150000,
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
        self.programming_language = str(programming_language).strip() or "N/A"
        self.overtime_hours = max(0, float(overtime_hours))
        self.overtime_rate = float(overtime_rate)

    def calculate_salary(self):
        overtime_pay = self.overtime_hours * self.overtime_rate
        performance_bonus = self.base_salary * (self.performance_score / 25)
        return self.base_salary + overtime_pay + performance_bonus

    def additional_info(self):
        return {
            "Ngôn ngữ lập trình": self.programming_language,
            "Giờ OT": self.overtime_hours,
            "Đơn giá OT": self.overtime_rate,
        }
