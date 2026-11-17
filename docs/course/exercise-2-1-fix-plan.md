# Exercise 2.1 Fix-Update Plan and Drafts (prepared Nov 16, 2026, for Nov 17)

## Big picture

Goal: lift "Agents, Skills and Memory" from 2 to 3. The other three criteria already score 3. Every change below is either a documentation fix or one small agent edit (v0.3) that gets measured in a new run (Run 003).

Rule for tomorrow: one change to the agent only (status definitions). Do not bundle the other ideas from the Run 002 notes, so any score change can be traced to that one edit.

## Order of work

1. Save `git status --short` as the pre-run baseline.
2. Edit the agent to v0.3 (wording in Part 1) and commit.
3. Run Run 003 with the three measurements (Part 2).
4. Update the log (Parts 3 to 6).
5. Final check: every grader "To further improve" bullet has a matching line in the log.

## Part 1: v0.3 wording (paste into `.claude/agents/test-gap-reviewer.md`)

Replace the process step "Mark each function as Covered, Partly covered, or Untested" with a reference to the definitions, and add this block after the Process list:

```
Coverage status definitions:
- Covered: a test calls the function and checks each distinct outcome it
  can produce (each return value, branch, or error path).
- Partly covered: a test calls the function, but at least one outcome is
  never checked. Example: a classifier with four categories where one
  category has no test. Name the missing outcome in the table.
- Untested: no test calls the function, directly or through another
  function.
If a function is exercised only through another function's test, add
"(indirect)" to its status and say which test reaches it.
```

Suggested commit message (names the misfire, as the grader asked):

```
feat: test-gap-reviewer v0.3 (define coverage statuses after Run 002 marked classify_rules_based Covered)
```

## Part 2: Run 003 measurement checklist

Same prompt as Runs 001 and 002: "Use the test-gap-reviewer agent to review the lp_sourcing package and report test gaps."

- Before: `git status --short` saved.
- Start a stopwatch when the report appears. Stop when I have checked every table row and ranked item against the code. That is review latency.
- Copy the agent completion line (looks like "Done (12 tool uses, 16.3k tokens, 32s)").
- Run `/cost` before exiting and copy the full output. This is the whole-session figure.
- After: `git status --short` saved.
- Prediction (written before the run): `classify_rules_based` is marked Partly covered with the LIMITED_PARTNER outcome named, Finding Accuracy returns to at least 3, and the other three scores do not drop.

## Part 3: Log table edits (Runs 001 and 002 columns, plus new Run 003 column)

| Field | Run 001 | Run 002 | Run 003 |
|---|---|---|---|
| Agent version | v0.1 (0c3470b) | v0.2 (80453df) | v0.3 (fill in SHA) |
| Agent-run time | 1m 15s | 32s | fill in |
| Agent-run tokens | Not captured (background agent; completion line not saved) | 16.3k tokens, 12 tool uses | fill in |
| Whole-session cost (status line, after first response) | About $0.49 | About $0.41 | fill in |
| Whole-session cost (after verbatim print) | Not captured | About $0.45 | fill in (`/cost`) |
| Whole-session token breakdown | Not captured | Not captured | fill in (`/cost`) |
| Review latency | Not measured | Not measured | fill in (timed) |

Add this note under the table:

> **Measurement limits.** I did not time review latency in Runs 001 and 002, and I am not estimating it after the fact. Run 003 is the first run where it was timed. Cost figures for Runs 001 and 002 are whole-session numbers read from the status line, and they include the main session's retelling and, in Run 002, the verbatim print. Agent-run tokens come from the agent's completion line, which Run 001 did not save. Run 003 records both agent-run and whole-session figures separately, and the whole-session figure comes from `/cost`.

## Part 4: Version history excerpt (paste as a code block)

From `git log --reverse --format='%h %ad %s' --date=short`, relevant lines only:

```
0c3470b 2026-11-05 feat: add test-gap-reviewer agent v0.1 (read-only)
57cfbe8 2026-11-05 docs: add test-gap-reviewer rubric before first run
055d7ac 2026-11-05 docs: add test-gap-reviewer iteration log template
ae64c63 2026-11-13 docs: record Run 001 evidence and scores for test-gap-reviewer v0.1
80453df 2026-11-13 feat: test-gap-reviewer agent v0.2 (keep classes and models out of findings)
635b4c3 2026-11-13 docs: record Run 002 evidence and compare v0.2 against v0.1
(add v0.3 and Run 003 commits here)
```

Sentence to add under it: "The rubric was committed before any scored run. The Run 001 record (ae64c63) was committed before the v0.2 fix (80453df), so the fix cannot have been shaped by Run 002 results."

Check tomorrow: the commit message for 80453df says what changed but does not name the misfire. I cannot rewrite it without changing pushed history, so the log explains the link instead (Part 5), and the v0.3 message names the misfire.

## Part 5: Focused diff for the v0.2 fix (paste as a diff block)

```diff
@@ -33,6 +33,10 @@ name, the risk level, and one or two sentences explaining why that
 function matters. If you cannot point to a real function in the code,
 do not report it.
 
+Classes and data models (such as those in models.py) are not functions.
+Do not include them in the coverage table or the ranked list. You may
+still name models.py among the files you read.
+
 Output format:
```

Sentence to add: "This diff is commit 80453df. It answers misfire 1 from Run 001 (item 6 of the ranked list reported pydantic models, not a function). The commit message describes the rule but does not name the misfire, so this paragraph is the link."

## Part 6: Before-and-after excerpts (short, from my own run reports)

**Misfire fixed: model finding in the ranked list**

Run 001, agent's answer, item 6:

> 6. models.py field validation (RawContact, EnrichedContact) - Low/Medium risk, supplementary. These are pydantic models, not functions, so excluded from the main ranking, but ...

Run 002, agent's answer: the ranked list has four items, all functions from the table. `models.py` appears only in the "Files read" list, marked "named only; models excluded from table per instructions."

**Regression: status flip**

Run 001, coverage table row: `classify_rules_based | Partly covered`, and ranked item 4 names the untested LIMITED_PARTNER branch.

Run 002, coverage table row: `classify.py | classify_rules_based | Covered (4 tests: family office, PE operator, exited founder, ambiguous/unknown)`. The LIMITED_PARTNER outcome is not among the four tests listed, so the status should have been Partly covered.

(Run 003 excerpt to add after the run.)

## Part 7: Rubric anchors for the Evaluation criterion

Paste the full text of `rubric-test-gap.md` (all four dimensions with levels 1 to 4) into the submitted log as an appendix titled "Rubric as committed in 57cfbe8 (before Run 001)". Do not edit the wording. If the log should stay short, paste only the score anchors and keep the dimension descriptions.

## Part 8: Run 003 comparison paragraph (fill in after the run)

> Run 003 tests the v0.3 change: [result for classify_rules_based status]. Finding Accuracy went from [x] to [y]. Risk Ranking and Evidence [held/changed]. Scope Discipline and Report Clarity [held/changed]. With three runs across three versions, I treat this as evidence for or against the status definitions, not as proof. If the flip to Covered recurs, the status definitions are not the cause, and the next suspect is how the agent counts tests (one test per signal word versus one per outcome).

## Part 9: Optional, not for tomorrow

Held back so Run 003 changes one thing: the scope-statement heading, the instruction to skip comments on unrelated system context, and the ranked-list layout with file, function, and risk on separate lines. These belong in v0.4.
