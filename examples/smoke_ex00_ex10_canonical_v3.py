#!/usr/bin/env python3
"""Strict smoke runner for EX00-EX10 with canonical-v3 output names.

Checks per form:
- mapper output has no missing PDF field names
- mapper output has no extra field names
- mapper output contains no None values

Outputs:
- forms/filled/canonical-v3/EXxx-canonical-v3.pdf
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fill_form import fill_form
from forms_registry import get_mapper_function

EX_CODES = ["EX00", "EX01", "EX02", "EX03", "EX04", "EX06", "EX07", "EX09", "EX10"]
OUTPUT_DIR = ROOT / "forms" / "filled" / "canonical-v3"


def _load_example_module(example_path: Path):
    spec = importlib.util.spec_from_file_location(example_path.stem, example_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {example_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _definition_field_names(form_code: str) -> set[str]:
    definition_path = ROOT / "forms" / "definitions" / f"{form_code}.json"
    payload = json.loads(definition_path.read_text(encoding="utf-8"))
    return {field["name"] for field in payload.get("fields", [])}


def main() -> int:
    failures: list[str] = []
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for form_code in EX_CODES:
        suffix = form_code[2:]
        example_path = ROOT / "examples" / f"ex{suffix}_domain_example.py"

        module = _load_example_module(example_path)
        form = getattr(module, "form", None)
        if form is None:
            failures.append(f"{form_code}: missing global 'form' object in example module")
            continue

        mapper = get_mapper_function(form_code)
        field_values = mapper(form)

        expected_fields = _definition_field_names(form_code)
        mapped_fields = set(field_values.keys())

        missing = sorted(expected_fields - mapped_fields)
        extra = sorted(mapped_fields - expected_fields)
        none_fields = sorted(k for k, v in field_values.items() if v is None)

        if missing:
            failures.append(f"{form_code}: missing fields ({len(missing)}): {', '.join(missing[:10])}")
        if extra:
            failures.append(f"{form_code}: extra fields ({len(extra)}): {', '.join(extra[:10])}")
        if none_fields:
            failures.append(f"{form_code}: None values ({len(none_fields)}): {', '.join(none_fields[:10])}")

        out_path = OUTPUT_DIR / f"{form_code}-canonical-v3.pdf"
        fill_form(form_code, {"field_values": field_values}, out_path)

        print(
            f"{form_code}: expected={len(expected_fields)} mapped={len(mapped_fields)} "
            f"missing={len(missing)} extra={len(extra)} none={len(none_fields)} -> {out_path}"
        )

    if failures:
        print("\nSMOKE CHECK FAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nSMOKE CHECK PASSED (EX00-EX10 canonical-v3)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
