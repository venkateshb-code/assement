# Terminal Commands — Week 1 Assessment

Run these in **VS Code Terminal (PowerShell)**. First extract the project ZIP, then `cd` into `week1-assessment`.

## Environment and dependencies
```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```
If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```
The `.env` file is ignored by Git. JSONPlaceholder is public and does not need a real API key; leave the sample placeholder or set your own key only if your trainer requests it.

## Run the tasks
```powershell
python src/task1_core_oop.py
python src/task2_files_api.py
python src/task3_analysis.py
```
Expected key Task 1 lines include:
```text
Above 50000: ['Rahul', 'Divya', 'Karthik', 'Meena', 'Suresh']
Chennai: ['Arun', 'Priya', 'Divya', 'Suresh']
Error: Invalid salary: -500
Transaction finished
```
Task 2 should print `Rows read: 8 | High earners: 5`, three users, and `/users/9999 -> 404 Not found` when the network is available.

## Task 4: terminal folders and grep
The project already contains `data/`, `notebooks/`, `reports/`, and `src/`. To demonstrate the requested commands:
```powershell
mkdir temp-demo
Copy-Item data\employees.csv temp-demo\employees-copy.csv
Move-Item temp-demo\employees-copy.csv data\employees-copy.csv
Remove-Item data\employees-copy.csv
Remove-Item temp-demo -Recurse
Select-String -Path data\employees.csv -Pattern "Chennai"
```
On macOS/Linux, use `grep -n "Chennai" data/employees.csv`, `mkdir -p`, `cp`, and `mv`.

## Jupyter and export
```powershell
jupyter notebook
```
Open `notebooks/assessment.ipynb`, run all cells, and use `%timeit` in the notebook. Export notebook to a Python script:
```powershell
jupyter nbconvert --to script notebooks/assessment.ipynb --output assessment_export
```

## Git/GitHub workflow
Create a **new empty GitHub repository** named `week1-assessment`, then in the project folder:
```powershell
git init
git add .gitignore README.md requirements.txt data src notebooks
git commit -m "Add assessment structure and sample data"
git branch -M main
git checkout -b feature/analysis
git add src/task1_core_oop.py
git commit -m "Implement Python OOP and error handling"
git add src/task2_files_api.py
git commit -m "Add CSV JSON and API workflow"
git add src/task3_analysis.py
git commit -m "Add data analysis and chart generation"
git add notebooks/assessment.ipynb
git commit -m "Add Jupyter analysis notebook"
git add data/departments.csv data/employees_raw.csv
git commit -m "Add cleaning and department join datasets"
git remote add origin https://github.com/YOUR-USERNAME/week1-assessment.git
git push -u origin main
git push -u origin feature/analysis
```
Replace `YOUR-USERNAME` with your GitHub username. On GitHub, open a Pull Request from `feature/analysis` to `main` and merge it.

### Deliberate README merge conflict
Do this only after pushing your work. Create two branches from updated `main`:
```powershell
git checkout main
git pull
git checkout -b feature/readme-a
Add-Content README.md "`nConflict edit from branch A."
git add README.md
git commit -m "Edit README from branch A"
git checkout main
git checkout -b feature/readme-b
Add-Content README.md "`nConflict edit from branch B."
git add README.md
git commit -m "Edit README from branch B"
git checkout feature/readme-a
git merge feature/readme-b
```
If Git merges automatically, edit the same README line differently on each branch and repeat the merge. If conflict markers appear, edit README.md to keep the intended final content and remove `<<<<<<<`, `=======`, `>>>>>>>`, then:
```powershell
git add README.md
git commit -m "Resolve README merge conflict"
git log --oneline --graph --all
```
Take a screenshot of the graph and submit it with the real Pull Request URL. Never invent a PR URL; copy the URL from your own GitHub PR page.
