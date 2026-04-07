#!/usr/bin/env python3
"""Generate canonical-v3 PDFs for all available EX01-EX30 examples.

For each available example module:
- build mapped field values from the domain form
- detect missing/extra keys versus form definition
- backfill blank text-like fields with deterministic placeholders
- save forms/filled/canonical-v3/EXxx-canonical-v3.pdf

This is intended for review PDFs where every text widget is visibly populated.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fill_form import fill_form
from forms_registry import get_mapper_function

TEXT_TYPES = {"Text", "ComboBox", "ListBox"}
CHECK_TYPES = {"CheckBox", "RadioButton"}
OUTPUT_DIR = ROOT / "forms" / "filled" / "canonical-v3"


def _discover_codes() -> list[str]:
    codes: list[str] = []
    for path in sorted((ROOT / "examples").glob("ex*_domain_example.py")):
        match = re.match(r"ex(\d{2})_domain_example\.py$", path.name)
        if not match:
            continue
        suffix = match.group(1)
        if int(suffix) >= 1:
            codes.append(f"EX{suffix}")
    return codes


def _load_example_module(example_path: Path):
    spec = importlib.util.spec_from_file_location(example_path.stem, example_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec: {example_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_definition(form_code: str) -> dict:
    definition_path = ROOT / "forms" / "definitions" / f"{form_code}.json"
    return json.loads(definition_path.read_text(encoding="utf-8"))


def _placeholder_for(name: str) -> str:
    return f"AUTO_{name}"


def main() -> int:
    failures: list[str] = []
    codes = _discover_codes()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Processing {len(codes)} forms: {', '.join(codes)}")

    for form_code in codes:
        suffix = form_code[2:]
        module = _load_example_module(ROOT / "examples" / f"ex{suffix}_domain_example.py")
        form = getattr(module, "form", None)
        if form is None:
            failures.append(f"{form_code}: missing global 'form' in example module")
            continue

        mapper = get_mapper_function(form_code)
        fv = mapper(form)
        fv_out = dict(fv)

        definition = _load_definition(form_code)
        fields = definition.get("fields", [])
        by_name = {f["name"]: f for f in fields}
        expected = set(by_name.keys())
        mapped = set(fv_out.keys())

        missing = sorted(expected - mapped)
        extra = sorted(mapped - expected)

        blank_before = 0
        backfilled = 0

        for name, meta in by_name.items():
            ftype = meta.get("type")

            if name not in fv_out:
                if ftype in TEXT_TYPES:
                    fv_out[name] = _placeholder_for(name)
                    backfilled += 1
                elif ftype in CHECK_TYPES:
                    fv_out[name] = False
                continue

            value = fv_out[name]
            if ftype in TEXT_TYPES and isinstance(value, str) and value.strip() == "":
                blank_before += 1
                fv_out[name] = _placeholder_for(name)
                backfilled += 1

        # Guard: no blank strings should remain in text-like fields.
        remaining_blank = 0
        for name, meta in by_name.items():
            if meta.get("type") not in TEXT_TYPES:
                continue
            value = fv_out.get(name)
            if isinstance(value, str) and value.strip() == "":
                remaining_blank += 1

        out_path = OUTPUT_DIR / f"{form_code}-canonical-v3.pdf"
        fill_form(form_code, {"field_values": fv_out}, out_path)

        print(
            f"{form_code}: expected={len(expected)} mapped={len(mapped)} "
            f"missing={len(missing)} extra={len(extra)} blank_before={blank_before} "
            f"backfilled={backfilled} remaining_blank={remaining_blank}"
        )

        if remaining_blank:
            failures.append(f"{form_code}: remaining_blank={remaining_blank}")

    if failures:
        print("\nFAILED")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nPASS: canonical-v3 generated for all available EX01-EX30 forms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
