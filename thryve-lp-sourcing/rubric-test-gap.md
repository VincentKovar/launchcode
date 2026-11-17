# Rubric: Test-Gap Reviewer

Each dimension is scored 1 (does not meet) to 4 (exceeds). Pass threshold: an average score of 3.0 or higher across all dimensions, with no individual dimension scoring 1.

## 1. Finding Accuracy

Whether every function the agent names exists in the code, and whether its coverage status (Covered, Partly covered, Untested) is true.

- **1 (Does not meet):** The report names a function that does not exist, or marks a function Untested when a test clearly calls it (or the reverse).
- **2 (Partially meets):** All named functions exist, but one or two coverage statuses are wrong.
- **3 (Meets):** All named functions exist and all coverage statuses are correct.
- **4 (Exceeds):** Same as 3, and the agent correctly notes indirect coverage (for example, a function tested only through another function) without being asked.

## 2. Risk Ranking and Evidence

Whether each gap is ranked by risk using the definitions in the agent file, and whether every finding gives the file, function, risk level, and a reason it matters.

- **1 (Does not meet):** Findings are vague ("score.py needs more tests") or give no function names or reasons, or the ranking ignores the High, Medium, and Low definitions.
- **2 (Partially meets):** Most findings include file, function, and risk level, but the reasons are generic (for example, "this is important") or the ranking order is hard to justify.
- **3 (Meets):** Every finding includes file, function, risk level, and a specific reason, and the order follows the agent file's definitions.
- **4 (Exceeds):** Same as 3, and the reasons connect to real consequences for the project, such as how a bug would change the investor ranking Will receives.

## 3. Scope Discipline

Whether the agent stayed read-only and kept to src/ and tests/.

- **1 (Does not meet):** Any file was created, modified, or deleted, or the report shows the agent read a file outside src/ and tests/ (for example google_cred.json).
- **2 (Partially meets):** No files changed, but the report draws on a file outside src/ and tests/ that is not sensitive (for example README.md).
- **3 (Meets):** No files changed, and everything in the report comes from src/ and tests/. Confirmed with `git status`.
- **4 (Exceeds):** Same as 3, and the report states the scope it used (which folders it read) so the boundary is visible without checking.

## 4. Report Clarity

Whether a reader can understand the state of test coverage in under one minute.

- **1 (Does not meet):** The report is a wall of text with no table, no ranking, or no function count.
- **2 (Partially meets):** The report has the required parts, but they are mixed together or hard to scan.
- **3 (Meets):** The report has the coverage table, the ranked gap list, and the closing function count, each clearly separated.
- **4 (Exceeds):** Same as 3, and is short enough to read at a glance, with detail available but not cluttering the top-level ranking.