# Thryve LP Sourcing Tool: Rough PRD

## Origin

Will Corbett (Thryve acquisitions specialist) sent this request:

> "The brand name LPs are pretty easy to find and maybe a tough sell for us at the onset. I'm looking for off the beaten path investors as well that have smaller pockets of capital and can't always get into elite PE funds which are often oversubscribed. Also, they could have more influence with Thryve potentially than a KKR or Carlyle type."

Follow-up context from Will:

> "Would be great if it could ingest data. We have lists of names but could put them through AI and it could pull some quick intel, names, emails etc. I probably have a few thousand family office names but need to make some sense of the various lists and target the ones that are relevant which might only be 50-100."

## Problem

Will has several thousand family office and investor names across scattered lists. Manually sorting them for relevance and outreach priority is not feasible. Brand-name LPs (KKR, Carlyle, etc.) are easy to identify but a hard sell for Thryve at this stage, and they carry less relative influence than a smaller, less-visible investor might. The real target is under-the-radar capital: family offices and smaller investors who can't easily get into oversubscribed elite PE funds and may be more receptive to a stake in Thryve.

## Goal

Turn a raw list of a few thousand names into a short, prioritized list (roughly 50 to 100) of relevant, off-the-beaten-path investors worth outreach, with basic intel attached for each.

## Scope (three layers)

1. **Filtering/classification layer**
   Given raw name lists, classify who is actually relevant. Relevant means capital allocators who could invest *in* Thryve (LPs, family offices, individuals with exit liquidity). Not relevant means PE funds that invest *in* companies like Thryve (deal competitors, not capital sources).

2. **Enrichment layer**
   Take a bare name and pull basic intel: affiliation, role, public contact info, recent relevant news. Built as a pluggable interface.
   - Default/free backend: web search. Good for identity and affiliation, not reliable for direct email addresses (most aren't public; scraping or guessing emails raises deliverability and compliance concerns).
   - Future backend: a paid data API (Preqin, PitchBook, Crunchbase, Apollo.io) if Thryve licenses one later. Not assumed or built into v1.

3. **Prioritization layer**
   Down-select from a few thousand names to the 50 to 100 worth outreach, weighted toward smaller, off-the-beaten-path capital over brand-name LPs.

## Data sensitivity

Raw family office list data is real, Thryve-internal, and confidential. It needs sanitizing before anything touches GitHub. Real data stays local only; the public repo uses synthetic/sample data.

## Technical baseline (from sandboxing exercise)

- Docker-based sandbox, project root mounted read/write into the container at `/workspace`, nothing else from the host machine exposed.
- UV for dependency management: deterministic lockfile installs, single-command reproducibility (`uv sync`, `uv run`), plays well with repeated container rebuilds during agent sessions.
- Repo: `thryve-lp-sourcing`, local and GitHub.

## Open questions / not yet decided

- Exact scoring criteria for "off the beaten path" (fund size thresholds? existing PE fund access? geography?)
- Whether/when to bring in a paid enrichment API
- Output format for Will (spreadsheet? dashboard? digest?)
- How this intersects with the M&A Analyzer's existing scoring framework, if at all

## Course framing

Being built as the Target Codebase for the LaunchCode Agentic Engineering course. Course exercises (Docker sandboxing, parallel agent sessions, etc.) apply against this repo.
