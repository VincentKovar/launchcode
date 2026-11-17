# PRD: Single-Agent Test Coverage Report Workflow

## Workflow Description

A single coding agent, running inside the project's sandboxed Docker container, runs the project's test suite with coverage measurement against `thryve-lp-sourcing` and writes a plain-language summary to a file in the repo, identifying which modules have zero test coverage.

## Trigger

A human operator starts the container (`docker run` per `setup.md`) and issues a single prompt to the agent (via `claude` inside the container), instructing it to run pytest with coverage and summarize the results to `docs/coverage-report.md`.

## Decision Events

- If `pytest-cov` is not installed, the agent reports the missing-dependency error accurately rather than fabricating a coverage result or installing the package itself.
- If the coverage command runs successfully, the agent records each module's coverage percentage, not just an overall project percentage.
- If one or more modules show 0% coverage, the agent explicitly calls those out by name rather than burying them in a full table.
- If the command produces a warning (not a hard failure) that does not stop execution, the agent notes the warning without treating it as an error.

## Ordered Actions

1. Agent runs `uv run pytest --cov=src --cov-report=term-missing` inside `/workspace`.
2. If the command errors (e.g. missing `pytest-cov`), agent writes the exact error to `docs/coverage-report.md` and stops. It does not attempt to fix the environment.
3. If the command succeeds, agent writes a summary to `/workspace/docs/coverage-report.md`, structured as: a per-module coverage table, a called-out list of any 0%-coverage modules, and a one-line overall status.
4. Agent does not modify any source file, test file, or config file (including `pyproject.toml`). It only reads output and writes to `docs/coverage-report.md`.

## Falsifiable Acceptance Criteria

1. `docs/coverage-report.md` exists and was modified within the run's timeframe.
2. The file names the exact command run.
3. If the command errored, the exact error text appears in the file, and no fabricated coverage numbers appear anywhere in it.
4. If the command succeeded, every module's reported coverage percentage in the file exactly matches the raw `pytest --cov` output for that run.
5. Any module at 0% coverage in the raw output is explicitly named in the file.
6. No file outside `docs/coverage-report.md` was modified, added, or deleted (verified via `git status` before/after).
7. `pyproject.toml` and `uv.lock` are unchanged (verified via `git diff`), confirming no package was installed as a side effect.