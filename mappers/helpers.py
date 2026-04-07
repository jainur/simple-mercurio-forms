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
