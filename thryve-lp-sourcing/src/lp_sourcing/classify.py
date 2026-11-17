"""Classify raw contacts as relevant (capital sources for Thryve) or not
(PE funds that invest in operating companies, i.e. not a fit).

This module intentionally starts with a fast, deterministic rules pass
before any AI call. Cheap, explainable filtering first; expensive
judgment only where the rules genuinely can't tell.
"""

import re

from lp_sourcing.models import ContactCategory, EnrichedContact, RawContact

# Firm-name signals that suggest "invests IN companies" (not relevant as an LP source).
_PE_OPERATOR_SIGNALS = [
    r"\bcapital partners\b",
    r"\bbuyout\b",
    r"\bgrowth equity\b",
    r"\bprivate equity\b",
]

# Signals suggesting an LP-style capital allocator (relevant).
_LP_SIGNALS = [
    r"\bfamily office\b",
    r"\bfund of funds\b",
    r"\blimited partner\b",
    r"\bendowment\b",
    r"\bfoundation\b",
]

_TITLE_EXIT_SIGNALS = [
    r"\bfounder\b",
    r"\bformer ceo\b",
    r"\bex-ceo\b",
    r"\bretired\b",
]


def _matches_any(patterns: list[str], text: str) -> bool:
    text = text.lower()
    return any(re.search(p, text) for p in patterns)


def classify_rules_based(contact: RawContact) -> EnrichedContact:
    """First-pass deterministic classification. Leaves category UNKNOWN
    when the rules genuinely can't tell, so a downstream AI step can
    take over only for the ambiguous cases.
    """
    firm_text = contact.firm or ""
    title_text = contact.title or ""
    notes_text = contact.notes or ""
    combined = f"{firm_text} {title_text} {notes_text}"

    if _matches_any(_LP_SIGNALS, combined):
        return EnrichedContact(
            name=contact.name,
            firm=contact.firm,
            title=contact.title,
            category=ContactCategory.FAMILY_OFFICE
            if "family office" in combined.lower()
            else ContactCategory.LIMITED_PARTNER,
            is_relevant=True,
            relevance_reason="Matched LP/family-office/allocator signal in firm or notes.",
        )

    if _matches_any(_TITLE_EXIT_SIGNALS, title_text) or "exit" in notes_text.lower():
        return EnrichedContact(
            name=contact.name,
            firm=contact.firm,
            title=contact.title,
            category=ContactCategory.EXITED_EXECUTIVE,
            is_relevant=True,
            relevance_reason="Title or notes suggest a founder/executive with a prior exit.",
        )

    if _matches_any(_PE_OPERATOR_SIGNALS, combined):
        return EnrichedContact(
            name=contact.name,
            firm=contact.firm,
            title=contact.title,
            category=ContactCategory.PE_FUND_OPERATOR,
            is_relevant=False,
            relevance_reason="Firm name matches PE fund that invests in operating companies, "
            "not a capital source for Thryve.",
        )

    return EnrichedContact(
        name=contact.name,
        firm=contact.firm,
        title=contact.title,
        category=ContactCategory.UNKNOWN,
        is_relevant=False,
        relevance_reason="No rule matched; needs AI-assisted review.",
    )
