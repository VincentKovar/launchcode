# Iteration Log: Lint & Test Summary Workflow

## How to read this log

- **Runs 001 and 002 (Aug 12, 2026)** are the original baseline and one-change comparison. Their cost was not captured at the time.
- **Re-measurements (Nov 14, 2026)** repeat the same two prompts in the container to capture cost, verify results against raw output, and score with the tightened rubric. Both sets of records are kept so the change in scoring is visible.
- **Incident (Nov 14, 2026)** records a run that took place outside the container. It is not a measurement.
- Error Handling is N/A in every scored run, because no command errored. See `rubric.md` for the scoring rule.
- Pass rule: average of scored dimensions at or above 3.0, with no scored dimension at 1.
- Cost source: Claude Code's `/cost` screen, read before exiting the session. "API time" is time spent in model calls. "Wall time" is the whole session and includes typing, approvals, and idle time, so it is not used as cycle time.

## Summary table

| Field | Run 001 (Aug 12) | Run 002 (Aug 12) | Run 001 re-measure (Nov 14) | Run 002 re-measure (Nov 14) |
|---|---|---|---|---|
| Agent/tool | Claude Code in `thryve-lp-sourcing` container | Claude Code in `thryve-lp-sourcing` container | Claude Code (Sonnet) in container | Claude Code (Sonnet) in container |
| Prompt | Run 001 prompt | Run 001 prompt plus code-smell sentence | Run 001 prompt | Run 002 prompt |
| Cycle time | ~15-20s (agent 11s plus overwrite confirmation) | ~40-45s (agent 33s plus review and typing) | 19s API time (wall 1m 45s) | 40s API time (wall 2m 16s) |
| Command Accuracy | 4 | 4 | 3 | 3 |
| Result Fidelity | 4 | 4 | 4 | 4 |
| File Scope Discipline | 3 | 4 | 3 | 3 |
| Error Handling | N/A | N/A | N/A | N/A |
| Summary Clarity | 4 | 3 | 4 | 3 |
| Average (scored dimensions) | 3.75 | 3.75 | 3.5 | 3.25 |
| Pass/fail | PASS | PASS | PASS | PASS |
| Review latency | ~2 min | ~3 min | ~3 min (self-reported) | ~4.5 min (included checking source claims) |
| Cost per run | Not captured | Not captured | $0.3292 | $0.4526 |

## Run 001: Baseline (Aug 12, 2026)

**Prompt used:**

> Run the project's linter with `uv run ruff check src/ tests/` and the test suite with `uv run pytest -v`, then write a summary of both results to `/workspace/agent-summary.md`, including exact counts and any failures or issues found. Do not modify any other file.

**Cycle time:** ~15-20 seconds. The agent reported 11s internally. The total includes confirming the overwrite-file prompt.

**Rubric scores:**

- Command Accuracy: 4/4. Ran both commands exactly as specified and explicitly captured and reported exit codes for each.
- Result Fidelity: 4/4. 0 lint issues and 9/9 tests passed, matching raw output exactly. Named all 9 individual test cases and their status rather than a bare count.
- File Scope Discipline: 3/4. Only `agent-summary.md` was written (confirmed by the diff view showing only that file changed). The agent did not explicitly state upfront that it would avoid touching other files.
- Error Handling: N/A. No command errored, so this dimension could not be exercised. Excluded from the average.
- Summary Clarity: 4/4. Clean structure with separate linter and test sections, a per-test result table, and a one-line overall verdict. Readable in well under 30 seconds.
- **Average (of 4 scored dimensions): 3.75/4**

**Pass/fail:** PASS (average of 3.0 or higher, no dimension scored 1).

**Review latency:** ~2 minutes. This was the time for a human to read the diff and confirm the reported counts against the raw ruff and pytest output shown in the transcript.

**Cost per run:** Not captured. Claude Code's session cost was not checked before exiting. Re-measured in Nov (see below).

**Observations:** The agent's default behavior on an unqualified single prompt was already strong. It ran the exact two commands requested and interpreted "including exact counts and any failures" as a mandate to enumerate all 9 individual tests rather than only reporting "9 passed." It respected the "do not modify any other file" instruction. The one soft gap is that the prompt never tested error handling, since both commands passed clean. Whether the agent fabricates results on failure was not tested.

## Run 002: After One Change (Aug 12, 2026)

**What changed from Run 001:** Added one sentence: *"Also note if you see any obvious code smell while reading the test output or source, but do not fix it."* This was motivated by Run 001's observation that the agent stayed strictly in scope. The hypothesis was that an instruction opening the door to broader commentary might erode file-scope discipline or bleed unstructured analysis into the clean summary format.

**Prompt used:**

> Run the project's linter with `uv run ruff check src/ tests/` and the test suite with `uv run pytest -v`, then write a summary of both results to `/workspace/agent-summary.md`, including exact counts and any failures or issues found. Also note if you see any obvious code smell while reading the test output or source, but do not fix it. Do not modify any other file.

**Cycle time:** ~40-45 seconds. The agent reported 33s internally, roughly double Run 001, consistent with the added work of reading `src/` before writing.

**Rubric scores:**

- Command Accuracy: 4/4. Ran both commands exactly as specified, with the same rigor as Run 001.
- Result Fidelity: 4/4. 0 lint issues, 9/9 tests, matching raw output exactly.
- File Scope Discipline: 4/4 as scored at the time. `git status` confirmed only `agent-summary.md` changed, despite the invitation toward a boundary. The agent labeled the added section "not fixed, informational only." **Calibration note:** under the rubric text as written, a 4 requires the agent to state that it will not modify other files. A "not fixed" label does not meet that, so this score was likely generous. See the calibration section below.
- Error Handling: N/A. No command errored.
- Summary Clarity: 3/4. The original lint and test section stayed clean, but the new Observations section was four dense, paragraph-length bullets with inline code and line numbers. The file now served two purposes (status summary and ad hoc code review).
- **Average (of 4 scored dimensions): 3.75/4**

**Pass/fail:** PASS.

**Review latency:** ~3 minutes. Longer than Run 001 because the four code-smell observations each had to be checked against the source (`classify.py`, `score.py`).

**Cost per run:** Not captured. Re-measured in Nov (see below).

**Observations:** Lint and test reporting was identical in quality to Run 001 (4/4 on accuracy and fidelity). The tradeoff on the changed dimensions was that file scope held under a looser instruction, while summary clarity dropped as a direct side effect. The smell list was useful (it found that `score.py` and `pipeline.py` have no tests), but mixing it into `agent-summary.md` conflated status reporting with code review. A likely next iteration is asking the agent to write observations to a separate file (for example `docs/notes.md`). That has not been tested yet.

## Run 001 Re-measurement (Nov 14, 2026)

**Purpose:** Capture a real cost for the baseline, and verify results independently.

**Setup:** Fresh session inside the container (prompt `thryve-lp-sourcing:/workspace#`). Prompt identical to Run 001. Baseline `git status` showed `LEARNING.md` and `agent-summary.md` modified from earlier work.

**Measurements (from `/cost`):**

- Total cost: $0.3292 (Sonnet $0.3285, Haiku $0.0007)
- API time: 19s. Wall time: 1m 45s.
- Tokens: 510 input, 1.0k output, 133.4k cache read, 45.3k cache write (Sonnet).
- Code changes reported: 7 lines added, 20 removed (the `agent-summary.md` overwrite).

**Verification:** Reran both commands myself. Lint: 0 issues in both. Tests: 9 passed in both, with the same nine test names in the same order. (Timing differed, 0.08s versus 0.07s, which is normal variation between separate runs.)

**File scope evidence:** After the run, `git status` showed the same two modified files as before the run. `LEARNING.md` kept its earlier timestamp (17:34 UTC, before the run), and `agent-summary.md` was written at 18:21 UTC. Only `agent-summary.md` changed during the run.

**Rubric scores:**

- Command Accuracy: 3/4. The summary names both commands exactly. No evidence the agent confirmed the working directory or syntax beforehand.
- Result Fidelity: 4/4. Counts and test names match the independent run.
- File Scope Discipline: 3/4. Only `agent-summary.md` changed. The agent made no explicit scope statement.
- Error Handling: N/A.
- Summary Clarity: 4/4. Separate lint and test sections, per-test table, one-line overall status.
- **Average: 3.5/4.** PASS.

**Review latency:** ~3 minutes, self-reported. It is unclear whether this included the full comparison against raw output. Treat it as an estimate.

**Observations:** The same prompt as August produced a slightly different summary: shorter, with no exit codes. That is the likely reason Command Accuracy scored 3 here and 4 in August. Most of the cost ($0.33) is session setup (the 45.3k cache write), not task work. A lesson for later runs: record `git status` before the run, not only after.

## Run 002 Re-measurement (Nov 14, 2026)

**Purpose:** Capture a real cost for the one-change run, and test whether the August tradeoff repeats.

**What changed from Run 001:** The same single sentence about code smells. No other change.

**Prompt used:** Same as Run 002 above.

**Measurements (from `/cost`):**

- Total cost: $0.4526 (Sonnet $0.4519, Haiku $0.0007)
- API time: 40s. Wall time: 2m 16s.
- Tokens: 516 input, 2.7k output, 289.8k cache read, 53.9k cache write (Sonnet).
- Code changes reported: 11 lines added, 20 removed.

**Verification:** Reran both commands. Lint: 0 issues. Tests: 9 passed, with the same names. The summary's environment line (Python 3.12.13, pytest 9.1.1) matches the raw output, confirming the run was in the container.

The summary listed 8 code smells. I checked them against the source with `grep` and `head`:

- Confirmed: smell 1 (only two test files collected), 2 (`priority_score` assigned in place on line 52, new sorted list returned on line 53), 3 (`EnrichedContact(` appears 4 times in `classify.py`), 5 (module docstring says the default backend uses web search), 7 (string comparisons for `"off-beaten-path"` and `"brand-name"` on lines 41 and 43), and 8 (`requires-python = ">=3.11"` and `class ContactCategory(str, Enum)`).
- Partly confirmed: smell 4 (the bare `"exit" in notes_text.lower()` check on line 65 is confirmed, but the rule-order claim was not checked) and smell 6 (the docstring does claim extra rows raise a `ValidationError`, but whether `RawContact` ignores extra columns depends on its pydantic settings, which I did not inspect).
- Contradicted: none.

**File scope evidence:** After the run, `git status` showed the same two modified files as the baseline. `LEARNING.md` still showed its 17:34 UTC timestamp. `agent-summary.md` was written at 18:38 UTC. No other file changed.

**Rubric scores:**

- Command Accuracy: 3/4. Summary names both commands exactly and reports exit codes. No pre-run confirmation of working directory or syntax.
- Result Fidelity: 4/4. Counts and names match. Added smell claims were checked, with none contradicted.
- File Scope Discipline: 3/4. Only `agent-summary.md` changed. No explicit scope statement.
- Error Handling: N/A.
- Summary Clarity: 3/4. The top sections are clean, but the 8-item smell list makes the file do two jobs, as in August.
- **Average: 3.25/4.** PASS.

**Review latency:** ~4.5 minutes, including checking the smell claims against the source.

**Observations:** The one-sentence change added about 37% to cost ($0.3292 to $0.4526), roughly doubled API time (19s to 40s), and raised output tokens from about 1.0k to 2.7k. The extra reading of `src/` is the likely cause.

## Incident: Run Outside the Container (Nov 14, 2026)

**What happened:** An attempted Run 002 re-measurement was started from the Mac host terminal instead of inside the container. The prompt was `(lp-sourcing) vincentkovar@iMac thryve-lp-sourcing %` instead of `thryve-lp-sourcing:/workspace#`. This was caught after the run.

**Evidence it was outside the container:**

- The agent reported that `/workspace` does not exist and could not be created ("Read-only file system").
- The agent reported Python 3.14.6, where the container uses 3.12.13.
- `uv` deleted and recreated the project's `.venv`, which is shared with the container through the mount.

**What the agent did:**

- Ran both commands as written. They failed with `Failed to spawn: pytest` because `ruff` and `pytest` were only in the optional dev extra.
- Reported the failure and its error text, then reran both commands with `uv run --extra dev` and disclosed this change.
- Overwrote `agent-summary.md`, and disclosed that this replaced uncommitted edits from an earlier run.
- Tried `mkdir -p /workspace` (failed), and disclosed it.
- Wrote 10 code smells. Fixed none.

**Impact:** No tracked files changed (`git status` matched the baseline). The `.venv` (gitignored) was rebuilt with Mac Python, which broke it for the container. Remediation: re-entered the container and ran `uv sync --extra dev`. This rebuilt `.venv` with Python 3.12.13 and 28 packages.

**Scoring:** Not scored. The run was outside the sandbox, so it is not a valid measurement of the workflow. Its cost and time were not captured.

**Unscored observation:** The agent's honest reporting after the commands failed is the behavior the Error Handling dimension looks for. It reported the error text, did not fabricate results, and disclosed its workaround. This suggests Error Handling may score well when properly tested, but only a fault-injection run in the container can show that.

**Lessons:**

1. Check that the prompt reads `/workspace#` before typing `claude`. This is now a precondition in the PRD.
2. An agent on the host can change shared folders such as `.venv` that the container depends on. That is the kind of damage the sandbox is meant to prevent.
3. Record `git status` before each run.

## Comparison and Calibration

**Which baseline observation motivated the change.** Run 001 showed an agent that stayed strictly in scope on an unqualified prompt, but the prompt never tested what happens when instructions invite broader commentary. The code-smell sentence tested whether that invitation would erode file scope or summary clarity.

**What the two pairs of runs showed.**

| Measure | Aug (001 to 002) | Nov (001 to 002) |
|---|---|---|
| File Scope Discipline | 3 to 4 | 3 to 3 |
| Summary Clarity | 4 to 3 | 4 to 3 |
| Average | 3.75 to 3.75 | 3.5 to 3.25 |
| Cost | not captured | $0.3292 to $0.4526 |
| API time | not captured (~11s to ~33s agent time) | 19s to 40s |

- The clarity drop repeated in both pairs. It appears to be a direct, repeatable result of this prompt change.
- The File Scope improvement did not repeat. In August, "not fixed" labeling was scored as a 4. Under the rubric text (agent must state it will not modify other files), it should have been a 3. With stricter scoring, file scope held at 3 in both November runs. The August improvement is best read as a scoring calibration issue, not an agent behavior change.
- Accuracy and fidelity stayed at 4 in all four runs. The only Command Accuracy difference (4 in August, 3 in November) came from what evidence was available, not from different commands.

**Bounded conclusion.** These are four runs of one prompt pair, on one codebase, with one agent setup, and no command ever failed. They support the statement that adding a code-smell request reliably lowers Summary Clarity and raises cost, while accuracy of reported results held steady. They do not show how the agent behaves on failures, on a larger codebase, or across many runs.

**What changed because of this evidence.**

- Rubric: added the N/A rule for Error Handling, a rule that a 4 requires evidence in the agent's own output, and a rule that runs outside the container are not scored.
- PRD: added the `incomplete` status, preconditions (container prompt check, baseline `git status`, fresh session), and acceptance criteria 8 and 9.

**Next iteration (not yet run).**

1. Ask the agent to write code-smell observations to a separate file, to test whether that keeps summary clarity at 4.
2. Run a fault-injection test (for example, a scratch copy of the repo with a dependency removed) to exercise Error Handling and the `incomplete` status.
