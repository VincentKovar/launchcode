# LP Sourcing

Classifies, enriches, and prioritizes potential limited partners, family
offices, and exited executives as fundraising outreach targets for Thryve.

## Background

Thryve receives large, messy lists of family office and investor names from
multiple sources. Most of that volume is not useful: many entries are PE
funds that invest *in* operating companies (not a fit, since they don't have
the capability to invest in Thryve itself). The useful subset is capital
allocators: family offices, LPs, funds of funds, and executives/founders
with a prior exit who invest as individuals.

This tool takes a raw list, filters out the not-relevant PE-fund-as-operator
entries, classifies the rest by type, and scores them for outreach priority,
favoring smaller and less brand-name capital sources per current
fundraising strategy (brand-name LPs are easy to find but a tougher early
sell; less prominent allocators may be more receptive and have more
relative influence at this stage).

## Status

Early-stage / in development. This is the Target Codebase for an agentic
engineering course; features are being added and evaluated incrementally
rather than built out all at once.

## Stack

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) for dependency management
- pandas for tabular data handling
- Pydantic for data validation
- pytest for testing

## Setup

```bash
uv sync --extra dev
```

## Running the pipeline

```bash
uv run python -m lp_sourcing.pipeline
```

Or from Python:

```python
from pathlib import Path
from lp_sourcing.pipeline import run_pipeline

run_pipeline(Path("data/sample/sample_contacts.csv"), Path("output/scored.csv"))
```

## Testing

```bash
uv run pytest
```

## Linting

```bash
uv run ruff check src/ tests/
```

CI (`.github/workflows/ci.yml`) runs both lint and tests on every push
and pull request to `main`.

## Data handling

The `data/sample/` folder contains synthetic, fabricated contact data for
development and testing. Real contact lists are never committed to this
repository; they are kept locally in `data/raw/`, which is gitignored.
See `docs/sanitization.md` for the full policy.

## Project layout

```
src/lp_sourcing/
  models.py         Pydantic data models
  classify.py       Rules-based relevance classification
  enrich.py         Pluggable enrichment interface (web search default)
  score.py          Outreach priority scoring
  pipeline.py       End-to-end orchestration
tests/              pytest test suite
data/sample/        Synthetic sample data (safe to commit)
data/raw/           Real Thryve data (gitignored, local only)
docs/
  sanitization.md   Policy for handling real contact data
.github/workflows/
  ci.yml            Lint (ruff) + test (pytest) on push/PR to main
pyproject.toml       Project metadata, dependencies, ruff config
setup.md             Docker-based agent sandbox setup notes
Dockerfile,
docker-entrypoint.sh,
settings.json,
statusline.sh        Agent sandbox container config (see setup.md)
```
