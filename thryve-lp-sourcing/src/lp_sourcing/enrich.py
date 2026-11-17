"""Enrichment: given a bare name/firm, pull quick public intel.

Designed as a pluggable interface. The default backend uses web search
(free, public-source only). A paid data API (Apollo, PitchBook, etc.)
can be swapped in later by implementing the same EnrichmentBackend
protocol, without touching the pipeline code.
"""

from typing import Protocol

from lp_sourcing.models import EnrichedContact


class EnrichmentBackend(Protocol):
    """Any enrichment source must implement this."""

    def enrich(self, contact: EnrichedContact) -> EnrichedContact:
        """Return a new EnrichedContact with additional fields filled in."""
        ...


class NoOpBackend:
    """Default backend for local dev/testing. Does nothing.

    Swap this for a real backend (e.g. WebSearchBackend) in the pipeline
    once an enrichment source is wired up.
    """

    def enrich(self, contact: EnrichedContact) -> EnrichedContact:
        return contact


def enrich_contact(contact: EnrichedContact, backend: EnrichmentBackend) -> EnrichedContact:
    """Enrich a single contact using the given backend."""
    return backend.enrich(contact)
