from employee_management.exceptions import InvalidAgeError, InvalidSalaryError


def validate_age(age):
    try:
        age = int(age)
    except (TypeError, ValueError) as error:
        raise InvalidAgeError("Tuổi phải là số nguyên.") from error

    if age < 18 or age > 65:
        raise InvalidAgeError("Tuổi phải nằm trong khoảng từ 18 đến 65.")
    return age


def validate_salary(salary):
    try:
        salary = float(salary)
    except (TypeError, ValueError) as error:
        raise InvalidSalaryError("Lương phải là số hợp lệ.") from error

    if salary <= 0:
        raise InvalidSalaryError("Lương phải lớn hơn 0.")
    return salary


def validate_email(email):
    email = str(email).strip()
    if "@" not in email or email.startswith("@") or email.endswith("@"):
        raise ValueError("Email không đúng định dạng, vui lòng nhập lại.")
    return email


def validate_performance_score(score):
    try:
        score = float(score)
    except (TypeError, ValueError) as error:
        raise ValueError("Điểm hiệu suất phải là số.") from error

    if score < 0 or score > 10:
        raise ValueError("Điểm hiệu suất phải nằm trong khoảng 0-10.")
    return score
