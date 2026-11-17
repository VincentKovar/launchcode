# LEARNING.md

## 2026-10-20: Module 2 credential setup (LaunchCode Agentic Engineering)

**Status at end of session**

- [x] Google Cloud project created
- [x] OAuth client created (Desktop app, unchecked "AI agent" box; name: gmail-drive-client)
- [x] Downloaded JSON saved as `google_cred.json` in `~/Projects/thryve-lp-sourcing`
- [x] Slack app created (Blank app), bot token copied
- [x] Slack test channel created, bot invited
- [x] `SLACK_BOT_TOKEN` and `SLACK_TEAM_ID` added to `~/.zshrc` and verified with `set` checks
- [x] `.gitignore` covers `google_cred.json`, `credentials.json`, and `token.json`
- [x] `git status` shows only `.gitignore` changed; no credential files appear

**Still open**

- [ ] Confirm whether the Gmail MCP server expects `credentials.json` or `google_cred.json`
- [ ] Run the first Gmail action so the browser approval creates the token file
- [ ] Add the `docker run` mounts for `~/.gmail-mcp` and `claude-auth`
- [ ] Verify the container can read `/workspace/google_cred.json`

**Concepts I want to remember**

- Docker controls what the agent can see and change on my computer.
- Google Cloud controls what the agent can do inside my Google accounts. `google_cred.json` identifies the app but grants no access by itself; approval during sign-in does.
- `.gitignore` keeps secrets off GitHub. The project folder and mounts let the agent use them locally.
- Environment variables keep secrets out of the run command and out of the repo.

**Test credentials**

These are for a test project. When the experiment ends, follow the cleanup checklist (`cleanup-checklist.md`).

-----
## 2026-11-02: Module 2 setup finished, first agent run

**Status at end of session**

- [x] Google consent screen configured (External, Testing, my address as test user)
- [x] Gmail API and Drive API enabled
- [x] `google_cred.json` copied into `LaunchCodeAgenticEngineer/module_2`
- [x] Course repo `.gitignore` now lists `google_cred.json` and `token.json` (committed)
- [x] Built `agentic_engineer_2`; Dockerfile `COPY` lines name specific files only
- [x] Launched container; `SLACK_BOT_TOKEN` and `SLACK_TEAM_ID` both "set" inside
- [x] `google_cred.json` visible at `/workspace` inside the container
- [x] `code-reviewer.md` written to `.claude/agents/` and committed from the Mac
- [x] Ran code-reviewer on `sample_review.py`: 2 Critical, 6 Warning, 10 Suggestion
- [x] Confirmed with `git status` on the Mac that no files changed
- [x] `docker history` shows no credentials in the image

**Still open**

- [ ] First Gmail sign-in (creates the token in `~/.gmail-mcp`) not done yet
- [ ] 2 commits are on my Mac only, not pushed
- [ ] Optional: `docker history --no-trunc agentic_engineer_2 | grep -i -E "token|secret|cred"`
- [ ] Next lesson: Author Skills Using Tools and MCP Servers (build `/post-standup`)
- [ ] Cleanup checklist: `google_cred.json` now exists in two folders

**Where the lesson differed from my setup**

- `/agents` no longer opens the Library panel in current Claude Code; typing `@` shows the agent list instead
- Lesson path `/workspace/module_2/sample_review.py` is `/workspace/sample_review.py` for me, because I mount `module_2` itself
- Git does not work inside the container; commits happen in a Mac Terminal
- Claude Code starts in auto mode, so an agent's `permissionMode` line may be ignored
- Running `env` without `-e` hit an "unbound variable" error from the startup script, not the empty result the lesson predicted

**Concepts I want to remember**

- An agent's `tools` line is an access badge: only what the role needs
- `.gitignore` only guards Git. Docker does not read it, so check the Dockerfile `COPY` lines
- A secret in any image layer stays visible in `docker history`; rotate it first, investigate second
- An agent's claim that it changed no files is a report, so verify with `git status`
- Commit the `.gitignore` guard before the secret file exists

**To restart tomorrow**

1. In a Mac Terminal: `cd ~/Projects/LaunchCodeAgenticEngineer/module_2`
2. Run the lesson's `docker run` command (same as today)
3. Inside the container: `claude`

-----
## 2026-11-12: Test-gap reviewer re-run, Run 001 evidence saved (Exercise 2.1, Exercise 1)

**Status at end of session**

- [x] Chose the test-gap reviewer over the lint and test summary agent (it needs judgment, is evaluable, and needs only Read, Grep and Glob)
- [x] Agent definition (`.claude/agents/test-gap-reviewer.md`, commit 0c3470b), rubric (57cfbe8), and iteration log template (055d7ac) were all committed before the first run
- [x] The Nov 5 report was never saved, so I re-ran the same agent with the same prompt in the `thryve-lp-sourcing` container
- [x] Agent finished in 1m 15s; whole session 1m 26s; about $0.49
- [x] `git status --short` before and after the run showed the same three modified files, so the agent changed nothing
- [x] Saved the report as `run-001-report-test-gap.md` in the repo (not committed yet)
- [x] The agent's own answer had all three required parts: a table of 7 functions, a ranked gap list, and a closing count line
- [x] Checked with grep: no test mentions `score_contact`, `score_all`, `run_pipeline` or `load_raw_contacts`, so "Untested" is correct for all four
- [x] Checked with grep: `NoOpBackend.enrich` is called in `tests/test_enrich.py` at lines 17 and 24, so "Covered" is correct
- [x] Container stopped; `docker ps` shows nothing running

**Still open**

- [x] Checked `enrich_contact` (Covered) and `classify_rules_based` (Partly covered): both match the agent's table
- [ ] Score the remaining Run 001 rows: Scope Discipline (3 or 4?) and Report Clarity. Finding Accuracy and Risk Ranking are decided (see the progress note below)
- [ ] Decide which run is Run 001 of record (the Nov 12 re-run has saved evidence; the Nov 5 numbers have none)
- [ ] Pick ONE meaningful problem and its root cause. Candidates so far: the main session dropped the table and count when it retold the report; item 6 in the ranked list names no function, which breaks the agent's own evidence rule
- [ ] Fix it in the agent file (v0.2), commit, and record the SHA in the log
- [ ] Run 002, score it with the same rubric, and compare
- [ ] Write the four answers in my own words; upload the agent file and iteration log as Markdown
- [ ] Commit the pending files from the Mac
- [ ] Fix the typo in `.gitignore`: `.env` became `.envcd` (uncommitted; `.env` is still ignored by the `*.env` line)
- [ ] The container mounts the whole repo, so `google_cred.json` is visible inside it. Fine for a read-only agent, but worth remembering

**Concepts I want to remember (in plain words)**

- An agent definition is a job description plus an access badge: a role, the tools it may use, and the exact shape of the report it must return.
- The rubric is the grading sheet. I write it before the run so I can't bend the grading to fit the result.
- Evidence has to be saved. A run I can't reread can't be scored, and I can't learn from it.
- A background agent's answer may be retold by the main session, and the retelling can drop parts. Judge the agent by its own output, and ask for it word for word if needed.
- An empty grep result is an answer: no matches means no test mentions that name.
- A leading underscore marks a private helper. Classes are not functions. A search for lines that start with `def` cannot see methods inside classes.
- `git status` before and after is the proof of "changed no files." The agent's claim is only a report.
- The loop: run, score, find one problem, find its root cause, make one focused fix, rerun, compare.

**If I had to explain it back**

I built a read-only agent that finds code with no tests and ranks the gaps by risk. I wrote its instructions and grading sheet first, then ran it. It named real functions, got the coverage statuses right on every check so far, and changed no files. Next I score it, find one thing it did badly, fix that one thing in its instructions, and run it again to see if the scores improve.

**To restart**

1. Tell Claude: "pick up the test-gap exercise." It will redo the setup and give one small step at a time.
2. In a Mac Terminal: `cd ~/Projects/thryve-lp-sourcing` then `git status --short` to see where things stand.
3. No container is needed for scoring. The container is only needed for Run 002.

**Progress note, later on 2026-11-12**

- [x] Question 1 drafted (the four criteria applied to the test-gap reviewer)
- [x] Finding Accuracy scored 4 and entered in the log. Reason: all 7 functions are real, all 7 statuses are correct, and the agent noted without being asked that `_matches_any` is covered indirectly
- [x] Risk Ranking and Evidence scored 2 (not yet entered in the log). Reason: items 1 to 5 each have a file, function, risk level, and a specific reason, and the order follows High to Medium. Item 6 breaks the rubric's "every finding" test: it names no function, gives two risk levels ("Low/Medium"), says it is excluded from the ranking but sits inside it, and cites "priority_score bounds," which do not exist in `models.py` (the field has only a description)
- [ ] Enter the Risk Ranking score of 2 in `iteration-log-test-gap.md`
- [ ] The Run 001 column still has the Nov 5 date, time and cost. Update it to the Nov 12 re-run (1m 15s agent, 1m 26s session, about $0.49), since that run has the saved evidence
- [ ] Best candidate for Question 2 (the misfire): item 6. The agent file says "if you cannot point to a real function, do not report it" but never says what to do when it notices something about a class or model. A focused v0.2 fix would add that

**More concepts I want to remember**

- Finding Accuracy asks whether the agent's statements are true, not whether my code is well tested. "Untested" is a correct answer when no test exists.
- To score a row, start at level 1 and climb. One word can decide a level: "every" is what separates a 2 from a 3.
- Detail is not evidence. A long, well-written finding can still break the agent's own rules.

**How I work best (note to self, and to Claude)**

- Start with the big picture: what I am building, why, and where I am in the instructions.
- Show me the desired outputs (for this exercise, the four questions and the two uploads) before the steps, so I can see what the steps are for.
- Then give me one small step at a time, with a plain-English explanation before any command.
- Define each term the first time it appears.
- I draft in my own words first, then pressure-test.
- I am practicing moving from suspicion to evidence: check each claim against the rubric level or the code, and say why.

-----
## 2026-11-13: Run 002 done, v0.2 compared (Exercise 2.1, Exercise 1)

This note replaces the open lists in the entries above for the test-gap exercise.

**Done**

- [x] Scored Run 001 fully: Finding Accuracy 4, Risk Ranking and Evidence 2, Scope Discipline 4, Report Clarity 3 (average 3.25). I changed Scope from 3 to 4 so both runs are scored the same way
- [x] Root cause of the Run 001 problem: item 6 reported pydantic models as a finding. The agent file said what to check but not what to do with classes and models
- [x] Fix: one rule added to the agent file, committed as v0.2 (80453df). The Run 001 record was committed first (ae64c63)
- [x] Run 002 on v0.2: same prompt and container setup; `git status` matched the baseline, so the agent changed nothing
- [x] Run 002 scores: Finding Accuracy 2, Risk Ranking and Evidence 3, Scope Discipline 4, Report Clarity 3 (average 3.0)
- [x] Evidence saved in `run-002-report-test-gap.md`
- [x] Fixed the `.gitignore` typo (`.envcd` back to `.env`)
- [x] Drafted my answers to Questions 1 to 3

**Result in one line:** the fix worked on its target (Risk Ranking went from 2 to 3 and item 6 is gone), but Finding Accuracy fell from 4 to 2 because `classify_rules_based` was labeled Covered instead of Partly covered. The agent file never defines the three statuses, which is the likely cause. One run each cannot prove it.

**Still open**

- [ ] Draft Question 4: what improved, what did not, the regression, and the limits (one run each; the checks match names, not behavior)
- [ ] Upload the agent file and the iteration log as Markdown on the course page
- [ ] Optional stretch: one general principle for the log
- [ ] Ideas for a later version (not done): define Covered, Partly covered, and Untested; put the scope statement under a fixed heading; tell the agent not to comment on its system context; lay out each ranked item with file, function, and risk on separate lines
- [ ] Check whether the commits need to be pushed to GitHub (nothing was pushed from this repo today)
- [ ] The container mounts the whole repo, so `google_cred.json` is visible inside it (carried over)

**Concepts I want to remember**

- A fix can improve its target and still lose ground elsewhere. Check every row, not only the one I changed.
- With one run each, I can say what changed, not why. A vague instruction (undefined statuses) lets the answer vary between runs.
- The main session retells a background agent's work and can drop parts or offer to take actions. Check the scope with `git status`, not with what it says.
- Read a suggested prompt before accepting it. The main session can write files, but the read-only agent cannot.

**To restart**

Tell Claude: "pick up Question 4 of the test-gap exercise." Ask for the big picture first, then one small step.

-----
## 2026-11-14: Exercise 2.1, Exercise 1 submitted

- [x] Submitted my answers to Questions 1 to 4, the agent file (`.claude/agents/test-gap-reviewer.md`, v0.2), and the iteration log (`iteration-log-test-gap.md`)
- [x] Final result: the fix improved its target (Risk Ranking and Evidence, 2 to 3), but Finding Accuracy fell from 4 to 2 because the agent file never defines the three coverage statuses. Average 3.25 to 3.0. One run each, so I cannot prove the cause
- [ ] Not done: the optional stretch (one general principle from the loop) and a v0.3 (define the statuses, fixed scope heading, ranked-item layout)
- [ ] Not done: check whether the commits need to be pushed to GitHub

**Next**

- Add my past grader feedback to the Launchcode Class project, as a checklist of recurring patterns to apply to future work
- Add the capstone requirements to the project, so I know what I am working toward
- Do both in a new chat inside the project

**To restart**

Open a new chat in the Launchcode Class project and say: "I want to add my past grader feedback and the capstone requirements to this project." Ask for the big picture first, then one small step.
