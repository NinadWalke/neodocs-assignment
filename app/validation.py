REQUIRED_FIELDS = {
    "test_id",
    "patient_id",
    "clinic_id",
    "test_type",
    "result",
}


def validate_test_payload(payload: dict) -> tuple[bool, str | None]:
    if not isinstance(payload, dict):
        return False, "Payload must be a JSON object"

    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        return False, f"Missing fields: {', '.join(sorted(missing))}"

    extra = payload.keys() - REQUIRED_FIELDS
    if extra:
        return False, f"Unexpected fields: {', '.join(sorted(extra))}"

    for key in REQUIRED_FIELDS:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            return False, f"Field '{key}' must be a non-empty string"

    return True, None
