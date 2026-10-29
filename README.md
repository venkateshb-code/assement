# Week 1 Python & Data Engineering Assessment

## Setup
1. Create and activate a virtual environment.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. Keep secrets in a local `.env` file. Never commit `.env`.
4. Run Task 1: `python src/task1_core_oop.py`
5. Run Task 2: `python src/task2_files_api.py`
6. Run Task 3: `python src/task3_analysis.py`
7. Start Jupyter: `jupyter notebook notebooks/assessment.ipynb`

## Data
- `data/employees.csv`: the eight assessment employees.
- `data/employees_raw.csv`: Task 3 cleaning exercise with two missing salaries and one duplicate.
- `data/departments.csv`: four listed departments and Marketing, which has no employees.

## Five-line findings summary
- The supplied employee data contains 8 records across Sales, HR, IT and Finance.
- Five employees earn more than 50000.
- IT has the largest headcount (3) in the supplied data.
- The raw cleaning sample has two missing salaries and one duplicate row.
- Marketing is the extra department with no employees, so it appears in the outer join.

## Git submission
Create branch `feature/analysis`, make at least five small commits, open and merge a Pull Request, and resolve a deliberate README conflict as described in the assessment guide. Add your real PR URL and screenshot of `git log --oneline --graph` before submission.
