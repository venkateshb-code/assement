import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMPLOYEES_FILE = ROOT / "data" / "employees.csv"


def bonus(salary, rate=0.1, *extras, **options):
    # """Return salary * rate plus extras, optionally limited by cap."""
    result = salary * rate + sum(extras)
    if "cap" in options:
        result = min(result, options["cap"])
    return result


class InvalidSalaryError(Exception):
    """Raised when an employee salary is negative."""


class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"Employee: {self.name}, Salary: {self.salary}"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return (
            f"Manager: {self.name}, Salary: {self.salary}, "
            f"Team size: {self.team_size}"
        )


def read_employees():
    with EMPLOYEES_FILE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    employees = read_employees()
    # CSV values are strings; convert salary before numeric operations.
    for employee in employees:
        employee["salary"] = int(employee["salary"])

    above_50000 = [
        employee["name"] for employee in employees
        if employee["salary"] > 50000
    ]
    print("Above 50000:", above_50000)

    raised_salaries = list(map(lambda salary: round(salary * 1.10, 2),
                               [e["salary"] for e in employees]))
    print("Salaries after 10% raise:", raised_salaries)

    chennai_employees = list(filter(
        lambda employee: employee["city"] == "Chennai", employees
    ))
    print("Chennai:", [employee["name"] for employee in chennai_employees])

    print("Bonus example:", bonus(50000, 0.1, 500, 250, cap=6000))
    worker = Employee("Arun", 30000)
    manager = Manager("Divya", 75000, team_size=5)
    print(worker.get_details())
    print("Annual salary:", worker.annual_salary())
    print(manager.get_details())

    try:
        Employee("Invalid", -500)
    except InvalidSalaryError as error:
        print("Error:", error)
    finally:
        print("Transaction finished")

    # Continue skips salary 0; break stops after the first salary > 85000.
    print("Loop demonstration:")
    for employee in employees:
        salary = employee["salary"]
        if salary == 0:
            continue
        if salary > 85000:
            print("Stopping at:", employee["name"], salary)
            break
        print(employee["name"], salary)


if __name__ == "__main__":
    main()
