# """Task 3: NumPy, Pandas, cleaning, joins, and charts."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save charts without requiring a desktop display.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def numpy_demo():
    marks = np.array([
        [80, 75, 90],
        [70, 85, 68],
        [92, 88, 77],
        [60, 65, 70],
    ])
    print("Marks shape:", marks.shape)
    print("Student averages:", marks.mean(axis=1))
    print("Subject averages:", marks.mean(axis=0))
    grace_marks = marks + 5  # broadcasting adds 5 to every score
    print("Marks with 5 grace marks:\n", grace_marks)
    weights = np.array([0.4, 0.35, 0.25])
    print("Weighted scores:", np.dot(marks, weights))


def clean_and_analyse():
    employees = pd.read_csv(DATA / "employees.csv")
    print("\n--- employees.info() ---")
    employees.info()
    print("\n--- employees.describe() ---")
    print(employees.describe(include="all"))
    print("\n--- loc example ---\n", employees.loc[employees["city"] == "Chennai"])
    print("\n--- iloc example ---\n", employees.iloc[:3])
    print("\n--- filter salary > 50000 ---\n", employees[employees["salary"] > 50000])

    raw = pd.read_csv(DATA / "employees_raw.csv")
    before_rows = len(raw)
    before_missing = int(raw.isna().sum().sum())
    before_duplicates = int(raw.duplicated().sum())

    # Make types/text consistent before analysis.
    raw["name"] = raw["name"].astype("string").str.strip().str.title()
    raw["department"] = raw["department"].astype("string").str.strip().str.title()
    raw["city"] = raw["city"].astype("string").str.strip().str.title()
    raw["id"] = pd.to_numeric(raw["id"], errors="coerce").astype("Int64")
    raw["salary"] = pd.to_numeric(raw["salary"], errors="coerce")
    # Salary is numeric and has two missing values; median is a robust simple fill.
    median_salary = raw["salary"].median()
    raw["salary"] = raw["salary"].fillna(median_salary)
    raw = raw.drop_duplicates().copy()
    raw["salary"] = raw["salary"].round(2).astype(float)

    after_rows = len(raw)
    after_missing = int(raw.isna().sum().sum())
    after_duplicates = int(raw.duplicated().sum())
    cleaning_summary = pd.DataFrame([
        {"stage": "Before", "rows": before_rows, "missing_values": before_missing,
         "duplicates": before_duplicates},
        {"stage": "After", "rows": after_rows, "missing_values": after_missing,
         "duplicates": after_duplicates},
    ])
    cleaning_summary.to_csv(REPORTS / "cleaning_summary.csv", index=False)
    raw.to_csv(DATA / "clean_data.csv", index=False)
    print("\nCleaning summary:\n", cleaning_summary)
    print(f"Median salary used to fill missing values: {median_salary}")

    grouped = raw.groupby("department").agg(
        headcount=("id", "count"),
        average_salary=("salary", "mean"),
        maximum_salary=("salary", "max"),
    ).reset_index()
    grouped.to_csv(REPORTS / "department_summary.csv", index=False)
    print("\nDepartment summary:\n", grouped)

    departments = pd.read_csv(DATA / "departments.csv")
    inner = raw.merge(departments, on="department", how="inner")
    left = raw.merge(departments, on="department", how="left")
    outer = raw.merge(departments, on="department", how="outer", indicator=True)
    inner.to_csv(REPORTS / "join_inner.csv", index=False)
    left.to_csv(REPORTS / "join_left.csv", index=False)
    outer.to_csv(REPORTS / "join_outer.csv", index=False)
    no_employee_departments = outer.loc[
        outer["_merge"] == "right_only", "department"
    ].dropna().unique().tolist()
    print("Inner join rows:", len(inner))
    print("Left join rows:", len(left))
    print("Departments with no employees:", no_employee_departments)

    return employees, raw, grouped


def make_charts(employees, grouped):
    # 1. Bar chart: average salary by department, with value labels.
    avg_salary = employees.groupby("department")["salary"].mean().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(avg_salary.index, avg_salary.values)
    ax.bar_label(bars, fmt="%.0f")
    ax.set(title="Average Salary by Department", xlabel="Department", ylabel="Average salary")
    ax.legend([bars], ["Average salary"])
    fig.tight_layout()
    fig.savefig(REPORTS / "chart_bar_avg_salary.png", dpi=150)
    plt.close(fig)
    print("Insight (bar): IT has the highest average salary in the supplied employee data.")

    # 2. Histogram with five bins.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(employees["salary"], bins=5, edgecolor="black", label="Employees")
    ax.set(title="Employee Salary Distribution", xlabel="Salary", ylabel="Number of employees")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "chart_histogram_salary.png", dpi=150)
    plt.close(fig)
    print("Insight (histogram): The histogram shows how salaries are distributed across five ranges.")

    # 3. Scatter: id vs salary, color by department and legend.
    fig, ax = plt.subplots(figsize=(8, 5))
    for department, subset in employees.groupby("department"):
        ax.scatter(subset["id"], subset["salary"], label=department)
    ax.set(title="Employee ID vs Salary", xlabel="Employee ID", ylabel="Salary")
    ax.legend(title="Department")
    fig.tight_layout()
    fig.savefig(REPORTS / "chart_scatter_id_salary.png", dpi=150)
    plt.close(fig)
    print("Insight (scatter): Karthik (Finance) has the highest salary among the eight employees.")

    # 4. Monthly sales line chart using assessment values.
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales = [12, 15, 14, 18, 22, 25]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(months, sales, marker="o", label="Monthly sales")
    ax.set(title="Monthly Sales (Jan–Jun)", xlabel="Month", ylabel="Sales")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS / "chart_line_monthly_sales.png", dpi=150)
    plt.close(fig)
    print("Insight (line): Monthly sales increased from 12 in January to 25 in June, with a small dip in March.")


if __name__ == "__main__":
    numpy_demo()
    employee_df, cleaned_df, department_df = clean_and_analyse()
    make_charts(employee_df, department_df)
    print(f"\nCharts and reports saved in: {REPORTS}")
