"""Priority scoring: rank relevant contacts for outreach.

Per stakeholder guidance, brand-name LPs are easy to find and a tougher
sell early on. This scorer favors smaller, less brand-name capital
sources that may have more appetite and more influence potential,
while still surfacing brand names lower in the list rather than
dropping them.
"""

from lp_sourcing.models import ContactCategory, EnrichedContact

_BRAND_NAME_FIRMS = {
    "kkr",
    "carlyle",
    "blackstone",
    "apollo global management",
    "tpg",
}

_CATEGORY_BASE_SCORE = {
    ContactCategory.FAMILY_OFFICE: 70,
    ContactCategory.LIMITED_PARTNER: 60,
    ContactCategory.EXITED_EXECUTIVE: 65,
    ContactCategory.NOTABLE_INDIVIDUAL: 55,
    ContactCategory.PE_FUND_OPERATOR: 0,
    ContactCategory.UNKNOWN: 10,
}


def score_contact(contact: EnrichedContact) -> float:
    """Return a 0-100 priority score. Higher = better outreach target."""
    if not contact.is_relevant:
        return 0.0

    score = _CATEGORY_BASE_SCORE.get(contact.category, 10)

    firm_lower = (contact.firm or "").lower()
    if any(brand in firm_lower for brand in _BRAND_NAME_FIRMS):
        score -= 20  # deprioritize, not exclude

    if contact.estimated_capital_scale == "off-beaten-path":
        score += 15
    elif contact.estimated_capital_scale == "brand-name":
        score -= 10

    return max(0.0, min(100.0, score))


def score_all(contacts: list[EnrichedContact]) -> list[EnrichedContact]:
    """Score and sort a list of contacts, highest priority first."""
    for c in contacts:
        c.priority_score = score_contact(c)
    return sorted(contacts, key=lambda c: c.priority_score or 0, reverse=True)
