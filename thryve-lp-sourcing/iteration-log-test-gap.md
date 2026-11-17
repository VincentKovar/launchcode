# Iteration Log: Test-Gap Reviewer

- Agent definition: `.claude/agents/test-gap-reviewer.md`
- Rubric: `rubric-test-gap.md` (committed 57cfbe8, before the first run)
- Run 001 evidence: `run-001-report-test-gap.md`
- Run 002 evidence: `run-002-report-test-gap.md`
- Run 003 evidence: `run-003-report-test-gap.md`

## Runs

| Field | Run 001 | Run 002 | Run 003 |
|---|---|---|---|
| Date | 2026-11-12 | 2026-11-13 | 2026-11-17 |
| Agent version (commit SHA) | v0.1 (0c3470b) | v0.2 (80453df) | v0.3 (484e75e) |
| Prompt used | Use the test-gap-reviewer agent to review the lp_sourcing package and report test gaps. | Same | Same |
| Cycle time (main session / agent alone) | 1m 26s / 1m 15s | 42s / 32s | 1m 6s / 55s |
| Agent-run tokens | Not captured (background agent; completion line not saved) | 16.3k (12 tool uses) | 19.0k (15 tool uses) |
| Whole-session cost, status line after first response | About $0.49 | About $0.41 | About $0.45 |
| Whole-session cost, `/cost` | Not captured | Not captured | $0.4696 |
| Whole-session tokens, `/cost` | Not captured | Not captured | Sonnet: 112 in, 6.1k out, 140.2k cache read, 61.5k cache write. Haiku: 536 in, 17 out |
| Review latency | Not measured | Not measured | 16m 42s (stopwatch, paused by hand; upper bound) |
| Rubric: Finding Accuracy | 4 | 2 | 3 |
| Rubric: Risk Ranking and Evidence | 2 | 3 | 3 |
| Rubric: Scope Discipline | 4 | 4 | 4 |
| Rubric: Report Clarity | 3 | 3 | 1 |
| Average (of 4) | 3.25 | 3.0 | 2.75 |
| Pass/fail | Pass | Pass | **Fail** (Report Clarity scored 1, and the average is 2.75) |
| Misfires / observations | See Run 001 notes | See Run 002 notes | See Run 003 notes |

**Measurement limits.** I did not time review latency in Runs 001 and 002, and I am not estimating it after the fact. Run 003 is the first run where it was timed, with a stopwatch I paused by hand, so 16m 42s is an upper bound, and it was my first review of this kind. Whole-session costs for Runs 001 and 002 come from the status line after the first response, and they include the main session's retelling. Agent-run tokens come from the agent's completion line, which Run 001 did not save. For Run 003 I recorded agent-run and whole-session figures separately, and the whole-session figures come from `/cost`. The status line ($0.45) and `/cost` ($0.4696) were read at different moments, so I compare Run 003 to Run 002 using the status line only.

## Run 001 notes

**Score reasons**

- Finding Accuracy (4): All 7 functions in the agent's table exist, all 7 statuses are correct, and the agent noted without being asked that `_matches_any` is covered indirectly.
- Risk Ranking and Evidence (2): Items 1 to 5 each give a file, function, risk level, and a specific reason, and the order runs High to Medium. Item 6 fails the "every finding" test. It names no function, gives two risk levels ("Low/Medium"), says it is excluded from the ranking but sits inside it, and cites "priority_score bounds," which do not exist in `models.py`.
- Scope Discipline (4, changed from 3 on 2026-11-13): `git status --short` matched the pre-run baseline exactly, everything in the report came from `src/` and `tests/`, and the report opens with a "Scope reviewed:" line naming the files it read. I changed it from 3 so both runs are scored the same way.
- Report Clarity (3): The table, the ranked list, and the closing count line are each clearly separated. The ranked list is hard to scan, because each item is one long paragraph with file, function, and risk run together. Laying out file, function, and risk on separate lines with the comments below would make it easier to read. This is saved for a later version.

**Misfires and observations**

1. Item 6 of the ranked list reports models, not a function. The agent file says "If you cannot point to a real function in the code, do not report it," but never says what to do when the agent notices something about a class or model. This is the leading candidate for the v0.2 fix.
2. The agent ran in the background, and the main session retold its answer. The retelling dropped the function table and the closing count line. The agent's own answer had both.
3. Because the agent ran in the background, its tool calls were not visible. `git status` is the scope evidence.
4. A trial run on 2026-11-05 used the same agent and prompt (1m 4s, agent alone 53s; $0.48 for the session). Its report was not saved, so it was not scored. The 2026-11-12 run replaces it as Run 001.

## Run 002 notes

**Score reasons**

- Finding Accuracy (2): All 7 functions exist, but `classify_rules_based` is marked "Covered" when it is Partly covered. The LIMITED_PARTNER outcome has no test, and each of the other outcomes is tested through only one signal word. The agent also did not note indirect coverage this time.
- Risk Ranking and Evidence (3): All four items give a file, function, risk level, and specific reason, and the order is High, High, High, Medium. Items 1 and 2 tie their reasons to the outreach ranking. Items 3 and 4 do not, so it is not a 4.
- Scope Discipline (4): `git status --short` matched the baseline exactly. The report has a "Files read" list of eight files, all in `src/` and `tests/`.
- Report Clarity (3): The table, ranked list, and closing count line are separate. A note about unrelated MCP server text at the top is clutter, and each ranked item is still a long paragraph.

**Comparison with Run 001**

- Improved: Risk Ranking and Evidence, from 2 to 3. Item 6 is gone. The ranked list holds only functions from the table, and `models.py` appears only in the list of files read.
- Did not change: Scope Discipline (4 in both runs) and Report Clarity (3 in both runs).
- Regressed: Finding Accuracy, from 4 to 2. `classify_rules_based` flipped from Partly covered to Covered, and its High-risk gap disappeared from the ranked list.
- Averages: Run 001 is 3.25 and Run 002 is 3.0. The targeted dimension improved, but the regression elsewhere outweighed it.
- Time and cost were lower in Run 002 (32s agent time and about $0.41, versus 1m 15s and about $0.49). With one run each, I treat this as variation, not as an effect of the fix.

**Misfires and observations**

1. The agent file says "Mark each function as Covered, Partly covered, or Untested" but never defines the three statuses. This is the likely cause of the `classify_rules_based` flip. The v0.2 rule was about models, not statuses, so I judge it unlikely to be the cause. With one run each, I cannot prove that.
2. The main session's retelling dropped the function table and the closing count line again. It also ended with an offer to write tests, and the input box showed a suggested prompt. It was not submitted, and `git status` confirmed no files changed.
3. The agent opened with a note about unrelated MCP server text in its system context. This is clutter at the top of the report.
4. Line breaks in the copied report come from terminal wrapping.
5. Ideas for a later version: define the three statuses; put the scope statement under a fixed heading; tell the agent not to comment on its system context; lay out each ranked item with file, function, and risk on separate lines.

## Run 003 notes

**Score reasons**

- Finding Accuracy (3): All six functions the report names exist. I confirmed that by searching `src/lp_sourcing/` for `def` lines. The four it calls untested have no matches in `tests/`. `classify_rules_based` can return five categories and the tests check four, so Partly covered is correct, and the report names the missing outcome, `LIMITED_PARTNER`. The report labels `_matches_any` as covered indirectly, but v0.3 added a rule asking for that label, so it does not meet level 4's "without being asked." I first scored this a 4 and corrected it to 3 on 2026-11-17, after rereading level 4 against the v0.3 rule. The status that flipped to Covered in Run 002 is correct again.
- Risk Ranking and Evidence (3): Every item gives a file, function, risk level, and a specific reason, and the order runs High, High, Medium-High, Medium, Low. `Medium-High` is not a level the agent file defines. I scored it as a labeling slip, not an ordering error, and I record it as a watch item. I checked the base-score claim in item 4 against `score.py` lines 20 to 27, and it is true. It is not a 4, because items 3 and 5 do not tie their reasons to the ranking Will receives. The rubric has no level for "one undefined label," which is a gap in the rubric.
- Scope Discipline (4): `git status --short` matched the pre-run baseline, and `/cost` reported 0 lines changed. The "Files reviewed" line names eight files, all under `src/` and `tests/`.
- Report Clarity (1): The agent's answer has no coverage table and no closing function count. The "Files reviewed" line lists files, not a count. Level 1 lists "no table, no ranking, or no function count." The report is not a wall of text, and level 2 requires "the required parts," so neither level fits cleanly. I used the literal level 1 text.

**Comparison with Run 002**

- **Improved:** Finding Accuracy, from 2 to 3. `classify_rules_based` is Partly covered again, and the report names the missing `LIMITED_PARTNER` outcome. This is what v0.3 targeted.
- **Did not change:** Risk Ranking and Evidence (3 in both) and Scope Discipline (4 in both).
- **Regressed:** Report Clarity, from 3 to 1. The table and the closing count line were present in Run 002 and missing in Run 003.
- **Averages:** 3.0 in Run 002 and 2.75 in Run 003. Run 003 fails the pass rule on two counts: the average is below 3.0, and Report Clarity scored 1.
- **Time and cost:** All higher in Run 003: agent 55s versus 32s, 19.0k versus 16.3k tokens, about $0.45 versus $0.41 on the status line. With one run per version, I treat this as variation. The four failed Grep attempts may have added tool uses, but I do not know that.
- **Prediction versus result:** I predicted that `classify_rules_based` would be Partly covered with `LIMITED_PARTNER` named, that Finding Accuracy would return to 3 or higher, and that the other three scores would not drop. The first two held. The third did not, because Report Clarity dropped to 1.
- **What I cannot conclude:** Run 001 had no status definitions and still got `classify_rules_based` right. So I cannot say the definitions caused the correct status in Run 003, or that their absence caused the flip in Run 002. Three runs on three versions is too few to separate the fix from run-to-run variation.

**Misfires and observations**

1. **No coverage table and no closing count line.** The agent file's Output format asks for both. The task the main session handed the agent, which I can only read in a garbled copy, appears to ask only for "a ranked list with file paths and a brief rationale for each gap's risk level." My hypothesis is that the task text overrode the agent file's output format. This is one run, the copy is damaged, and I did not save the task text in Runs 001 and 002, so I cannot tell whether it changed.
2. **`Medium-High` label.** The agent file defines High, Medium, and Low but never says to use only those. Candidate for v0.4: "Use exactly one of High, Medium, or Low for each finding. Do not combine levels."
3. **`classify_rules_based` rated Medium.** In `score.py`, line 32 checks `is_relevant` and line 33 returns 0.0 when it is false. Line 35 takes the starting score from `contact.category`. Both values are set by `classify_rules_based`, so I judge High the better fit. Run 001 rated it High. Run 002 did not rank it at all, because it marked it Covered. Medium is arguable under the "transforms or validates data that feeds a High function" clause, and the report gave no reason for choosing it. I did not count this against the score.
4. **Four `EACCES ... 'rg'` errors.** The agent's Grep attempts failed with permission denied inside the container, and the agent read files directly instead. I do not know the cause, and I do not know whether Runs 001 and 002 had the same errors.
5. **Terminal copy damage.** Status lines overwrote parts of the copied text. The evidence file uses only the clean "Response:" block.
6. **Not seen this time.** The note about unrelated MCP server text, which opened the Run 002 answer, did not appear.
7. **Review latency.** This is the first run where I timed it. See the measurement limits note.

## Change between runs

**v0.1 to v0.2 (commit 80453df)**

- Problem: item 6 of the Run 001 ranked list reported pydantic models, not a function. It gave two risk levels, cited "priority_score bounds" that do not exist, and held Risk Ranking and Evidence at a 2.
- Root cause: the agent file says what to check (public functions) but never says what to do with other code, such as classes and data models. The agent invented a "supplementary" category.
- Fix (v0.2, commit 80453df): one rule added after the evidence rule. Classes and data models (such as those in models.py) are not functions, must not appear in the coverage table or the ranked list, and models.py may still be named among the files read.
- Run 001 record committed as ae64c63, before the fix.
- Prediction for Run 002: the ranked list contains only functions from the table, and Risk Ranking and Evidence rises to at least a 3.
- Regressions to watch: the scope line should still name the files read, the closing count line should still appear, and the other scores should not drop.

The v0.2 diff (commit 80453df):

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

This diff answers misfire 1 from Run 001. The commit message describes the rule but does not name the misfire, so this paragraph is the link between them.

**v0.2 to v0.3 (commit 484e75e)**

- Problem: In Run 002, the agent marked `classify_rules_based` Covered after finding four tests, but the `LIMITED_PARTNER` outcome had no test. Its high-risk gap dropped out of the ranked list, and Finding Accuracy fell from 4 to 2.
- Root cause (hypothesis): The agent file said "Mark each function as Covered, Partly covered, or Untested" but never defined the three statuses. The v0.2 rule was about models, so I judged it unlikely to be the cause.
- Fix: Added definitions for the three statuses, based on whether each distinct outcome is checked, and a rule to label indirect coverage. The commit message names the misfire: "define coverage statuses after Run 002 marked classify_rules_based Covered."
- Prediction (written in my fix plan on Nov 16, before Run 003): `classify_rules_based` is Partly covered with `LIMITED_PARTNER` named, Finding Accuracy returns to 3 or higher, and the other scores do not drop.
- Result: See "Comparison with Run 002." The first two parts held, and Report Clarity dropped to 1.

## Version history

Commits for this agent, oldest first. Commits unrelated to it are left out.

```
0c3470b 2026-11-05 feat: add test-gap-reviewer agent v0.1 (read-only)
57cfbe8 2026-11-05 docs: add test-gap-reviewer rubric before first run
055d7ac 2026-11-05 docs: add test-gap-reviewer iteration log template
ae64c63 2026-11-13 docs: record Run 001 evidence and scores for test-gap-reviewer v0.1
80453df 2026-11-13 feat: test-gap-reviewer agent v0.2 (keep classes and models out of findings)
635b4c3 2026-11-13 docs: record Run 002 evidence and compare v0.2 against v0.1
484e75e 2026-11-17 feat: test-gap-reviewer v0.3 (define coverage statuses after Run 002 marked classify_rules_based Covered)
9542ca9 2026-11-17 docs: record Run 003 evidence for test-gap-reviewer v0.3
```

The rubric was committed before any scored run. The Run 001 record (ae64c63) was committed before the v0.2 fix (80453df), and the Run 003 record (9542ca9) was committed after the v0.3 fix and before I edited this log.

## Before and after excerpts

**Model finding removed (v0.2).** Run 001, item 6 of the ranked list: "models.py field validation (RawContact, EnrichedContact) - Low/Medium risk, supplementary. These are pydantic models, not functions, so excluded from the main ranking, but note they have no dedicated validation tests..." Run 002: the ranked list has four items, all functions from the table. `models.py` appears only in the files-read list, marked "named only; models excluded from table per instructions."

**Status corrected (v0.3).** Run 002, table row: "classify_rules_based | Covered (4 tests: family office, PE operator, exited founder, ambiguous/unknown)". Run 003, item 4: "classify_rules_based (LIMITED_PARTNER branch) ... Partly covered ... the LIMITED_PARTNER outcome is never exercised."

**New regression (Run 003).** Run 002 ended with "Checked 7 public functions across 4 modules...", and had a coverage table. Run 003 has neither. It ends with a "Files reviewed:" list and a read-only statement.

## Known limitation

Grep checks names, not behavior. The agent has the same limit, because it also cannot run code. This is a built-in weakness of the read-only design.

## Appendix: rubric as committed in 57cfbe8, before Run 001

The rubric file is unchanged since that commit. `git diff 57cfbe8 HEAD -- rubric-test-gap.md` shows no differences.

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
