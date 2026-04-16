import sys

from employee_management.exceptions import (
    EmployeeException,
    EmployeeNotFoundError,
    InvalidAgeError,
    InvalidSalaryError,
    ProjectAllocationError,
)
from employee_management.models import Developer, Intern, Manager
from employee_management.services import (
    Company,
    calculate_total_payroll,
    get_top_paid_employees,
)
from employee_management.utils import (
    format_currency,
    format_employee_detail,
    format_employee_table,
    format_projects,
    format_report_block,
    validate_age,
    validate_email,
    validate_performance_score,
    validate_salary,
)


for stream_name in ("stdin", "stdout", "stderr"):
    stream = getattr(sys, stream_name, None)
    if stream and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")


def print_header(title):
    print("\n" + "=" * 72)
    print(title.center(72))
    print("=" * 72)


def read_input(message):
    return input(message).replace("\ufeff", "").strip()


def pause():
    try:
        input("\nNhấn Enter để tiếp tục...")
    except EOFError:
        pass


def prompt_non_empty(message):
    while True:
        value = read_input(message)
        if value:
            return value
        print("Dữ liệu không được để trống. Vui lòng nhập lại.")


def prompt_age(message="Tuổi: "):
    while True:
        try:
            return validate_age(read_input(message))
        except InvalidAgeError as error:
            print(error)


def prompt_salary(message="Lương cơ bản: "):
    while True:
        try:
            return validate_salary(read_input(message))
        except InvalidSalaryError as error:
            print(error)


def prompt_email(message="Email: "):
    while True:
        try:
            return validate_email(read_input(message))
        except ValueError as error:
            print(error)


def prompt_score(message="Điểm hiệu suất (0-10): ", default=None):
    while True:
        raw_value = read_input(message)
        if raw_value == "" and default is not None:
            return default
        try:
            return validate_performance_score(raw_value)
        except ValueError as error:
            print(error)


def prompt_non_negative_int(message, default=0):
    while True:
        raw_value = read_input(message)
        if raw_value == "":
            return default
        try:
            value = int(raw_value)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Vui lòng nhập số nguyên không âm.")


def prompt_non_negative_float(message, default=0):
    while True:
        raw_value = read_input(message)
        if raw_value == "":
            return default
        try:
            value = float(raw_value)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Vui lòng nhập số không âm.")


def prompt_employee_id(company, role_name):
    raw_value = read_input("Mã nhân viên (Enter để tự sinh): ")
    if raw_value:
        return raw_value
    return company.generate_employee_id(role_name)


def prompt_common_info(company, role_name):
    employee_id = prompt_employee_id(company, role_name)
    name = prompt_non_empty("Họ tên: ")
    age = prompt_age()
    email = prompt_email()
    department = prompt_non_empty("Phòng ban: ")
    base_salary = prompt_salary()
    performance_score = prompt_score("Điểm hiệu suất ban đầu (0-10, Enter = 0): ", default=0)
    return {
        "employee_id": employee_id,
        "name": name,
        "age": age,
        "email": email,
        "department": department,
        "base_salary": base_salary,
        "performance_score": performance_score,
    }


def add_manager(company):
    print_header("THÊM MANAGER")
    common_info = prompt_common_info(company, "Manager")
    team_size = prompt_non_negative_int("Quy mô đội nhóm: ")
    allowance = prompt_non_negative_float("Phụ cấp quản lý (Enter = 5000000): ", default=5000000)
    employee = Manager(
        **common_info,
        team_size=team_size,
        management_allowance=allowance,
    )
    employee_id, auto_generated = company.add_employee(employee)
    print(f"Đã thêm Manager thành công với ID: {employee_id}")
    if auto_generated:
        print("Mã nhân viên bị trùng, hệ thống đã tự sinh mã mới.")


def add_developer(company):
    print_header("THÊM DEVELOPER")
    common_info = prompt_common_info(company, "Developer")
    programming_language = prompt_non_empty("Ngôn ngữ lập trình chính: ")
    overtime_hours = prompt_non_negative_float("Số giờ OT (Enter = 0): ", default=0)
    employee = Developer(
        **common_info,
        programming_language=programming_language,
        overtime_hours=overtime_hours,
    )
    employee_id, auto_generated = company.add_employee(employee)
    print(f"Đã thêm Developer thành công với ID: {employee_id}")
    if auto_generated:
        print("Mã nhân viên bị trùng, hệ thống đã tự sinh mã mới.")


def add_intern(company):
    print_header("THÊM INTERN")
    common_info = prompt_common_info(company, "Intern")
    mentor_name = prompt_non_empty("Tên người hướng dẫn: ")
    support_allowance = prompt_non_negative_float("Phụ cấp thực tập (Enter = 1000000): ", default=1000000)
    employee = Intern(
        **common_info,
        mentor_name=mentor_name,
        support_allowance=support_allowance,
    )
    employee_id, auto_generated = company.add_employee(employee)
    print(f"Đã thêm Intern thành công với ID: {employee_id}")
    if auto_generated:
        print("Mã nhân viên bị trùng, hệ thống đã tự sinh mã mới.")


def menu_add_employee(company):
    print_header("1. THÊM NHÂN VIÊN MỚI")
    print("a. Thêm Manager")
    print("b. Thêm Developer")
    print("c. Thêm Intern")
    choice = read_input("Chọn chức năng: ").lower()
    actions = {
        "a": add_manager,
        "b": add_developer,
        "c": add_intern,
    }
    action = actions.get(choice)
    if not action:
        print("Lựa chọn không hợp lệ.")
        return
    action(company)


def menu_show_employees(company):
    print_header("2. HIỂN THỊ DANH SÁCH NHÂN VIÊN")
    print("a. Tất cả nhân viên")
    print("b. Theo loại (Manager/Developer/Intern)")
    print("c. Theo hiệu suất (từ cao đến thấp)")
    choice = read_input("Chọn chức năng: ").lower()

    try:
        if choice == "a":
            employees = company.get_all_employees()
        elif choice == "b":
            role_name = prompt_non_empty("Nhập loại nhân viên: ")
            employees = company.get_employees_by_role(role_name)
        elif choice == "c":
            employees = company.get_employees_sorted_by_performance()
        else:
            print("Lựa chọn không hợp lệ.")
            return

        print(format_employee_table(employees))
    except IndexError:
        print("Chưa có dữ liệu.")


def menu_search_employee(company):
    print_header("3. TÌM KIẾM NHÂN VIÊN")
    print("a. Theo ID")
    print("b. Theo tên")
    print("c. Theo ngôn ngữ lập trình (cho Developer)")
    choice = read_input("Chọn chức năng: ").lower()

    try:
        if choice == "a":
            employee = company.find_employee_by_id(prompt_non_empty("Nhập ID nhân viên: "))
            print(format_employee_detail(employee))
        elif choice == "b":
            employees = company.search_by_name(prompt_non_empty("Nhập tên cần tìm: "))
            print(format_employee_table(employees))
        elif choice == "c":
            employees = company.search_developers_by_language(prompt_non_empty("Nhập ngôn ngữ: "))
            print(format_employee_table(employees))
        else:
            print("Lựa chọn không hợp lệ.")
    except EmployeeNotFoundError as error:
        print(error)
    except IndexError:
        print("Chưa có dữ liệu.")


def menu_salary_management(company):
    print_header("4. QUẢN LÝ LƯƠNG")
    print("a. Tính lương cho từng nhân viên")
    print("b. Tính tổng lương công ty")
    print("c. Top 3 nhân viên lương cao nhất")
    choice = read_input("Chọn chức năng: ").lower()

    try:
        if choice == "a":
            print(format_employee_table(company.get_all_employees()))
        elif choice == "b":
            total_payroll = calculate_total_payroll(company.get_all_employees())
            print(f"Tổng lương công ty: {format_currency(total_payroll)}")
        elif choice == "c":
            top_employees = get_top_paid_employees(company.get_all_employees())
            print(format_employee_table(top_employees))
        else:
            print("Lựa chọn không hợp lệ.")
    except IndexError:
        print("Chưa có dữ liệu.")


def menu_project_management(company):
    print_header("5. QUẢN LÝ DỰ ÁN")
    print("a. Phân công nhân viên vào dự án")
    print("b. Xóa nhân viên khỏi dự án")
    print("c. Hiển thị dự án của 1 nhân viên")
    choice = read_input("Chọn chức năng: ").lower()

    try:
        employee_id = prompt_non_empty("Nhập ID nhân viên: ")
        if choice == "a":
            project_name = prompt_non_empty("Tên dự án: ")
            employee = company.assign_project(employee_id, project_name)
            print(f"Đã phân công {employee.name} vào dự án {project_name}.")
        elif choice == "b":
            project_name = prompt_non_empty("Tên dự án cần xóa: ")
            employee = company.remove_project(employee_id, project_name)
            print(f"Đã xóa {employee.name} khỏi dự án {project_name}.")
        elif choice == "c":
            employee = company.find_employee_by_id(employee_id)
            print(format_projects(employee))
        else:
            print("Lựa chọn không hợp lệ.")
    except EmployeeNotFoundError as error:
        print(error)
    except ProjectAllocationError as error:
        print(error)


def menu_performance(company):
    print_header("6. ĐÁNH GIÁ HIỆU SUẤT")
    print("a. Cập nhật điểm hiệu suất cho nhân viên")
    print("b. Hiển thị nhân viên xuất sắc (điểm > 8)")
    print("c. Hiển thị nhân viên cần cải thiện (điểm < 5)")
    choice = read_input("Chọn chức năng: ").lower()

    try:
        if choice == "a":
            employee_id = prompt_non_empty("Nhập ID nhân viên: ")
            score = prompt_score()
            employee = company.update_performance(employee_id, score)
            print(f"Đã cập nhật điểm hiệu suất cho {employee.name}: {employee.performance_score}")
        elif choice == "b":
            print(format_employee_table(company.get_excellent_employees()))
        elif choice == "c":
            print(format_employee_table(company.get_employees_need_improvement()))
        else:
            print("Lựa chọn không hợp lệ.")
    except EmployeeNotFoundError as error:
        print(error)
    except IndexError:
        print("Chưa có dữ liệu.")


def menu_hr_management(company):
    print_header("7. QUẢN LÝ NHÂN SỰ")
    print("a. Xóa nhân viên (nghỉ việc)")
    print("b. Tăng lương cơ bản cho nhân viên")
    print("c. Thăng chức (Intern -> Developer, Developer -> Manager)")
    choice = read_input("Chọn chức năng: ").lower()

    try:
        employee_id = prompt_non_empty("Nhập ID nhân viên: ")
        if choice == "a":
            employee = company.remove_employee(employee_id)
            print(f"Đã xóa nhân viên {employee.name} khỏi hệ thống.")
        elif choice == "b":
            amount = prompt_non_negative_float("Nhập số tiền tăng lương: ")
            employee = company.increase_salary(employee_id, amount)
            print(
                f"Đã tăng lương cơ bản cho {employee.name}. "
                f"Lương mới: {format_currency(employee.base_salary)}"
            )
        elif choice == "c":
            current_employee = company.find_employee_by_id(employee_id)
            if isinstance(current_employee, Intern):
                programming_language = prompt_non_empty("Ngôn ngữ lập trình sau thăng chức: ")
                overtime_hours = prompt_non_negative_float("Giờ OT mặc định (Enter = 0): ", default=0)
                promoted_employee = company.promote_employee(
                    employee_id,
                    programming_language=programming_language,
                    overtime_hours=overtime_hours,
                )
            elif isinstance(current_employee, Developer):
                team_size = prompt_non_negative_int("Số thành viên đội nhóm quản lý: ")
                allowance = prompt_non_negative_float("Phụ cấp quản lý (Enter = 5000000): ", default=5000000)
                promoted_employee = company.promote_employee(
                    employee_id,
                    team_size=team_size,
                    management_allowance=allowance,
                )
            else:
                promoted_employee = company.promote_employee(employee_id)
            print(
                f"Đã thăng chức thành công. {promoted_employee.name} hiện là "
                f"{promoted_employee.role_name}."
            )
        else:
            print("Lựa chọn không hợp lệ.")
    except EmployeeNotFoundError as error:
        print(error)
    except EmployeeException as error:
        print(error)


def menu_reports(company):
    print_header("8. THỐNG KÊ BÁO CÁO")
    print("a. Số lượng nhân viên theo loại")
    print("b. Tổng lương theo phòng ban")
    print("c. Số dự án trung bình trên mỗi nhân viên")
    choice = read_input("Chọn chức năng: ").lower()

    try:
        if choice == "a":
            print(format_report_block("Số lượng nhân viên theo loại", company.count_employees_by_role()))
        elif choice == "b":
            print(format_report_block("Tổng lương theo phòng ban", company.total_salary_by_department()))
        elif choice == "c":
            average = company.average_projects_per_employee()
            print(f"Số dự án trung bình trên mỗi nhân viên: {average:.2f}")
        else:
            print("Lựa chọn không hợp lệ.")
    except IndexError:
        print("Chưa có dữ liệu.")


def show_main_menu():
    print_header("HỆ THỐNG QUẢN LÝ NHÂN VIÊN CÔNG TY ABC")
    print("1. Thêm nhân viên mới")
    print("2. Hiển thị danh sách nhân viên")
    print("3. Tìm kiếm nhân viên")
    print("4. Quản lý lương")
    print("5. Quản lý dự án")
    print("6. Đánh giá hiệu suất")
    print("7. Quản lý nhân sự")
    print("8. Thống kê báo cáo")
    print("9. Thoát")


def main():
    company = Company("Công ty ABC")
    actions = {
        "1": menu_add_employee,
        "2": menu_show_employees,
        "3": menu_search_employee,
        "4": menu_salary_management,
        "5": menu_project_management,
        "6": menu_performance,
        "7": menu_hr_management,
        "8": menu_reports,
    }

    while True:
        show_main_menu()
        try:
            choice = read_input("Chọn chức năng (1-9): ")
            if choice == "9":
                print("Đã thoát chương trình.")
                break

            action = actions.get(choice)
            if not action:
                raise ValueError

            action(company)
        except EOFError:
            print("\nĐầu vào đã kết thúc. Chương trình tự thoát.")
            break
        except ValueError:
            print("Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 9 hoặc đúng ký tự submenu.")
        pause()


if __name__ == "__main__":
    main()
