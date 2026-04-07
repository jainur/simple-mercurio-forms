from __future__ import annotations

from typing import Any, Mapping


def coerce_str(value: Any) -> str:
    """Convert None to empty string and preserve textual values for PDF fields."""
    return "" if value is None else str(value)


def split_nie(value: str | None) -> tuple[str, str, str]:
    """Split NIE/NIF-like identifiers into (prefix, body, suffix) segments."""
    if not value:
        return "", "", ""

    normalized = "".join(ch for ch in str(value).strip().upper() if ch not in {" ", "-"})
    if not normalized:
        return "", "", ""

    if len(normalized) == 1:
        return normalized, "", ""

    if len(normalized) == 2:
        return normalized[0], "", normalized[1]

    return normalized[0], normalized[1:-1], normalized[-1]


def assign_checkboxes(
    field_values: dict[str, Any],
    selected_value: Any,
    checkbox_map: Mapping[str, Any],
) -> None:
    """Set each checkbox key to True only when selected_value matches its expected value."""
    for field_name, expected_value in checkbox_map.items():
        field_values[field_name] = selected_value == expected_value


def normalize_enum_semantic(value: Any) -> Any:
    """Normalize enum-like values so semantically equivalent options compare reliably."""
    if value is None:
        return None

    raw_value = getattr(value, "value", value)
    if isinstance(raw_value, str):
        return raw_value.strip().upper()
    return raw_value


def apply_enum_registry(
    field_values: dict[str, Any],
    selected_value: Any,
    checkbox_registry: Mapping[str, Any],
    *,
    enabled: bool = True,
) -> None:
    """Assign checkbox values from a field->enum registry using normalized enum semantics."""
    normalized_selected = normalize_enum_semantic(selected_value)

    for field_name, expected in checkbox_registry.items():
        if isinstance(expected, (list, tuple, set, frozenset)):
            expected_values = {normalize_enum_semantic(item) for item in expected}
            field_values[field_name] = bool(enabled) and normalized_selected in expected_values
            continue

        field_values[field_name] = bool(enabled) and normalized_selected == normalize_enum_semantic(expected)


def map_identity_person_block(
    field_values: dict[str, Any],
    person: Any,
    *,
    passport_field: str,
    nie_fields: tuple[str, str, str],
    date_fields: tuple[str, str, str],
    text_fields: Mapping[str, str],
    gender_checkbox_map: Mapping[str, Any],
    marital_checkbox_map: Mapping[str, Any],
) -> None:
    """Map a standard applicant/foreigner identity section into PDF fields."""
    field_values[passport_field] = coerce_str(getattr(person, "passport", None))

    nie_value = getattr(person, "nie", None)
    if nie_value:
        n1, n2, n3 = split_nie(nie_value)
        field_values[nie_fields[0]] = n1
        field_values[nie_fields[1]] = n2
        field_values[nie_fields[2]] = n3
    else:
        field_values[nie_fields[0]] = ""
        field_values[nie_fields[1]] = ""
        field_values[nie_fields[2]] = ""

    date_value = getattr(person, "date_of_birth", None)
    if date_value is not None:
        field_values[date_fields[0]] = date_value.strftime("%d")
        field_values[date_fields[1]] = date_value.strftime("%m")
        field_values[date_fields[2]] = date_value.strftime("%Y")
    else:
        field_values[date_fields[0]] = ""
        field_values[date_fields[1]] = ""
        field_values[date_fields[2]] = ""

    for attr_name, field_name in text_fields.items():
        field_values[field_name] = coerce_str(getattr(person, attr_name, None))

    gender = getattr(person, "gender", None)
    marital = getattr(person, "marital_status", None)
    assign_checkboxes(field_values, getattr(gender, "value", None), gender_checkbox_map)
    assign_checkboxes(field_values, getattr(marital, "value", None), marital_checkbox_map)


def map_optional_object_fields(
    field_values: dict[str, Any],
    obj: Any,
    *,
    text_fields: Mapping[str, str],
) -> None:
    """Map object attributes to text fields; if object is missing write empty strings."""
    for attr_name, field_name in text_fields.items():
        field_values[field_name] = coerce_str(getattr(obj, attr_name, None)) if obj else ""


def map_notification_block(
    field_values: dict[str, Any],
    notification: Any,
    *,
    text_fields: Mapping[str, str],
    consent_field: str | None = None,
) -> None:
    """Map notification fields and consent checkbox for required notification sections."""
    for attr_name, field_name in text_fields.items():
        field_values[field_name] = coerce_str(getattr(notification, attr_name, None))
    if consent_field:
        field_values[consent_field] = bool(getattr(notification, "consent_electronic_notifications", False))
