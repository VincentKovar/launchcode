from lp_sourcing.classify import classify_rules_based
from lp_sourcing.models import ContactCategory, RawContact


def test_family_office_is_relevant():
    contact = RawContact(name="Jane Doe", firm="Doe Family Office", title="Principal")
    result = classify_rules_based(contact)
    assert result.is_relevant is True
    assert result.category == ContactCategory.FAMILY_OFFICE


def test_pe_fund_operator_is_not_relevant():
    contact = RawContact(name="John Smith", firm="Ridgeline Capital Partners", title="Managing Director")
    result = classify_rules_based(contact)
    assert result.is_relevant is False
    assert result.category == ContactCategory.PE_FUND_OPERATOR


def test_exited_founder_is_relevant():
    contact = RawContact(name="Ana Reyes", title="Former CEO", notes="Sold company in 2022, active angel investor")
    result = classify_rules_based(contact)
    assert result.is_relevant is True
    assert result.category == ContactCategory.EXITED_EXECUTIVE


def test_ambiguous_contact_is_unknown_not_falsely_relevant():
    """A silent misclassification (calling something relevant when it isn't)
    is worse than an honest 'unknown' that gets flagged for review.
    """
    contact = RawContact(name="Pat Lee", firm="Lee Holdings", title="Managing Partner")
    result = classify_rules_based(contact)
    assert result.category == ContactCategory.UNKNOWN
    assert result.is_relevant is False
