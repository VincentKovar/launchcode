# Agent Sandbox Setup

This note documents the Docker-based sandbox used to run coding agents
(Claude Code, OpenCode) against this repository. It is the baseline
container configuration for the rest of the LaunchCode Agentic Engineer
course, including running parallel agent sessions in later lessons.

## Source

The Dockerfile is adapted from the course starter at
`module_1/Dockerfile` in
[LaunchCodeEducation/LaunchCodeAgenticEngineer](https://github.com/LaunchCodeEducation/LaunchCodeAgenticEngineer).
`settings.json`, `statusline.sh`, and `docker-entrypoint.sh` are copied
unchanged from the same source. The only functional change from the
course starter is the dependency install step: this project uses `uv`
and `pyproject.toml`/`uv.lock`, not `pip` and `requirements.txt`.

## Build command

```bash
docker build -t thryve-lp-sourcing .
```

## Run command

```bash
docker run -it --rm \
  -v "$(pwd)":/workspace \
  -v claude-auth:/claude-auth \
  --name thryve-agent \
  thryve-lp-sourcing
```

- Mounted path: the project root only (`$(pwd)`, i.e. this repository),
  mapped to `/workspace` inside the container.
- Network mode: default Docker bridge network (container has outbound
  internet access for package installs and, later, enrichment API
  calls; no inbound ports are published).
- `claude-auth` is a separate named Docker volume used only to persist
  the Claude Code login credential between container runs. It holds no
  project data.

## Smoke test

**Prompt given to the agent (inside the running container, via `claude`):**

> Run the project's test suite with `uv run pytest -v`, then write a
> short summary of the results to `/workspace/agent-summary.md`,
> including how many tests passed and what each one verifies.

**Result:** the agent ran `uv sync --extra dev` (to install the `dev`
extra containing pytest, since it isn't installed by default), then
`uv run pytest -v`. All 4 tests passed. The agent wrote
`agent-summary.md` to `/workspace`, which appeared on the host machine
at the repository root immediately after, confirming the mount is
live and bidirectional for this one folder.

Verified boundary checks performed from inside the container:

- `ls /workspace` showed the real project files (src, tests, README,
  Dockerfile, etc.)
- `ls /` showed a minimal container filesystem with no host-specific
  folders
- `ls /Users` failed with "no such file or directory," confirming the
  Mac home directory (and everything in it: other projects, SSH keys,
  personal files) is not visible inside the container
- `agent-summary.md`, written by the agent inside the container, was
  confirmed present and readable on the host Mac immediately after,
  via a separate host-side terminal session

## Security decisions

**1. Why did you mount only this folder?**

The project has no dependency on anything else on the host machine.
Mounting only the project root, rather than the home directory or a
broader parent folder, means a mistake by the agent (a bad file write,
an accidental delete, a runaway script) can only affect this project,
not other work, personal files, SSH keys, or credentials stored
elsewhere on the Mac.

**2. What did you choose to keep ephemeral?**

Everything inside the container's own filesystem outside `/workspace`
and `/claude-auth`: the installed Python virtual environment build
artifacts, apt package caches, and any scratch files the agent might
create in `/tmp`. None of this is meaningful to persist; rebuilding
the image recreates it identically.

**3. What did you choose to persist?**

Two things, and only two: the project folder itself (via the
`/workspace` mount, so source code, tests, and any files the agent
writes survive container restarts) and the Claude Code login
credential (via the `claude-auth` named volume, so re-authenticating
isn't required on every run). Nothing else persists.

**4. What dependencies did you include in your extended Docker image?**

- Python 3.12 (base image)
- `uv` (this project's package manager)
- Project dependencies from `pyproject.toml`/`uv.lock`: pandas, pydantic,
  anthropic SDK, python-dotenv, plus dev tools pytest and ruff
- Node.js/npm, needed only to install the agent tooling itself
  (`@anthropic-ai/claude-code`, `opencode-ai`), not by the project code
- git, curl, bash, nano, procps, ca-certificates (general dev
  utilities from the course starter)
- ngrok (kept from the course starter for possible future use; not
  currently required by this project, which runs no server)

No API keys or credentials are baked into the image. The project's
`ANTHROPIC_API_KEY` (needed once real enrichment is built) will be
supplied at container run time via an environment variable or `.env`
file, never committed to the image or the repository.

**5. What did your smoke test prove?**

That the agent, running entirely inside the sandbox, can install
project dependencies, execute the project's real test command, read
and correctly summarize the results, and write a file back to the
mounted project folder, all without any access to the host machine
beyond that one folder. It also incidentally confirmed the
classifier's core safety property still holds: ambiguous contacts fall
back to "unknown" rather than being guessed as relevant.

**6. What risks remain?**

- The image installs ngrok even though it isn't used yet; if a future
  exercise activates it, that will need its own filesystem/network
  review at that time.
- No real enrichment or network-calling code exists yet. When it's
  built, the container's network access will need to be scoped more
  tightly than the current default bridge mode (e.g. restricted to
  only the Anthropic API and any search API domains), rather than
  open outbound internet access.
- `data/raw/`, where real confidential Thryve contact data will
  eventually live, is currently empty and gitignored, but has not yet
  been tested with the container mounted while real data is present.
  Before loading real data, re-verify that no agent action can copy or
  transmit that folder's contents outside `/workspace` (e.g. via a
  future network-enabled enrichment step).
- The container runs as root inside itself. This is standard for the
  course starter but is worth revisiting later in the course if
  stricter privilege separation becomes relevant.

These answers are provisional for the first setup of this sandbox and
are expected to evolve as the project and course progress.
