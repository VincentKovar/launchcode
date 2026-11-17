from lp_sourcing.enrich import NoOpBackend, enrich_contact
from lp_sourcing.models import ContactCategory, EnrichedContact


def _sample_contact() -> EnrichedContact:
    return EnrichedContact(
        name="Jane Doe",
        firm="Doe Family Office",
        title="Principal",
        category=ContactCategory.FAMILY_OFFICE,
        is_relevant=True,
    )


def test_noop_backend_returns_equivalent_contact():
    contact = _sample_contact()
    result = NoOpBackend().enrich(contact)
    assert result == contact


def test_noop_backend_does_not_mutate_input():
    contact = _sample_contact()
    original = contact.model_copy()
    NoOpBackend().enrich(contact)
    assert contact == original


def test_enrich_contact_delegates_to_backend():
    contact = _sample_contact()
    result = enrich_contact(contact, NoOpBackend())
    assert result == contact


def test_enrich_contact_uses_backend_return_value():
    class UppercaseNameBackend:
        def enrich(self, contact: EnrichedContact) -> EnrichedContact:
            return contact.model_copy(update={"name": contact.name.upper()})

    contact = _sample_contact()
    result = enrich_contact(contact, UppercaseNameBackend())
    assert result.name == "JANE DOE"
    assert result is not contact


def test_enrich_contact_passes_through_backend_fields():
    class FixedEmailBackend:
        def enrich(self, contact: EnrichedContact) -> EnrichedContact:
            return contact.model_copy(update={"public_email": "jane@example.com"})

    contact = _sample_contact()
    result = enrich_contact(contact, FixedEmailBackend())
    assert result.public_email == "jane@example.com"
    assert result.name == contact.name
