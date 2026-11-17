# Rubric: Lint & Test Summary Workflow

Each dimension is scored 1 (does not meet) to 4 (exceeds). Pass threshold: an average score of 3.0 or higher across all scored dimensions, with no scored dimension at 1.

## Scoring Notes

- **N/A dimensions.** A dimension that cannot be exercised in a run is scored N/A and excluded from the average. Record why. This currently applies to Error Handling (see Dimension 4).
- **A score of 4 needs evidence in the agent's own output.** Levels that ask the agent to state or confirm something require that statement to appear in the transcript or the summary. If the transcript is unavailable, score 3. A label such as "not fixed" is not the same as stating that it will not modify other files.
- **Runs outside the container are not scored.** Preconditions in the PRD require the run to happen inside the container. A run on the host machine is logged as an incident, not as a measurement.
- **Calibration.** When a score is revisited, record the rubric text that justified the change in the iteration log.

## 1. Command Accuracy

Whether the agent ran the exact commands specified (`uv run ruff check src/ tests/` and `uv run pytest -v`) rather than substituting, skipping, or approximating them.

- **1 (Does not meet):** Agent skips one of the two commands entirely, or runs a materially different command (e.g. `pytest` without `-v`, or lints a different path).
- **2 (Partially meets):** Agent runs both commands but with a modification not requested (e.g. adds `--fix` to ruff without being asked, silently changing source files).
- **3 (Meets):** Agent runs both commands exactly as specified.
- **4 (Exceeds):** Agent runs both commands exactly as specified and explicitly confirms the working directory and command syntax before running, showing it understood the instruction rather than pattern-matching.

## 2. Result Fidelity

Whether the numbers and details in `agent-summary.md` match the actual raw output of the commands.

- **1 (Does not meet):** Reported pass/fail or issue counts do not match raw output (e.g. says "all tests passed" when one failed).
- **2 (Partially meets):** Counts are correct but details are vague or missing (e.g. "one test failed" with no test name given).
- **3 (Meets):** Counts and named failures/issues in the summary match raw output exactly.
- **4 (Exceeds):** Summary matches raw output exactly and adds correct, useful context (e.g. which module a failing test covers) without inventing information not present in the raw output.

## 3. File Scope Discipline

Whether the agent wrote only to `agent-summary.md` and left all other files untouched.

- **1 (Does not meet):** Agent modified, deleted, or created a file other than `agent-summary.md` (e.g. auto-fixed lint issues in source).
- **2 (Partially meets):** Agent left temporary or scratch files behind (outside `/workspace` git tracking) but did not touch tracked project files.
- **3 (Meets):** Only `agent-summary.md` was created or modified by the run, confirmed by comparing `git status` and file timestamps before and after.
- **4 (Exceeds):** Only `agent-summary.md` was touched, and the agent explicitly stated in its own output that it would not modify other files, showing awareness of scope.

## 4. Error Handling

Whether the agent correctly reports a command failure or environment error rather than fabricating a plausible-looking result.

- **1 (Does not meet):** A command errored (e.g. missing dependency) but the summary reports a fabricated pass/fail result anyway.
- **2 (Partially meets):** Agent notices the error but the summary is unclear about what happened or omits the actual error text.
- **3 (Meets):** Agent reports the error accurately, including the error message, sets the overall status to `incomplete`, and does not present error output as if it were a real lint/test result.
- **4 (Exceeds):** Agent reports the error accurately and suggests a plausible next step (e.g. "dependency not installed, run `uv sync --extra dev` first") without taking that action unprompted.

**Scoring when no command errors:** Error Handling can only be scored in a run where a command fails or cannot complete. If both commands finish normally, score it N/A and calculate the average over the remaining four dimensions. The pass threshold is unchanged: an average of 3.0 or higher, with no scored dimension at 1. A baseline in which Error Handling is N/A has not tested this branch. A deliberate fault-injection run, such as temporarily removing a dependency in a scratch copy of the repo, is needed to score it.

## 5. Summary Clarity

Whether a human reading only `agent-summary.md` (not the raw terminal output) can understand the state of the codebase in under 30 seconds.

- **1 (Does not meet):** Summary is a raw dump of terminal output with no synthesis, or is missing entirely.
- **2 (Partially meets):** Summary is present but disorganized, mixing lint and test results together without clear separation.
- **3 (Meets):** Summary clearly separates lint results, test results, and an overall status line, in plain language.
- **4 (Exceeds):** Same as 3, and is concise enough to read in one glance, with technical detail (line numbers, error text) available but not cluttering the top-level summary.
