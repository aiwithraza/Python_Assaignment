from abc import ABC, abstractmethod


def check_not_negative(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a number")
    if value < 0:
        raise ValueError(f"{label} cannot be negative")


class Employee(ABC):
    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Employee name cannot be empty")
        self.name = name.strip()

    @abstractmethod
    def calculate_pay(self):
        pass


class SalariedEmployee(Employee):
    def __init__(self, name, monthly_salary):
        super().__init__(name)
        check_not_negative(monthly_salary, "Salary")
        self.monthly_salary = monthly_salary

    def calculate_pay(self):
        return self.monthly_salary


class HourlyEmployee(Employee):
    def __init__(self, name, hourly_rate, hours_worked):
        super().__init__(name)
        check_not_negative(hourly_rate, "Hourly rate")
        check_not_negative(hours_worked, "Hours worked")
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_pay(self):
        normal_hours = min(self.hours_worked, 40)
        overtime_hours = max(self.hours_worked - 40, 0)
        return normal_hours * self.hourly_rate + overtime_hours * self.hourly_rate * 1.5


class CommissionEmployee(Employee):
    def __init__(self, name, base_salary, sales, commission_rate):
        super().__init__(name)
        check_not_negative(base_salary, "Base salary")
        check_not_negative(sales, "Sales")
        check_not_negative(commission_rate, "Commission rate")
        if commission_rate > 1:
            raise ValueError("Commission rate must be between 0 and 1")
        self.base_salary = base_salary
        self.sales = sales
        self.commission_rate = commission_rate

    def calculate_pay(self):
        return self.base_salary + self.sales * self.commission_rate


def payroll_summary(employees):
    lines = []
    total = 0
    for employee in employees:
        if not isinstance(employee, Employee):
            raise TypeError("Payroll can only contain Employee objects")
        pay = employee.calculate_pay()
        lines.append((employee.name, type(employee).__name__, pay))
        total += pay
    return lines, total


def main():
    try:
        Employee("Test")
    except TypeError as error:
        print("Error:", error)

    staff = [
        SalariedEmployee("Ahmed", 60000),
        HourlyEmployee("Sana", 20, 45),
        CommissionEmployee("Bilal", 500, 4000, 0.10),
        HourlyEmployee("Hina", 15, 30),
    ]
    lines, total = payroll_summary(staff)

    print(f"{'Name':<10}{'Type':<22}{'Pay':>10}")
    for name, kind, pay in lines:
        print(f"{name:<10}{kind:<22}{pay:>10.2f}")
    print(f"{'TOTAL':<32}{total:>10.2f}")


if __name__ == "__main__":
    main()