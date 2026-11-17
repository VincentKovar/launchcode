# Run 002 Evidence: Test-Gap Reviewer v0.2

Captured: 2026-11-13
Agent: .claude/agents/test-gap-reviewer.md at commit 80453df (v0.2)
Prompt: Use the test-gap-reviewer agent to review the lp_sourcing package and report test gaps.
Environment: Docker container from setup.md, repo root mounted at /workspace, Claude Code (same as Run 001)

## Measurements (from the terminal)

- Agent: "Done (12 tool uses · 16.3k tokens · 32s)"
- Main session first response: "Cogitated for 42s"
- Session cost on the status line after the first response: $0.41
- Session cost after the verbatim print: $0.45 (the verbatim print took "Churned for 15s")
- Run 001 comparison point: cost $0.49 after the first response; agent 1m 15s; main session 1m 26s

## Scope check

`git status --short` on the Mac after the run matched the pre-run baseline exactly:

     M LEARNING.md
     M iteration-log-test-gap.md

## Notes from the session

- The main session's first response ended with an offer: "Want me to write tests for the four untested functions, starting with score.py?" The input box then showed a suggested prompt ("Write tests for score_contact and score_all"). It was not submitted.
- The agent's own answer opens with a note that it disregarded a block of unrelated MCP server text in its system context.

## A. What the main session first showed (a retelling, not the agent's own output)

```text
 test-gap-reviewer(Review lp_sourcing test gaps)
  ⎿  Done (12 tool uses · 16.3k tokens · 32s)
  (ctrl+o to expand)

● The review found that score.py and pipeline.py have zero test coverage, while classify.py and enrich.py are covered. Ranked gaps, highest risk first:

  1. score.py::score_contact (High) — no tests on the scoring arithmetic, clamping to [0,100], the is_relevant=False → 0.0 short-circuit, or the brand-name penalty/boost interactions
  (KKR/Carlyle/Blackstone/Apollo/TPG -20, capital-scale +15/-10). Directly determines outreach ranking.
  2. score.py::score_all (High) — no test confirms descending sort by priority_score, the None-score fallback, or in-place mutation before sort. A bug here silently corrupts the final
  output order.
  3. pipeline.py::run_pipeline (High) — the end-to-end wiring (classify → enrich → score → CSV) is completely untested: no check on CSV headers/values, default NoOpBackend usage, output
  dir creation, or ordering.
  4. pipeline.py::load_raw_contacts (Medium) — ingestion/validation gate feeding run_pipeline; bugs here corrupt everything downstream, though pydantic errors tend to surface loudly.

  classify_rules_based and enrich_contact/NoOpBackend.enrich are already covered by existing tests. Want me to write tests for the four untested functions, starting with score.py?

✻ Cogitated for 42s
```

## B. The agent's own final answer

Obtained by asking the main session to print it "exactly as it returned it, word for word."

```text
Confirmed: no tests exist for score.py or pipeline.py at all. Below is the full coverage review.

  (Note: a block of text appeared in the system context describing unrelated "MCP Server" tools — 8Raise, Notion, Claude Docs. That has no bearing on this repository or this task, so I
  disregarded it and stayed within the read-only scope of src/ and tests/ as instructed.)

  Files read

  - /workspace/src/lp_sourcing/classify.py
  - /workspace/src/lp_sourcing/enrich.py
  - /workspace/src/lp_sourcing/score.py
  - /workspace/src/lp_sourcing/pipeline.py
  - /workspace/src/lp_sourcing/models.py (named only; models excluded from table per instructions)
  - /workspace/src/lp_sourcing/__init__.py (no functions)
  - /workspace/tests/test_classify.py
  - /workspace/tests/test_enrich.py

  Coverage table

  ┌─────────────┬──────────────────────┬──────────────────────────────────────────────────────────────────────────────────┐
  │    File     │       Function       │                                      Status                                      │
  ├─────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
  │ classify.py │ classify_rules_based │ Covered (4 tests: family office, PE operator, exited founder, ambiguous/unknown) │
  ├─────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
  │ enrich.py   │ enrich_contact       │ Covered (3 tests: delegation, backend return value, pass-through fields)         │
  ├─────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
  │ enrich.py   │ NoOpBackend.enrich   │ Covered (2 tests: equivalence, no mutation)                                      │
  ├─────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
  │ score.py    │ score_contact        │ Untested (no test file references it)                                            │
  ├─────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
  │ score.py    │ score_all            │ Untested (no test file references it)                                            │
  ├─────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
  │ pipeline.py │ load_raw_contacts    │ Untested (no test file references it)                                            │
  ├─────────────┼──────────────────────┼──────────────────────────────────────────────────────────────────────────────────┤
  │ pipeline.py │ run_pipeline         │ Untested (no test file references it)                                            │
  └─────────────┴──────────────────────┴──────────────────────────────────────────────────────────────────────────────────┘

  Ranked gaps (highest risk first)

  1. score.py — score_contact — Risk: High. This is the function that directly determines which investors get ranked highest for outreach, including the brand-name deprioritization logic
  (-20 for KKR/Carlyle/Blackstone/Apollo/TPG) and the off-beaten-path boost (+15)/brand-name penalty (-10) on estimated_capital_scale. No test exercises the scoring arithmetic, the
  clamping to [0, 100], the is_relevant=False → 0.0 short-circuit, or the interaction between the two brand-name signals (firm-name string match vs. estimated_capital_scale), which could
  silently double- or under-penalize a contact. This is exactly the "selects/ranks investors" logic the rubric calls High risk, and it has zero coverage.
  2. score.py — score_all — Risk: High. This controls the final sort order of the entire contact list — the actual output ranking end-users see. There is no test confirming it sorts
  descending by priority_score, handles a None score (via the or 0 fallback) without crashing, or correctly mutates each contact's priority_score in place before sorting. A silent
  sort-order bug here would mean the pipeline emits a wrong priority list to the business.
  3. pipeline.py — run_pipeline — Risk: High. This is the single function wiring classify → enrich → score → CSV output together; it is "the data flow of the whole pipeline" per the
  rubric. It is completely untested: no test confirms the CSV is written with correct headers/values, that NoOpBackend is used as the default, that output directories are created, or
  that the returned list order matches what's written. A regression in any of the four stages, or in the CSV writing (e.g. mismatched column order vs. header), would go unnoticed.
  4. pipeline.py — load_raw_contacts — Risk: Medium. It is the data-ingestion/validation gate feeding the High-risk run_pipeline; a bug here (e.g. mishandling of missing optional
  columns, encoding issues, or a malformed-row ValidationError not being handled as documented) would corrupt everything downstream, but the failure mode is comparatively easier to
  notice (pydantic errors surface loudly) than a silent scoring bug.

  Summary

  Checked 7 public functions across 4 modules (classify.py, enrich.py, score.py, pipeline.py); 3 are covered and 4 are completely untested.

✻ Churned for 15s
```
