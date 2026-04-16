def format_currency(amount):
    return f"{amount:,.0f} VND"


def _format_table(headers, rows):
    if not rows:
        return "Chưa có dữ liệu."

    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    separator = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    lines = [separator]
    header_line = "| " + " | ".join(
        str(value).ljust(widths[index]) for index, value in enumerate(headers)
    ) + " |"
    lines.append(header_line)
    lines.append(separator)

    for row in rows:
        row_line = "| " + " | ".join(
            str(value).ljust(widths[index]) for index, value in enumerate(row)
        ) + " |"
        lines.append(row_line)
    lines.append(separator)
    return "\n".join(lines)


def format_employee_table(employees):
    rows = []
    for employee in employees:
        rows.append(
            [
                employee.employee_id,
                employee.name,
                employee.role_name,
                employee.department,
                employee.age,
                employee.performance_score,
                len(employee.projects),
                format_currency(employee.calculate_salary()),
            ]
        )

    headers = [
        "ID",
        "Họ tên",
        "Chức vụ",
        "Phòng ban",
        "Tuổi",
        "Hiệu suất",
        "Số dự án",
        "Lương",
    ]
    return _format_table(headers, rows)


def format_employee_detail(employee):
    detail_lines = [
        f"ID: {employee.employee_id}",
        f"Họ tên: {employee.name}",
        f"Chức vụ: {employee.role_name}",
        f"Phòng ban: {employee.department}",
        f"Tuổi: {employee.age}",
        f"Email: {employee.email}",
        f"Lương cơ bản: {format_currency(employee.base_salary)}",
        f"Điểm hiệu suất: {employee.performance_score}",
        f"Dự án: {', '.join(employee.projects) if employee.projects else 'Chưa có'}",
    ]

    for key, value in employee.additional_info().items():
        if isinstance(value, float):
            if "lương" in key.lower() or "phụ cấp" in key.lower():
                detail_lines.append(f"{key}: {format_currency(value)}")
            else:
                detail_lines.append(f"{key}: {value}")
        else:
            detail_lines.append(f"{key}: {value}")

    detail_lines.append(f"Tổng lương thực nhận: {format_currency(employee.calculate_salary())}")
    return "\n".join(detail_lines)


def format_projects(employee):
    if not employee.projects:
        return f"Nhân viên {employee.name} chưa được phân công dự án nào."
    projects = "\n".join(f"- {project}" for project in employee.projects)
    return f"Danh sách dự án của {employee.name} ({employee.employee_id}):\n{projects}"


def format_report_block(title, mapping):
    lines = [title]
    for key, value in mapping.items():
        if isinstance(value, (int, float)) and "lương" in title.lower():
            lines.append(f"- {key}: {format_currency(value)}")
        else:
            lines.append(f"- {key}: {value}")
    return "\n".join(lines)
