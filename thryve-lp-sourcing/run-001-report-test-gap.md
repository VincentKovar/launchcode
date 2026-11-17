# Run 001 Evidence: Test-Gap Reviewer

Captured: 2026-11-12 (re-run; the 2026-11-05 report was not saved)
Agent: .claude/agents/test-gap-reviewer.md at commit 0c3470b
Prompt: Use the test-gap-reviewer agent to review the lp_sourcing package and report test gaps.
Environment: Docker container from setup.md, repo root mounted at /workspace, Claude Code in manual mode

## Measurements (from the terminal)

- Agent time: 1m 15s (shown as "Agent ... finished")
- Main session: "Worked for 1m 26s"
- Session cost on the status line after the first report: $0.49
- Agent ran as a background agent; the main session retold its result

## Scope check

`git status --short` on the Mac after the run matched the pre-run baseline exactly:

     M .gitignore
     M LEARNING.md
     M iteration-log-test-gap.md

## A. What the main session first showed (a retelling, not the agent's own output)

This version has no function table and no closing count line.

```text
lp_sourcing Test Gap Review

The test-gap-reviewer agent found no tests for score.py or pipeline.py, plus several untested branches in classify.py. Ranked by risk:

1. score_contact (score.py:30) - High risk, zero tests. Implements the core ranking logic (brand-name penalties, capital-scale boosts, clamping). A sign/logic error would silently misrank every investor.
2. score_all (score.py:49) - High risk, zero tests. Sorts the entire outreach list; a reversed sort or bad key would flip priority order with nothing to catch it.
3. run_pipeline (pipeline.py:24) - High risk, zero tests. End-to-end classify->enrich->score->write flow that produces the actual output CSV; a wiring bug would corrupt deliverables undetected.
4. classify_rules_based (classify.py:43) - High risk, partially tested. The LIMITED_PARTNER branch and most PE-operator/exit-title signal variants ("buyout", "private equity", "founder", "ex-ceo", "retired", standalone "exit") are never exercised, even though this gates whether a contact is scored at all.
5. load_raw_contacts (pipeline.py:12) - Medium risk. CSV parsing and the documented malformed-row ValidationError path are untested.
6. models.py field validation - Low/Medium, supplementary. Pydantic models have no dedicated validation tests (e.g., priority_score bounds, source_urls defaults).

Top priority: write tests for score.py and pipeline.py first - they currently have zero coverage and sit directly on the output path.
```

## B. The agent's own final answer

Obtained by asking the main session to print it "exactly as it returned it, word for word." Copied from the terminal; table borders come from terminal formatting.

```text
Test Coverage Review: lp_sourcing

Scope reviewed: /workspace/src/lp_sourcing/{classify.py, enrich.py, score.py, models.py, pipeline.py, __init__.py} against /workspace/tests/{test_classify.py, test_enrich.py}. No test_score.py, test_pipeline.py, or test_models.py exist.

Coverage table (public functions)

+--------------------------------+----------------------+----------------+
|              File              |       Function       |     Status     |
+--------------------------------+----------------------+----------------+
| src/lp_sourcing/classify.py:43 | classify_rules_based | Partly covered |
| src/lp_sourcing/enrich.py:29   | NoOpBackend.enrich   | Covered        |
| src/lp_sourcing/enrich.py:33   | enrich_contact       | Covered        |
| src/lp_sourcing/score.py:30    | score_contact        | Untested       |
| src/lp_sourcing/score.py:49    | score_all            | Untested       |
| src/lp_sourcing/pipeline.py:12 | load_raw_contacts    | Untested       |
| src/lp_sourcing/pipeline.py:24 | run_pipeline         | Untested       |
+--------------------------------+----------------------+----------------+

(classify.py:38 _matches_any is a private helper, exercised indirectly by every test_classify.py case - not a gap worth separate ranking.)

Ranked gaps, highest risk first

1. score_contact - src/lp_sourcing/score.py:30 - High risk. No test file exists for score.py at all. This function implements the core stakeholder-driven ranking rule described in the module docstring (deprioritize brand-name firms like KKR/Carlyle/Blackstone, boost "off-beaten-path" capital scale, zero out non-relevant contacts) and directly produces the priority_score that determines outreach order. A sign error in the brand-name penalty (line 38-39) or the capital-scale adjustment (line 41-44), or a clamping bug (line 46), would silently misrank every investor with nothing to catch it.
2. score_all - src/lp_sourcing/score.py:49 - High risk. Also fully untested. It mutates priority_score on each contact and sorts the whole list (reverse=True, key=lambda c: c.priority_score or 0). A reversed sort, wrong key, or None-handling bug would flip the entire outreach list without any test noticing - this is literally "which investors are ranked" per the task's own High-risk definition.
3. run_pipeline - src/lp_sourcing/pipeline.py:24 - High risk. No test exercises the end-to-end classify -> enrich -> score -> write flow. It is the single function that controls the whole pipeline's data flow and produces the actual deliverable (the output CSV, written at lines 46-55). A wiring bug - e.g., writing c.category.value for the wrong row, skipping enrich_contact, or not actually using the sorted order from score_all - would corrupt the business output with zero coverage to catch it.
4. classify_rules_based untested branches - src/lp_sourcing/classify.py:43 - High risk. Covered only for: family-office LP signal, one PE-operator pattern ("capital partners"), one exit-title pattern ("former ceo"), and the UNKNOWN fallback. Untested:
   - The LIMITED_PARTNER category branch (line 58-60 ternary) - no test exercises "fund of funds", "limited partner", "endowment", or "foundation" signals (classify.py:24-27), nor confirms the ternary falls through to LIMITED_PARTNER when "family office" is absent.
   - Three of four PE-operator signals - "buyout", "growth equity", "private equity" (classify.py:16-18) are never triggered by a test.
   - Three of four exit-title signals - "founder", "ex-ceo", "retired" (classify.py:31,33,34), and the standalone "exit" in notes_text branch (line 65) independent of a title match.
   Because is_relevant/category gate whether a contact is scored at all (vs. forced to 0 in score_contact), a bug in any of these regexes would directly change which investors are selected or excluded - the exact failure mode the test suite's own test_ambiguous_contact_is_unknown_not_falsely_relevant docstring calls out as worst-case, yet most signal variants are unverified.
5. load_raw_contacts - src/lp_sourcing/pipeline.py:12 - Medium risk. Feeds the High-risk run_pipeline. The docstring asserts "missing optional columns are fine, extra/malformed rows will raise a pydantic ValidationError," but no test verifies CSV parsing, missing-column handling, or the malformed-row error path. A silent parsing issue here would propagate bad or missing data into classification and scoring.
6. models.py field validation (RawContact, EnrichedContact) - Low/Medium risk, supplementary. These are pydantic models, not functions, so excluded from the main ranking, but note they have no dedicated validation tests (e.g., priority_score bounds, source_urls default factory behavior). Low risk on their own since pydantic itself enforces most structure, but worth flagging since pipeline.py's correctness claims about them are unverified.

Checked 7 public functions across 5 source modules against 2 test files.
```
