#!/usr/bin/env python3
"""
Fill editable immigration PDF forms from structured input values.

Usage
-----
python fill_form.py --form EX11 --input examples/ex11-input.json
python fill_form.py --form EX11 --input payload.json --output forms/filled/EX11-filled.pdf

Input JSON format
-----------------
{
  "field_values": {
    "Texto5": "GARCIA",
    "Texto6": "MARTIN"
  },
  "semantic_values": [
    {
      "selector": {"normalized_role": "passport_number"},
      "value": "P1234567"
    },
    {
      "selector": {
        "normalized_group": "identity_header",
        "normalized_role": "sex_option"
      },
      "value": "M"
    },
    {
      "selector": {
        "normalized_group": "yes_no_question",
        "normalized_parent_label_contains": "Hijas/os"
      },
      "value": "NO"
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import logging
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

import fitz
from pydantic import BaseModel

from forms_registry import get_form_code_for_model_module, get_mapper_function

EDITABLE_DIR = Path("forms/editable")
DEFINITIONS_DIR = Path("forms/definitions")
FILLED_DIR = Path("forms/filled")

CHECK_TYPES = {"CheckBox", "RadioButton"}
TEXT_TYPES = {"Text", "ComboBox", "ListBox"}


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def _normalize(s: Any) -> str:
    if s is None:
        return ""
    txt = str(s).strip()
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(ch for ch in txt if not unicodedata.combining(ch))
    return txt.casefold()


def _to_form_code(raw: str) -> str:
    value = (raw or "").strip().upper()
    if not value.startswith("EX"):
        value = f"EX{value}"
    return value


def _load_form_definition(form_code: str) -> dict:
    path = DEFINITIONS_DIR / f"{form_code}.json"
    if not path.exists():
        raise FileNotFoundError(f"Definition file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_form_definition(form_code: str) -> dict:
    return _load_form_definition(form_code)


def _find_editable_pdf(form_code: str) -> Path:
    candidates = sorted(EDITABLE_DIR.glob(f"{form_code}*.pdf"))
    if not candidates:
        raise FileNotFoundError(f"No editable PDF found for {form_code} in {EDITABLE_DIR}")
    # Prefer files explicitly marked as editable.
    for candidate in candidates:
        if "editable" in candidate.name.lower():
            return candidate
    return candidates[0]


def _selector_matches(field: dict, selector: dict) -> bool:
    for key, expected in selector.items():
        if key.endswith("_contains"):
            base = key[: -len("_contains")]
            actual = field.get(base)
            if _normalize(expected) not in _normalize(actual):
                return False
            continue

        actual = field.get(key)
        if isinstance(expected, str):
            if _normalize(actual) != _normalize(expected):
                return False
        else:
            if actual != expected:
                return False

    return True


def _field_option_token(field: dict) -> str:
    # Prefer explicit checkbox option text. Fallback to the right side of labels like "Sexo: M".
    option = field.get("checkbox_option_text")
    if option:
        return _normalize(option)

    label = field.get("label") or ""
    if ":" in label:
        return _normalize(label.split(":", 1)[1])
    return _normalize(label)


def _build_assignments(definition: dict, payload: dict) -> tuple[dict[str, Any], list[str]]:
    fields = definition.get("fields", [])
    by_name = {f["name"]: f for f in fields}
    assignments: dict[str, Any] = {}
    warnings: list[str] = []

    # 1) Direct field assignments by widget name.
    for field_name, value in (payload.get("field_values") or {}).items():
        if field_name not in by_name:
            warnings.append(f"field_values key '{field_name}' not found in definition")
            continue
        assignments[field_name] = value

    # 2) Semantic assignments using selector metadata.
    for idx, item in enumerate(payload.get("semantic_values") or [], start=1):
        selector = item.get("selector") or {}
        value = item.get("value")
        if not selector:
            warnings.append(f"semantic_values[{idx}] has empty selector")
            continue

        matched = [f for f in fields if _selector_matches(f, selector)]
        if not matched:
            warnings.append(f"semantic_values[{idx}] matched 0 fields for selector={selector}")
            continue

        check_like = [f for f in matched if f.get("type") in CHECK_TYPES]

        # Checkbox/radio selector with option values (single-select or multi-select).
        if check_like and isinstance(value, (str, list, tuple, set)):
            wanted = {_normalize(v) for v in ([value] if isinstance(value, str) else list(value))}
            for field in check_like:
                token = _field_option_token(field)
                assignments[field["name"]] = token in wanted

            # Also apply scalar values to non-checkbox matches in the same selector.
            for field in matched:
                if field.get("type") not in CHECK_TYPES:
                    assignments[field["name"]] = value
            continue

        # Checkbox/radio selector with explicit bool value.
        if check_like and isinstance(value, bool):
            for field in check_like:
                assignments[field["name"]] = value
            for field in matched:
                if field.get("type") not in CHECK_TYPES:
                    assignments[field["name"]] = value
            continue

        # Generic assignment for text-like and remaining field types.
        for field in matched:
            assignments[field["name"]] = value

    return assignments, warnings


def build_assignments(definition: dict, payload: dict) -> tuple[dict[str, Any], list[str]]:
    return _build_assignments(definition, payload)


def _set_widget_value(widget: fitz.Widget, value: Any) -> None:
    field_type = widget.field_type_string

    if field_type in CHECK_TYPES:
        on_state = widget.on_state() if callable(widget.on_state) else widget.on_state
        checked = bool(value)
        widget.field_value = on_state if checked else "Off"
        widget.update()
        return

    if field_type in TEXT_TYPES:
        widget.field_value = "" if value is None else str(value)
        widget.update()
        return

    # Fallback for uncommon field types.
    widget.field_value = "" if value is None else str(value)
    widget.update()


def fill_form(form_code: str, payload: dict, output_path: Path | None = None) -> Path:
    definition = _load_form_definition(form_code)
    source_pdf = _find_editable_pdf(form_code)

    assignments, warnings = _build_assignments(definition, payload)
    for warning in warnings:
        log.warning(warning)

    if output_path is None:
        FILLED_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = FILLED_DIR / f"{form_code}-filled-{stamp}.pdf"
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(source_pdf))
    updated = 0

    for page in doc:
        for widget in page.widgets():
            name = widget.field_name
            if name not in assignments:
                continue
            _set_widget_value(widget, assignments[name])
            updated += 1

    if hasattr(doc, "need_appearances"):
        doc.need_appearances(True)

    doc.save(str(output_path), garbage=4, deflate=True)
    doc.close()

    log.info("Source PDF: %s", source_pdf)
    log.info("Assigned fields (by name): %d", len(assignments))
    log.info("Updated widgets: %d", updated)
    log.info("Saved filled PDF: %s", output_path)

    return output_path


def fill_form_from_model(model: BaseModel, output_path: Path | None = None) -> Path:
    """
    Fill a form from a Pydantic domain model instance.

    The form code and mapper are resolved automatically from the model's module:
      models.ex00.EX00FormSchema  →  form code EX00, mapper mappers.ex00

    Parameters
    ----------
    model       : instance of any EXnn domain model (e.g. EX00FormSchema)
    output_path : optional; written to forms/filled/ by default

    Returns
    -------
    Path of the saved filled PDF
    """
    model_module = model.__class__.__module__
    form_code = get_form_code_for_model_module(model_module)
    mapper = get_mapper_function(form_code)

    field_values = mapper(model)
    payload = {"field_values": field_values}
    return fill_form(form_code, payload, output_path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fill editable PDFs from JSON input")
    parser.add_argument("--form", required=True, help="Form code, e.g. EX11")
    parser.add_argument("--input", required=True, help="Path to JSON payload file")
    parser.add_argument("--output", help="Optional output PDF path")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    form_code = _to_form_code(args.form)

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input JSON not found: {input_path}")

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    out = Path(args.output) if args.output else None

    fill_form(form_code, payload, out)


if __name__ == "__main__":
    main()
