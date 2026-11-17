"""Data models for the LP sourcing pipeline."""

from enum import Enum

from pydantic import BaseModel, Field


class ContactCategory(str, Enum):
    """What kind of capital source this contact represents."""

    FAMILY_OFFICE = "family_office"
    LIMITED_PARTNER = "limited_partner"
    EXITED_EXECUTIVE = "exited_executive"
    NOTABLE_INDIVIDUAL = "notable_individual"
    PE_FUND_OPERATOR = "pe_fund_operator"  # invests IN companies, not relevant as LP source
    UNKNOWN = "unknown"


class RawContact(BaseModel):
    """A single row as it arrives from an unprocessed source list."""

    name: str
    firm: str | None = None
    title: str | None = None
    source_list: str | None = None
    notes: str | None = None


class EnrichedContact(BaseModel):
    """A contact after enrichment and classification."""

    name: str
    firm: str | None = None
    title: str | None = None
    category: ContactCategory = ContactCategory.UNKNOWN
    is_relevant: bool = False
    relevance_reason: str | None = None
    estimated_capital_scale: str | None = Field(
        default=None,
        description="Rough sizing signal, e.g. 'brand-name' vs 'emerging/off-beaten-path'",
    )
    public_email: str | None = None
    source_urls: list[str] = Field(default_factory=list)
    priority_score: float | None = Field(
        default=None, description="0-100, higher favors smaller/off-beaten-path capital"
    )
