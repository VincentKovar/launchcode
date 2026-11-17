# Sanitization Policy

This project works with real Thryve fundraising target data (family
office names, executive names, firm affiliations, and eventually contact
details). That data is confidential and must never reach this public/
shared repository.

## What is excluded from the repository

- **Raw contact lists**: anything under `data/raw/` is gitignored. This
  is where real Thryve source lists live locally.
- **Enriched output containing real names/emails**: anything under
  `output/` or matching `*.output.csv` is gitignored.
- **API keys and credentials**: `.env` files are gitignored. Credentials
  are read from environment variables at runtime, never hardcoded.
- **Internal identifiers**: no internal Thryve project codes, deal
  names, or CRM references appear in code, comments, or commit
  messages.

## What is included instead

- `data/sample/sample_contacts.csv`: fully fabricated names, firms, and
  titles, structured the same way the real data is, safe to commit and
  safe for anyone to clone and run against.

## Verification before every commit

Before committing, confirm:

1. `git status` shows nothing under `data/raw/` or `output/` staged.
2. No API keys appear in any staged file (`git diff --staged` review).
3. Any new sample/test data is fabricated, not copied from a real list.

## Rotation note

If a credential is ever accidentally committed, it must be rotated
immediately, not just removed from the file. Removing it from a future
commit does not remove it from git history.
