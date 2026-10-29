# Analysis notes

- Missing salary values in `employees_raw.csv` are filled with the median of the non-missing salaries.
- The exact duplicate row is removed with `drop_duplicates()`.
- ID and salary are converted to numeric types; text columns are stripped and title-cased.
- The IQR rule is not used to delete salary values because the supplied eight-row dataset is small and a high salary may be valid; inspect values before deciding to remove any outlier.
- `Marketing` is the extra department with no employees and appears in the outer join.
- The monthly sales line uses the exact assessment values: Jan–Jun = 12, 15, 14, 18, 22, 25.
