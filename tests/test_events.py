
from app.event_validator import validate_event


def test_valid_conversion_is_accepted():
    accepted, normalized, error = validate_event(
        "conversion",
        apply_fix=False
    )

    assert accepted is True
    assert normalized == "conversion"
    assert error is None


def test_purchase_is_normalized_after_fix():
    accepted, normalized, error = validate_event(
        "purchase",
        apply_fix=True
    )

    assert accepted is True
    assert normalized == "conversion"
    assert error is None


def test_unsupported_event_is_rejected():
    accepted, normalized, error = validate_event(
        "refund",
        apply_fix=True
    )

    assert accepted is False
    assert error == "Unsupported event type"
