# launchcode

Backup of my LaunchCode Agentic Engineering coursework files. The target codebase for the course is `thryve-lp-sourcing`, which lives in its own repo. This repo holds the planning, measurement, and course documents.

Snapshot taken Nov 17, 2026, from the "Launchcode Class" Claude Project.

## Layout

| Path | What it is |
|---|---|
| `docs/thryve-lp-sourcing-PRD.md` | Rough PRD for the LP sourcing tool |
| `docs/prd.md` | PRD for the single-agent lint and test summary workflow |
| `docs/rubric.md` | Scoring rubric for that workflow |
| `docs/iteration-log.md` | Runs, re-measurements, incident, and calibration |
| `docs/session_tasks.md` | Parallel agent session scope contracts and results |
| `docs/cleanup-checklist.md` | Steps to remove test credentials when done |
| `docs/course/capstone-brief.md` | Capstone project brief |
| `docs/course/grader-feedback.md` | Grader feedback from the Oct 31 submissions |
| `docs/course/exercise-2-1-fix-plan.md` | Plan and drafts for the Exercise 2.1 fix (Run 003) |
| `docs/course/1.1-optional-reflection-sandbox.md` | Optional sandbox reflection prompts |
| `docs/archive/iteration-log-aug-original.md` | Original August iteration log (superseded) |

## thryve-lp-sourcing/

Snapshot of the target codebase from the Mac project folder: the `test-gap-reviewer` agent (`.claude/agents/`), its rubric, iteration log and run reports (`rubric-test-gap.md`, `iteration-log-test-gap.md`, `run-00N-report-test-gap.md`), the lint and test workflow docs, Dockerfile, CI, source and tests. The live repo is VincentKovar/thryve-lp-sourcing.

## Not included

Credentials (`google_cred.json`, Slack token), raw Thryve data, outputs, `.venv` and caches. The root `.gitignore` blocks them.
