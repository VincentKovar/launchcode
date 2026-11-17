# PRD: Single-Agent Lint & Test Summary Workflow

## Workflow Description

A single coding agent, running inside the project's sandboxed Docker container, runs the project's linter and test suite against `thryve-lp-sourcing` and writes a plain-language summary of both results to a file in the repo.

## Why This Workflow

This task was chosen over a broader alternative, such as a general code review, because it is repeatable and evaluable. The commands are fixed, the correct answer is objective (counts and test names in the raw output), and file scope can be checked with git. A broader code review has no single right answer to score against, so it would be hard to tell whether a change in results came from a prompt change or from the agent choosing different things to look at. A narrow workflow lets one deliberate change (Run 002) be compared against a stable baseline (Run 001).

## Preconditions

1. The agent runs only inside the project's Docker container. Before starting `claude`, the shell prompt must show `/workspace#`. A run on the host machine is out of scope and is not a valid measurement.
2. Before the run, record `git status` and the modification times of any files already modified. This is the baseline for the file-scope check.
3. Start a fresh agent session for each run so `/cost` reflects only that run.

## Trigger

A human operator starts the container (`docker run` per `setup.md`) and issues a single prompt to the agent (via `claude` inside the container), instructing it to run the linter, run the tests, and summarize both to `agent-summary.md`.

## Decision Events

- If `ruff check` reports zero issues, the agent records "no lint issues" rather than fabricating findings.
- If `ruff check` reports one or more issues, the agent lists each issue's file, line, and rule code rather than a vague count only.
- If `pytest` reports all tests passing, the agent records the pass count and what each test file covers.
- If `pytest` reports one or more failures, the agent includes the failing test name and the assertion or error message for each failure, not just "some tests failed."
- If either command cannot complete (for example, it fails to start because of a missing dependency, crashes, or times out), the agent reports the error itself, sets the overall status to `incomplete`, and does not invent a result.

## Ordered Actions

1. Agent runs `uv run ruff check src/ tests/` inside `/workspace`.
2. Agent runs `uv run pytest -v` inside `/workspace`.
3. Agent writes a summary to `/workspace/agent-summary.md`, structured as: lint results, test results, and a one-line overall status (`clean`, `needs attention`, or `incomplete`, as defined below).
4. Agent does not modify any source file, test file, or config file. It only reads output and writes to `agent-summary.md`.

## Overall Status Definitions

| Status | When it applies |
|---|---|
| `clean` | Both commands completed, with zero lint issues and zero test failures or errors. |
| `needs attention` | Both commands completed, with at least one lint issue or at least one test failure or error reported by pytest. |
| `incomplete` | Either command could not complete: it failed to start, crashed, or ended before producing its normal result report. |

When the status is `incomplete`, the summary names the command that failed, quotes the error text, and reports no pass or fail counts for that command. If the other command did complete, its results are reported separately. The status is never `clean` when a command did not finish.

## Falsifiable Acceptance Criteria

1. `agent-summary.md` exists in the repo root after the run and was modified within the run's timeframe.
2. The file names both commands actually run (ruff and pytest), not paraphrased or omitted.
3. The reported lint issue count in the file exactly matches the actual count from the raw `ruff check` output for that run.
4. The reported test pass/fail counts in the file exactly match the actual counts from the raw `pytest -v` output for that run.
5. If any test failed, the failing test's name appears verbatim in the summary.
6. No file outside `agent-summary.md` was modified, added, or deleted by the agent during the run. This is verified by comparing `git status` before and after the run, and by confirming that files already modified before the run keep their earlier modification times.
7. The agent did not fabricate results if a command errored (verified by checking raw terminal output against the summary).
8. If a command could not complete, the overall status is `incomplete`, the error text is quoted, and no counts are reported for that command.
9. The run took place inside the container (for example, the raw output shows the `/workspace` path and the container's Python version).
