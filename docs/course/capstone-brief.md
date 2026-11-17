# Capstone Project Brief: Ship Your Agentic Engineering Paved Road

Module: Capstone | Est. time: 23-29 hours | Type: Project Brief

Goal: Build and package a forkable, governed, multi-agent engineering pipeline that demonstrates measurable impact, safe boundaries, and right-tool engineering judgment. A reviewer should be able to evaluate it in five minutes and probe the engineering decisions in 30.

Passing the course requires Proficient (3) or higher in every capstone rubric category.

## Learning Goals

1. Design and justify a sandboxed, production-ready agentic environment: containerized harness with explicit filesystem, network, and credential boundaries, documented so a stranger can fork and run it.
2. Architect governed multi-agent systems: scoped context, tools, and permissions per agent and subagent role, with audit trails that hold up to scrutiny.
3. Apply right-tool reasoning: evaluate each step against agentic, deterministic, and human options and explain the trade-offs.
4. Measure and interpret impact: compare pre- and post-implementation results across quality, review latency, defect rate, cycle time, and cost, and explain what the numbers mean.
5. Translate technical design into stakeholder value: technical walkthrough and architecture write-up, impact report, ops-ready runbook (incidents, escalations, rollback), and a one-pager for a non-engineer.

## The Seven Workstreams (sequential by design)

Note from the brief: governance (4) only means something if orchestration (3) is solid, and the impact report (7) only holds up if the Module 1 baseline was set carefully.

### Workstream 1: Select Your Capstone Workflow and Evidence Path
- Choose a real or representative engineering workflow where agents can improve quality, reduce cycle time, or reduce review burden. Examples: PR review and release notes, dependency triage, test generation, ticket-to-implementation support, documentation refresh, codebase knowledge retrieval.
- Choose one delivery path: real deployment (real or sanitized internal data, with approvals) or job-seeker/no-deployment (public or representative dataset).
- Define the stakeholder, trigger, inputs, outputs, acceptance criteria, failure modes, and what the final demo must show.
- Inventory artifacts built in Modules 1-4 and mark gaps to fill.

### Workstream 2: Assemble the Forkable Enablement Repository
- Public or sanitized GitHub repo with a README that lets a stranger fork and run it in under 15 minutes.
- Include the Module 1 containerized agent harness, PRD, quality rubric, baseline measurements, and iteration log.
- Include versioned agents, at least two versioned skills, and a persistent memory layout from Module 2.
- Keep prompts, skills, tool contracts, memory rules, evaluation assets, governance policies, and config files versioned alongside the code.

### Workstream 3: Implement the Multi-Agent Pipeline
- An orchestrator agent delegates to scoped subagents (planner, implementer, reviewer, tester, project-manager or release-manager).
- Each subagent gets only the tools and context it needs. Do not expose every MCP tool globally.
- Stand up or configure MCP-backed persistent storage and vector retrieval tools, with schema definitions, classification tags, citation expectations, and traceability.
- Create a small ground-truth set for retrieval and a retrieval quality report showing the tool does not silently miss obvious results.

### Workstream 4: Add Evaluation, Calibration, and Governance Controls
- Build or refine a holdout-set evaluation harness combining deterministic checks with rubric-based scoring.
- Calibration log showing routing, prompt, subagent scope, and tool-grant changes made because of eval results or observed failures.
- Role-to-tool access matrix and governance policy with least-privilege defaults, justification-to-widen, and data classification boundaries.
- CI/CD guardrails: prompt, skill, tool-contract, and policy changes must pass the relevant eval or policy test before merging.

### Workstream 5: Right-Size Each Workflow Step
- Document whether each step belongs to an agent, deterministic code, or a human checkpoint.
- Find at least one stable agentic step predictable enough to convert into deterministic code, script logic, a database query, or traditional automation.
- Before/after evidence for the conversion: latency, cost, predictability, maintainability, audit clarity.
- Write an ADR capturing the decision, rejected alternatives, evidence from logs or evals, and consequences.

### Workstream 6: Run a Production-Like Integration and Impact Study
- Run the complete agent + deterministic + human workflow end-to-end on real, sanitized, public, or representative data.
- Add reliability and cost controls: timeouts, retries, fallbacks, rate limits, max-iteration guards, per-call budgets, per-workflow budgets.
- Run a tool-evolution drill: swap a model, change a tool interface, convert another step, or revoke a permission. Use the self-improving loop to document what broke, what improved, and how the eval harness caught regressions.
- Measure quality, review latency, defect rates, cycle time, and cost per run against the Module 1 baseline.

### Workstream 7: Package the Final Portfolio Submission
- Write the architecture narrative, impact report, ADR package, stakeholder one-pager, and ops-ready runbook.
- Record a 5-10 minute technical walkthrough video that runs the system end-to-end and shows governance stopping an over-reaching agent.
- Sanitize secrets, PII, customer data, internal URLs, proprietary identifiers, and logs.
- Submit all links and files in Canvas.

## Before You Begin (access needed)
- GitHub repository (public, private with reviewer access, or sanitized copy)
- Docker or devcontainer environment
- Agent runtime: Claude Code, OpenCode, or the course-approved runtime
- MCP tooling: at least one MCP-backed persistent storage tool and one agent-initiated vector retrieval tool, or approved sample equivalents
- Workflow data appropriate for the chosen path
- CI/CD environment (GitHub Actions, GitLab CI, or equivalent) for eval-gated checks and policy tests
- Baseline evidence: Module 1 PRD, quality rubric, first-run metrics, iteration log
- Recording tool with readable terminal, browser, or slides
- Approval and sanitization plan

## Project Requirements

Working evidence is required, not just descriptions. Screenshots and diagrams support the story, but the repo, logs, eval results, and demo must prove the system runs.

### Required Repository Contents
- **README and run path:** setup instructions, prerequisites, environment variables, example commands; completable by a stranger in under 15 minutes.
- **Containerized agent harness:** Dockerfile, devcontainer, docker-compose, or equivalent with explicit filesystem, network, and credential boundaries.
- **Module 1 evidence:** PRD, quality rubric with scoring guide and thresholds, baseline measurements, iteration log.
- **Module 2 evidence:** at least one versioned agent definition, at least two versioned skills, persistent memory layout, memory architecture notes, reflection log entries that led to concrete updates.
- **Module 3 evidence:** orchestration diagram, routing-and-tool-grant map, MCP configuration, schema definitions, vector retrieval quality report, evaluation harness, holdout set, calibration log.
- **Module 4 evidence:** governance policy, role-to-tool access matrix, CI/CD guardrails, audit log template, failure-mode playbook, agent-vs-deterministic-vs-human decision matrix, deterministic conversion, ADR.
- **Production-like integration:** end-to-end workflow combining agentic steps, deterministic steps, and human checkpoints, with monitoring, reliability controls, cost controls, and an incident runbook.
- **Sanitization:** no secrets, PII, customer data, proprietary credentials, or internal-only references unless approved and access-controlled.

### Delivery Path Requirements
- **Real-deployment path:** run on real or sanitized internal data, document approvals, document what was deployed or simulated, show how sensitive data was protected.
- **Job-seeker / no-deployment path:** run on a public or representative dataset, document constraints honestly, explain what would change in a real deployment.
- **Either path:** run the tool-evolution drill, produce the impact report, provide ADRs for durable decisions, demonstrate governance stopping an over-reaching agent.

### Evaluation and Impact Requirements
- **Baseline comparison:** compare post-capstone results against Module 1 baseline measurements.
- **Required metrics:** quality, review latency, defect rates, cycle time, cost per run. Use the best available proxy when a metric cannot be measured directly, and explain the proxy.
- **Evaluation harness:** deterministic checks, rubric-based scoring, holdout-set results, and a calibration log showing what changed because of the evidence.
- **Tool-evolution drill:** the change attempted, what broke, what improved, what the eval harness detected, what you fixed, the final result.
- **Run evidence:** logs, transcripts, commit history, eval outputs, or other artifacts connecting claims to actual runs.

### Architecture and Decision Requirements
- **Architecture write-up:** workflow, agent roles, deterministic steps, human checkpoints, data flow, MCP boundaries, storage, retrieval, CI/CD integration, governance enforcement.
- **ADRs** for: rubric design, memory layout, MCP boundaries, subagent scoping and routing, governance policy, and at least one agent-to-deterministic conversion.
- **ADR quality bar:** context, decision, rejected alternatives, evidence, consequences, open risks. At least one rejected alternative must cite concrete evidence from logs, evals, cost data, or calibration results.
- **Right-tool rationale:** for every major step, explain why it is agentic, deterministic, or human-reviewed.

### Governance and Safety Requirements
- **Least privilege:** each role gets only the tools, skills, data classifications, and autonomy level required.
- **Enforcement in code:** policies visible in config, MCP allow-lists, skill activation rules, CI/CD checks, or container permissions. A policy document alone is not enough.
- **Auditability:** log agent actions, tool calls, policy decisions, human approvals, failures, retries, rollbacks.
- **Escalation and rollback:** define when to stop, escalate to a human, revert a change, or fall back to deterministic behavior.
- **Security hygiene:** secrets handling, data classification, retrieval citations, schema validation, red-team or policy-bypass checks.

### Core and Stretch
- **Core:** provided templates, a representative dataset or sample MCP server if needed, one production-like integration, one deterministic conversion, one tool-evolution drill, a complete portfolio package.
- **Stretch:** approved internal data, custom MCP servers, a policy-test suite, a red-team prompt set, reviewer/tester-specific rubrics, richer monitoring, a higher-risk deterministic conversion with stricter SLAs.

## Presentation Requirements

5-10 minute technical walkthrough video (live repo demo, slide-supported demo, or both). Must work for a technical reviewer and still make the value clear to a non- or semi-technical manager.

- First minute: workflow, stakeholder, baseline problem, expected value.
- Show repo structure and the README path a stranger would follow.
- Demonstrate the containerized harness and run the multi-agent pipeline end-to-end.
- Show subagent delegation, scoped tool grants, MCP-backed storage or retrieval, and at least one evaluation result.
- Show the governance policy stopping a deliberately over-reaching agent or unauthorized tool/data request.
- Explain the agent-vs-deterministic-vs-human decision matrix and the deterministic conversion.
- Show baseline-vs-after impact metrics and the tool-evolution drill summary.
- Do not reveal secrets, private customer data, internal URLs, or proprietary details.

Suggested flow: Problem and value; Architecture; Live run; Governance; Evaluation; Right-tool decisions; Impact; Operations.

## Projected Timeline (23-29 hours)

| Phase | Focus | Hours |
|---|---|---|
| 1 | Scope and evidence inventory: choose workflow, stakeholder, path, dataset, acceptance criteria; review Modules 1-4 artifacts; confirm approvals and sanitization | 2-3 |
| 2 | Repository assembly and run instructions: README, harness, PRD, rubric, baseline, iteration log, agents, skills, memory, reproducible commands; verify a fresh clone runs | 4-5 |
| 3 | Multi-agent orchestration and MCP tools: delegation, routing, tool grants, storage, vector retrieval, ground-truth set, retrieval report, eval harness, calibration log | 5-6 |
| 4 | Governance, CI/CD, right-tool conversion: policy, role-to-tool matrix, audit logging, secrets handling, CI guardrails, overreach test, one deterministic conversion with before/after | 5-6 |
| 5 | Evaluation, impact report, tool-evolution drill: holdout eval, final metrics vs baseline, drill, impact report, ADR package, one-pager | 4-5 |
| 6 | Portfolio polish and submission: architecture write-up, runbook, README polish, sanitization review, video, Canvas submission, rubric self-check | 3-4 |

Plan for the upper range if this is a first significant automation project.

## Scoring Notes (from the brief)
Rubric has two sections: Project Evidence (what you build, why, whether it works, value created, and how clearly you present each element) and Presentation Quality (overall narrative structure and visual design).

- Evidence beats assertion: claims about quality, cost, speed, safety, or reliability must point to logs, eval results, metrics, commit history, or demo evidence.
- The repository must be runnable without reverse-engineering.
- Governance must be enforceable, connected to tool grants, containers, CI/CD checks, MCP allow-lists, skill rules, or audit logs.
- ADRs must show rejected alternatives and the evidence behind the final call.
- No-deployment projects can earn full credit with a representative dataset, transparent constraints, and an explanation of what changes in a real deployment.
- The one-pager and concise video are required, not optional.
- Sanitized evidence is acceptable when it preserves the engineering proof.

## Canvas Submission Checklist

Links (required):
1. GitHub repository link, plus reviewer access notes if private
2. Walkthrough video link, hosted outside Canvas (Google Drive, Dropbox, Loom, Vimeo, or unlisted YouTube). Must be viewable without requesting access; test in a private/incognito window. Do not upload the video file to Canvas. Include any password or access note with the link.

PDF uploads (one PDF each, required unless noted):
1. Architecture write-up
2. Impact report (baseline-vs-after metrics and tool-evolution drill summary)
3. Stakeholder one-pager (non-engineer audience)
4. Ops-ready runbook
5. ADR package
6. Rubric self-check (brief note mapping the submission to the Canvas rubric)
7. Sanitization or approval note (optional; for internal data, internal workflows, or redacted production-like evidence)

Also noted in the brief: upload the completed slide deck as a PDF, then submit.

## Reference Links
- Docker: https://docs.docker.com/
- Dev Containers: https://devcontainers.github.io/
- Claude Code: https://code.claude.com/docs/
- OpenCode: https://opencode.ai/docs/
- Model Context Protocol: https://modelcontextprotocol.io/docs/
- GitHub Actions: https://docs.github.com/actions
- ADR overview: https://adr.github.io/
- OWASP GenAI / LLM Top 10: https://genai.owasp.org/llm-top-10/
- Synthetic data for the no-deployment path: Faker (https://faker.readthedocs.io/), Mockaroo (https://mockaroo.com/), SDV (https://docs.sdv.dev/sdv), Hugging Face Datasets (https://huggingface.co/datasets)
- Presentation design: Presentation Zen (https://presentationzen.com/), Purdue OWL (https://owl.purdue.edu/)
