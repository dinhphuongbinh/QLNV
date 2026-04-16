def calculate_total_payroll(employees):
    if not employees:
        raise IndexError("Chưa có dữ liệu.")
    return sum(employee.calculate_salary() for employee in employees)


def get_top_paid_employees(employees, limit=3):
    if not employees:
        raise IndexError("Chưa có dữ liệu.")
    return sorted(employees, key=lambda employee: employee.calculate_salary(), reverse=True)[:limit]


def get_salary_statistics(employees):
    if not employees:
        raise IndexError("Chưa có dữ liệu.")

    total = calculate_total_payroll(employees)
    average = total / len(employees)
    highest = max(employees, key=lambda employee: employee.calculate_salary())
    lowest = min(employees, key=lambda employee: employee.calculate_salary())
    return {
        "total": total,
        "average": average,
        "highest": highest,
        "lowest": lowest,
    }
