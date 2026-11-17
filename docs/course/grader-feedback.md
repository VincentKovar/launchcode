# Past Grader Feedback (LaunchCode Agentic Engineering)

Student: Vincent Kovar
Grader: Hire Human Agentic Grader (posted by Christian Frauenhoffer's upload-only account)
All four reports below were posted Oct 31.

## Context

- Passing an assignment rubric requires a score of at least 3 on each criterion.
- Assignments are practice for the capstone. Passing the course means earning Proficient (3) or higher in every capstone rubric category.
- You do not need to pass every assignment to continue or to pass the course. Resubmission is allowed.
- Boilerplate notice text and the support-ticket instructions were left out of this doc. Support portal: https://launchcode.freshdesk.com/support/tickets/new (subject: "Agentic Grader Issues - Agentic Engineer").

## Score Overview

| # | Assignment (feedback title) | Posted | Criterion | Score |
|---|---|---|---|---|
| 1 | Establish an existing codebase and working automated check | 2:32pm | Workflow Scoping | 1/4 |
| 1 | | | Quality Spec and Baseline | 1/4 |
| 2 | Project-specific setup needs stronger boundary verification | 2:44pm | Sandboxed Environment | 2/4 |
| 2 | | | Governance, Security and CI/CD | 2/4 |
| 3 | Parallel-agent workflow feedback | 2:50pm | Sandboxed Environment | 3/4 |
| 3 | | | Workflow Scoping | 2/4 |
| 3 | | | Evaluation and Calibration | 3/4 |
| 3 | | | Iteration Narrative | 3/4 |
| 4 | Well-scoped workflow; run records need completion | 2:53pm | Workflow Scoping | 3/4 |
| 4 | | | Quality Spec and Baseline | 2/4 |
| 4 | | | Evaluation and Calibration | 1/4 |

Final scores: #1 = 2/8, #2 = 4/8, #3 = 11/16, #4 = 6/12. None met the passing threshold at Attempt 1.

Rubric criteria that recur across assignments: Workflow Scoping, Quality Spec and Baseline, Sandboxed Environment, Governance Security and CI/CD, Evaluation and Calibration, Iteration Narrative.

---

## 1. Establish an existing codebase and working automated check

Posted: Oct 31 at 2:32pm (no attempt number shown on this report)

### 1) Workflow Scoping: 1/4

**Why this score**
The response identifies TIE's acquisition-evaluation domain and describes its planned modules, but explicitly states that the implementation is not yet built. This matches the rubric's Beginning description: a planned project rather than an existing codebase for agents to inspect and modify. The three proposed improvements provide future directions, but do not establish an implemented target.

**Strengths**
- The project description explains the intended relationship between lead sourcing, scorecard evaluation, and portfolio-synergy simulation.
- Three future improvements are identified, including AI-assisted scoring for two named scorecard categories.

**Areas for improvement**
- Choose an existing implemented codebase, or first build a usable scorecard foundation. Update the description to identify its technology stack, current structure, and existing code an agent would need to understand before making changes.
- Bound each proposed improvement as a discrete task. For the simulation and data-enrichment features in particular, specify the inputs, expected outputs, and scope limits so completion can be evaluated without further clarification.

### 2) Quality Spec and Baseline: 1/4

**Why this score**
The response explicitly says that no testing currently exists and describes a test to be written later. Although it names pytest commands and explains the intended validation, the rubric requires an existing automated check; a planned check falls within the Beginning description.

**Strengths**
- The proposed test targets a concrete behavior: calculating the weighted composite from known category inputs.
- The response names pytest and python -m pytest and explains why scoring arithmetic matters to acquisition-threshold decisions.

**Areas for improvement**
- Implement the proposed automated test against a working scoring function and run it before presenting it as the codebase's quality gate.
- Update the response to identify the existing check, its exact run command, and what passing confirms. For a single known-input test, describe validation of that case rather than implying that it proves correctness for all scoring inputs.

**Final Score: 2/8**

**Rubric Result:** Does not yet meet the passing thresholds. At least 3 is needed on each criterion.

---

## 2. Project-specific setup needs stronger boundary verification

Posted: Oct 31 at 2:44pm (Attempt 1)

### 1) Sandboxed Environment: 2/4

**Why this score**
The Dockerfile is adapted to the project's Python and uv stack, and the runtime command mounts only the project folder plus a named authentication volume. However, setup.md explicitly documents unrestricted outbound access, includes no failed network-egress check, and summarizes the smoke test rather than providing its terminal output. The image also retains ngrok despite identifying no current project need for it. These are substantive gaps in the proficient sandboxing requirements.

**Strengths**
- The Dockerfile uses Python 3.12 and installs project dependencies with uv sync --extra dev using the project's dependency files.
- The documented run command maps the repository to /workspace without mounting the home directory or other broad host paths.
- The smoke-test prompt is bounded and project-specific: run the existing test suite and write a summary under /workspace.

**Areas for improvement**
- Constrain network egress for the sandboxed task, document the resulting runtime configuration, and paste an in-container curl check showing that the outbound request fails.
- Paste the actual smoke-test terminal output and host-side verification output showing that agent-summary.md persisted. Include evidence supporting the claim that task-related writes stayed within the intended project boundary; the current narrative checks do not establish the full claim.
- Remove ngrok from the image because the submission explicitly identifies it as unnecessary for the current project. Add it later only when a concrete task requires it.

### 2) Governance, Security and CI/CD: 2/4

**Why this score**
setup.md contains the build command, run command, mounted path, network mode, smoke-test prompt, and all six required reflection answers. The security reasoning is specific and distinguishes persistent from ephemeral storage. However, the required copy-pasted smoke-test output and network-egress check output are missing, leaving the documented verification incomplete.

**Strengths**
- The mount explanation names excluded sensitive host resources and explains how restricting access limits damage from accidental writes or deletion.
- The persistence answers distinguish the project mount and authentication volume from container-only scratch storage.
- The residual-risk answer identifies future confidential data under data/raw/ and proposes checking transmission boundaries before introducing real data, alongside tighter network scoping.

**Areas for improvement**
- Replace the prose-only smoke-test result with a copy-pasted transcript containing the executed test command, actual results, summary-file creation, and host-side persistence check.
- Add a network-egress verification section with the command and its actual output. Update the documented network mode to match the restricted configuration used for that verification, rather than leaving restriction as future work.

**Final Score: 4/8**

**Rubric Result:** Does not yet meet the passing thresholds. At least 3 is needed on each criterion.

---

## 3. Parallel-agent workflow feedback

Posted: Oct 31 at 2:50pm (Attempt 1)

### 1) Sandboxed Environment: 3/4

**Why this score**
The submitted log identifies separate feature branches and worktree directories, and the isolation notes describe each container mounting only its assigned worktree. Q2 provides additional separation checks: the new test file appeared only in Session A's worktree, while pipeline changes appeared only in Session B's. This supports the core isolation requirement. The reported Git-pointer problem required host-side commits but does not establish a failure of filesystem separation.

**Strengths**
- Separate worktree paths and feature branches are documented for both sessions.
- The reflection distinguishes filesystem isolation from the task-scoping decisions that prevent merge conflicts.

**To further improve**
- Include actual setup-verification output from git worktree list, branch checks, and ls /workspace in each container so the mount-to-branch mapping is directly inspectable.
- Explain which specific collision a shared working directory would have allowed, alongside the documented limitation of mounting only the worktree.

### 2) Workflow Scoping: 2/4

**Why this score**
The uploaded session_tasks.md contains precise, non-overlapping write paths, read-only boundaries, allowed commands, and task-specific definitions of done. However, Q2 and Q6 explicitly state that the original assignments used rough boundaries and lacked the complete scope contract before launch. The completed artifact therefore demonstrates a useful final specification, but not that these boundaries governed the sessions from the start. The required pre-worktree commitment of the scope contract is also not established.

**Strengths**
- The submitted file assigns Session A only tests/test_enrich.py and Session B only pipeline docstrings and README.md.
- Both definitions of done describe verifiable outputs, including passing enrichment tests and documentation changes without test-file edits.

**Areas for improvement**
- Establish the full write allow-list, read-only paths, allowed commands, and definition of done before either session begins, rather than completing the contract retrospectively.
- Document that session_tasks.md was committed on main before creating the worktrees. Preserve any original scope and later amendments so the results can be evaluated against the contract actually used.

### 3) Evaluation and Calibration: 3/4

**Why this score**
The results record a merge decision and specific rationale for each session, along with branch commit listings. Q1-Q3 address usefulness, assigned-file adherence, and merge readiness. Session A's rationale identifies five passing tests covering return values, non-mutation, and backend delegation; Session B's rationale identifies the functions documented and the README additions. These provide a substantive review rather than an unsupported approval. The acknowledged emphasis on file presence and separation, rather than closely validating assertions and documentation against implementation, limits the depth of the evaluation.

**Strengths**
- Both merge decisions are tied to named outputs and explicit scope checks.
- The results include commit identifiers and messages for both branches.
- The reflection candidly distinguishes the checks performed from the deeper content review that was not performed.

**To further improve**
- Record targeted findings from each branch's git status and git diff main review, including how the changed content satisfies its definition of done.
- For the tests, inspect representative assertions against the intended behavior; for the documentation, compare the behavioral claims with the function bodies. Connect those findings directly to the merge decisions.

### 4) Iteration Narrative: 3/4

**Why this score**
All six responses are complete and grounded in this run. Q4 identifies concrete human decisions involving placeholder filenames, inaccessible Git metadata, and merge tooling, with explanations of why the setup could not make those decisions. Q5 connects the conflict-free merges to the disjoint test-versus-documentation write scopes. Q6 proposes changes directly tied to observed problems: auditing real files before prompting, formalizing the scope contract, and addressing Git access. The reflection meets proficiency, but does not fully distinguish preventive file-level scoping from situations that still require a corrective prompt during execution.

**Strengths**
- The proposed upfront audit directly addresses the placeholder-filename mismatch encountered by both agents.
- The merge explanation attributes conflict avoidance to the specific file split rather than to worktree isolation alone.
- The reflection recognizes that successful agent behavior did not compensate structurally for an incomplete pre-run contract.

**To further improve**
- Explicitly separate what a stronger pre-run file contract would prevent from what would still require an in-session clarification or corrective prompt. Use the placeholder-target incident to illustrate the distinction.

**Final Score: 11/16**

**Rubric Result:** Does not yet meet the passing thresholds. At least 3 is needed on each criterion.

---

## 4. Well-scoped workflow; run records need completion

Posted: Oct 31 at 2:53pm (Attempt 1)

### 1) Workflow Scoping: 3/4

**Why this score**
The PRD defines a narrow single-agent lint-and-test reporting workflow tailored to thryve-lp-sourcing. It includes the workflow description, trigger, decision events, ordered actions, and falsifiable acceptance criteria covering command reporting, output accuracy, failure reporting, and file modification boundaries. It meets proficiency but does not justify this task over a concrete alternative as required for exemplary credit.

**Strengths**
- Names the exact commands, working directory, output file, and required summary structure.
- Defines observable checks, including matching counts against raw command output and comparing git status before and after the run.
- Distinguishes clean results, findings, test failures, and command execution errors.

**To further improve**
- Explain why this workflow was chosen over a concrete alternative, such as a broader code review, using repeatability or evaluability as the reason.
- Specify the overall status to report when either command cannot complete, resolving that edge case before scoring.

### 2) Quality Spec and Baseline: 2/4

**Why this score**
The rubric contains five task-specific dimensions, four scoring levels, examples, and an explicit pass threshold. However, the iteration log remains an unfilled template. Run 001 has no recorded measurements, scores, scoring notes, pass/fail result, or observations, so the required baseline measurement is missing.

**Strengths**
- The dimensions address command accuracy, result fidelity, file scope, error handling, and summary clarity.
- Examples describe relevant outcomes, such as fabricated passing results, missing failure names, unauthorized fixes, and accurate environment-error reporting.
- The log template includes the required measurement and evaluation fields.

**Areas for improvement**
- Complete Run 001 with its date, actual prompt, cycle time, review latency, and cost. Use explicitly labeled estimates where exact measurements are unavailable.
- Record all five rubric scores with brief evidence-based notes, the calculated result, and observations that interpret the baseline behavior.
- Clarify how Error Handling is scored when neither command errors, addressing the untested branch identified in Question 1.

### 3) Evaluation and Calibration: 1/4

**Why this score**
Both run sections contain placeholders rather than completed evaluation records. The reflections report a code-smell instruction change and two score movements, but neither log entry contains a completed rubric evaluation, and Run 002 contains no recorded change or outcome analysis. The partial written comparison does not replace the required two scored run records.

**Strengths**
- Question 2 identifies a specific prompt addition and reports a trade-off: File Scope Discipline increased from 3 to 4 while Summary Clarity decreased from 4 to 3.
- Question 1 recognizes that successful commands did not exercise error handling.
- Question 3 identifies accuracy and fidelity as consistent across the reported runs.

**Areas for improvement**
- Populate both run entries with the prompts used, all five scores with supporting notes, required measurements, and pass/fail decisions.
- In Run 002, record the exact single change and connect it to specific differences in the resulting summary or agent behavior.
- Explain which baseline observation motivated the code-smell instruction and whether the clarity-versus-scope trade-off supported that hypothesis. Bound the stability conclusion to what these two runs demonstrate.

**Final Score: 6/12**

**Rubric Result:** Does not yet meet the passing thresholds. At least 3 is needed on each criterion.
