"""End-to-end pipeline: raw CSV in, classified/scored CSV out."""

import csv
from pathlib import Path

from lp_sourcing.classify import classify_rules_based
from lp_sourcing.enrich import EnrichmentBackend, NoOpBackend, enrich_contact
from lp_sourcing.models import EnrichedContact, RawContact
from lp_sourcing.score import score_all


def load_raw_contacts(csv_path: Path) -> list[RawContact]:
    """Load a raw contact list from CSV into validated RawContact rows.

    Expects a header row with columns matching RawContact's fields
    (name, firm, title, source_list, notes); missing optional columns
    are fine, extra/malformed rows will raise a pydantic ValidationError.
    """
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [RawContact(**row) for row in reader]


def run_pipeline(
    input_csv: Path,
    output_csv: Path,
    backend: EnrichmentBackend | None = None,
) -> list[EnrichedContact]:
    """Run the full classify -> enrich -> score pipeline on a raw CSV.

    Loads contacts from `input_csv`, classifies them with the
    deterministic rules pass, enriches them via `backend` (defaults to
    NoOpBackend, i.e. no enrichment), scores and sorts them by outreach
    priority (highest first), and writes the result to `output_csv`
    (parent directories are created if needed).

    Returns the scored contacts in the same order written to the CSV.
    """
    backend = backend or NoOpBackend()

    raw_contacts = load_raw_contacts(input_csv)
    classified = [classify_rules_based(c) for c in raw_contacts]
    enriched = [enrich_contact(c, backend) for c in classified]
    scored = score_all(enriched)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["name", "firm", "title", "category", "is_relevant", "priority_score", "relevance_reason"]
        )
        for c in scored:
            writer.writerow(
                [c.name, c.firm, c.title, c.category.value, c.is_relevant, c.priority_score, c.relevance_reason]
            )

    return scored
