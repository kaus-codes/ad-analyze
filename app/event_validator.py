
VALID_EVENTS = {"impression", "click", "conversion"}

def normalize_event(event_name, apply_fix=False):
    if apply_fix and event_name == "purchase":
        return "conversion"

    return event_name

def validate_event(event_name, apply_fix=False):
    normalized = normalize_event(event_name, apply_fix)

    if normalized not in VALID_EVENTS:
        return False, normalized, "Unsupported event type"

    return True, normalized, None
