#!/usr/bin/env python3
"""Run form-filling tests with realistic, diverse personas.

This script validates mapper/fill behavior while using varied, human-realistic profiles:
- different countries and nationalities
- adult and child applicants
- varied civil status and gender
- with and without representation

Outputs:
- forms/filled/realistic-personas/EXxx-realistic-<persona>.pdf
- docs/framework/realistic-persona-test-report.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any, get_args, get_origin

from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fill_form import fill_form
from forms_registry import get_mapper_function

TEXT_TYPES = {"Text", "ComboBox", "ListBox"}
OUT_DIR = ROOT / "forms" / "filled" / "realistic-personas"
REPORT_PATH = ROOT / "docs" / "framework" / "realistic-persona-test-report.json"


@dataclass(frozen=True)
class Persona:
    code: str
    first_name: str
    first_surname: str
    second_surname: str
    gender: str
    marital_status: str
    birth_country: str
    nationality: str
    birth_place: str
    city: str
    province: str
    postal_code: str
    address: str
    address_number: str
    floor_door: str
    mobile_phone: str
    email: str
    is_minor: bool
    with_representation: bool
    consent_electronic_notifications: bool


PERSONAS = [
    Persona(
        code="adult-col-male-single-no-rep",
        first_name="Luis Andres",
        first_surname="Garcia",
        second_surname="Martinez",
        gender="MALE",
        marital_status="SINGLE",
        birth_country="Colombia",
        nationality="Colombiana",
        birth_place="Bogota",
        city="Madrid",
        province="Madrid",
        postal_code="28013",
        address="Calle de Alcala",
        address_number="112",
        floor_door="3B",
        mobile_phone="612345678",
        email="luis.garcia@example.es",
        is_minor=False,
        with_representation=False,
        consent_electronic_notifications=True,
    ),
    Persona(
        code="adult-mar-female-married-with-rep",
        first_name="Amina",
        first_surname="El Idrissi",
        second_surname="Bennani",
        gender="FEMALE",
        marital_status="MARRIED",
        birth_country="Marruecos",
        nationality="Marroqui",
        birth_place="Casablanca",
        city="Barcelona",
        province="Barcelona",
        postal_code="08015",
        address="Carrer de Mallorca",
        address_number="245",
        floor_door="1A",
        mobile_phone="622334455",
        email="amina.elidrissi@example.es",
        is_minor=False,
        with_representation=True,
        consent_electronic_notifications=True,
    ),
    Persona(
        code="child-per-female-single-with-guardian",
        first_name="Camila",
        first_surname="Quispe",
        second_surname="Rojas",
        gender="FEMALE",
        marital_status="SINGLE",
        birth_country="Peru",
        nationality="Peruana",
        birth_place="Lima",
        city="Valencia",
        province="Valencia",
        postal_code="46007",
        address="Avenida del Puerto",
        address_number="88",
        floor_door="4C",
        mobile_phone="633556677",
        email="camila.quispe@example.es",
        is_minor=True,
        with_representation=True,
        consent_electronic_notifications=False,
    ),
    Persona(
        code="adult-uk-other-divorced-no-rep",
        first_name="Alex",
        first_surname="Taylor",
        second_surname="Morgan",
        gender="OTHER",
        marital_status="DIVORCED",
        birth_country="Reino Unido",
        nationality="Britanica",
        birth_place="Manchester",
        city="Malaga",
        province="Malaga",
        postal_code="29010",
        address="Calle Larios",
        address_number="19",
        floor_door="2D",
        mobile_phone="644778899",
        email="alex.taylor@example.es",
        is_minor=False,
        with_representation=False,
        consent_electronic_notifications=True,
    ),
    Persona(
        code="adult-arg-male-widowed-with-rep",
        first_name="Javier",
        first_surname="Fernandez",
        second_surname="Lopez",
        gender="MALE",
        marital_status="WIDOWED",
        birth_country="Argentina",
        nationality="Argentina",
        birth_place="Cordoba",
        city="Sevilla",
        province="Sevilla",
        postal_code="41001",
        address="Calle Sierpes",
        address_number="7",
        floor_door="5A",
        mobile_phone="655667788",
        email="javier.fernandez@example.es",
        is_minor=False,
        with_representation=True,
        consent_electronic_notifications=False,
    ),
    Persona(
        code="adult-sen-female-separated-no-rep",
        first_name="Ndeye",
        first_surname="Diop",
        second_surname="Ndiaye",
        gender="FEMALE",
        marital_status="SEPARATED",
        birth_country="Senegal",
        nationality="Senegalesa",
        birth_place="Dakar",
        city="Bilbao",
        province="Bizkaia",
        postal_code="48009",
        address="Gran Via",
        address_number="54",
        floor_door="6E",
        mobile_phone="666778899",
        email="ndeye.diop@example.es",
        is_minor=False,
        with_representation=False,
        consent_electronic_notifications=True,
    ),
]


def _discover_codes() -> list[str]:
    codes: list[str] = []
    for path in sorted((ROOT / "examples").glob("ex*_domain_example.py")):
        m = re.match(r"ex(\d{2})_domain_example\.py$", path.name)
        if m:
            codes.append(f"EX{m.group(1)}")
    return codes


def _load_example_form(form_code: str) -> BaseModel:
    suffix = form_code[2:]
    path = ROOT / "examples" / f"ex{suffix}_domain_example.py"
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load example module: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    form_obj = getattr(mod, "form", None)
    if callable(form_obj):
        form_obj = form_obj()
    if form_obj is None:
        raise RuntimeError(f"Example {path.name} has no usable 'form'")
    return form_obj


def _copy_model(model: BaseModel, updates: dict[str, Any]) -> BaseModel:
    if hasattr(model, "model_copy"):
        return model.model_copy(update=updates)
    return model.copy(update=updates, deep=True)


def _extract_enum_type(annotation: Any) -> type[Enum] | None:
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return annotation
    origin = get_origin(annotation)
    if origin is None:
        return None
    for arg in get_args(annotation):
        if isinstance(arg, type) and issubclass(arg, Enum):
            return arg
    return None


def _enum_by_name(enum_type: type[Enum], wanted_name: str) -> Enum | None:
    key = wanted_name.upper()
    if key in enum_type.__members__:
        return enum_type[key]
    return None


def _safe_field_names(model: BaseModel) -> set[str]:
    if hasattr(model, "model_fields"):
        return set(model.model_fields.keys())
    return set(model.__fields__.keys())


def _safe_field_annotation(model: BaseModel, field: str) -> Any:
    if hasattr(model, "model_fields"):
        f = model.model_fields.get(field)
        return None if f is None else f.annotation
    f = model.__fields__.get(field)
    return None if f is None else f.type_


def _apply_identity(node: BaseModel, persona: Persona) -> BaseModel:
    fields = _safe_field_names(node)
    updates: dict[str, Any] = {}

    identity_like = {"first_surname", "name", "date_of_birth"}.issubset(fields)
    if identity_like:
        updates.update(
            {
                "name": persona.first_name,
                "first_surname": persona.first_surname,
                "second_surname": persona.second_surname,
                "birth_country": persona.birth_country if "birth_country" in fields else getattr(node, "birth_country", None),
                "birth_place": persona.birth_place if "birth_place" in fields else getattr(node, "birth_place", None),
                "nationality": persona.nationality if "nationality" in fields else getattr(node, "nationality", None),
                "address": persona.address if "address" in fields else getattr(node, "address", None),
                "address_number": persona.address_number if "address_number" in fields else getattr(node, "address_number", None),
                "floor_door": persona.floor_door if "floor_door" in fields else getattr(node, "floor_door", None),
                "city": persona.city if "city" in fields else getattr(node, "city", None),
                "postal_code": persona.postal_code if "postal_code" in fields else getattr(node, "postal_code", None),
                "province": persona.province if "province" in fields else getattr(node, "province", None),
                "mobile_phone": persona.mobile_phone if "mobile_phone" in fields else getattr(node, "mobile_phone", None),
                "email": persona.email if "email" in fields else getattr(node, "email", None),
                "date_of_birth": date(2014, 5, 16) if persona.is_minor else date(1989, 11, 3),
            }
        )
        if "legal_guardian_name" in fields:
            updates["legal_guardian_name"] = "Marta Ruiz" if persona.is_minor else None
        if "legal_guardian_id" in fields:
            updates["legal_guardian_id"] = "Y9988776K" if persona.is_minor else None
        if "legal_guardian_title" in fields:
            updates["legal_guardian_title"] = "Madre" if persona.is_minor else None
        if "children_in_school_age" in fields:
            updates["children_in_school_age"] = persona.is_minor
        if "has_school_age_children_in_spain" in fields:
            updates["has_school_age_children_in_spain"] = persona.is_minor

        if "gender" in fields:
            enum_t = _extract_enum_type(_safe_field_annotation(node, "gender")) or type(getattr(node, "gender", None))
            if isinstance(enum_t, type) and issubclass(enum_t, Enum):
                value = _enum_by_name(enum_t, persona.gender)
                if value is not None:
                    updates["gender"] = value

        if "marital_status" in fields:
            enum_t = _extract_enum_type(_safe_field_annotation(node, "marital_status")) or type(getattr(node, "marital_status", None))
            if isinstance(enum_t, type) and issubclass(enum_t, Enum):
                value = _enum_by_name(enum_t, persona.marital_status)
                if value is not None:
                    updates["marital_status"] = value

    if {"name_or_company", "id_number"}.issubset(fields):
        updates.update(
            {
                "name_or_company": f"{persona.first_name} {persona.first_surname}",
                "id_number": "Y1234567A",
                "address": persona.address if "address" in fields else getattr(node, "address", None),
                "address_number": persona.address_number if "address_number" in fields else getattr(node, "address_number", None),
                "floor_door": persona.floor_door if "floor_door" in fields else getattr(node, "floor_door", None),
                "city": persona.city if "city" in fields else getattr(node, "city", None),
                "postal_code": persona.postal_code if "postal_code" in fields else getattr(node, "postal_code", None),
                "province": persona.province if "province" in fields else getattr(node, "province", None),
                "mobile_phone": persona.mobile_phone if "mobile_phone" in fields else getattr(node, "mobile_phone", None),
                "email": persona.email if "email" in fields else getattr(node, "email", None),
            }
        )

    if "consent_electronic_notifications" in fields:
        updates["consent_electronic_notifications"] = persona.consent_electronic_notifications

    return _copy_model(node, updates) if updates else node


def _recursive_apply(node: Any, persona: Persona) -> Any:
    if isinstance(node, BaseModel):
        updates: dict[str, Any] = {}
        for field in _safe_field_names(node):
            val = getattr(node, field)
            if isinstance(val, BaseModel):
                updates[field] = _recursive_apply(val, persona)
        transformed = _copy_model(node, updates) if updates else node
        return _apply_identity(transformed, persona)
    return node


def _apply_representation_policy(form: BaseModel, persona: Persona) -> BaseModel:
    fields = _safe_field_names(form)
    updates: dict[str, Any] = {}

    rep_fields = [
        "filing_representative",
        "presenter_details",
        "legal_representative",
        "representative_details",
        "representative",
    ]

    for field in rep_fields:
        if field not in fields:
            continue
        current = getattr(form, field)
        if not persona.with_representation:
            updates[field] = None
        elif current is not None:
            updates[field] = _recursive_apply(current, persona)

    return _copy_model(form, updates) if updates else form


def _load_definition(form_code: str) -> dict[str, Any]:
    return json.loads((ROOT / "forms" / "definitions" / f"{form_code}.json").read_text(encoding="utf-8"))


def _pick_personas_for_form(form_index: int, scenarios_per_form: int) -> list[Persona]:
    count = max(1, min(scenarios_per_form, len(PERSONAS)))
    selected: list[Persona] = []

    adults = [p for p in PERSONAS if not p.is_minor]
    children = [p for p in PERSONAS if p.is_minor]
    adults_with_rep = [p for p in adults if p.with_representation]
    adults_without_rep = [p for p in adults if not p.with_representation]

    # Seeded picks guarantee realistic variation with age and representation diversity.
    seeded = []
    if children:
        seeded.append(children[form_index % len(children)])
    if adults_with_rep:
        seeded.append(adults_with_rep[form_index % len(adults_with_rep)])
    if adults_without_rep:
        seeded.append(adults_without_rep[form_index % len(adults_without_rep)])
    seeded.append(PERSONAS[(form_index + 2) % len(PERSONAS)])

    for candidate in seeded:
        if candidate not in selected:
            selected.append(candidate)
        if len(selected) >= count:
            return selected

    for offset in range(len(PERSONAS)):
        candidate = PERSONAS[(form_index + offset) % len(PERSONAS)]
        if candidate not in selected:
            selected.append(candidate)
        if len(selected) >= count:
            break

    return selected


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run realistic multi-persona form tests")
    parser.add_argument(
        "--scenarios-per-form",
        type=int,
        default=4,
        help="How many persona scenarios to run per form (default: 4, max: number of personas)",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    failures: list[str] = []

    codes = _discover_codes()
    for idx, code in enumerate(codes):
        def_path = ROOT / "forms" / "definitions" / f"{code}.json"
        if not def_path.exists():
            continue

        try:
            base_form = _load_example_form(code)
            definition = _load_definition(code)
            field_types = {f["name"]: f.get("type") for f in definition.get("fields", [])}
            mapper = get_mapper_function(code)

            personas = _pick_personas_for_form(idx, args.scenarios_per_form)
            for scenario_index, persona in enumerate(personas, start=1):
                persona_form = _recursive_apply(base_form, persona)
                persona_form = _apply_representation_policy(persona_form, persona)
                field_values = mapper(persona_form)

                blank_text = sorted(
                    name
                    for name, value in field_values.items()
                    if field_types.get(name) in TEXT_TYPES and isinstance(value, str) and value.strip() == ""
                )

                out_pdf = OUT_DIR / f"{code}-realistic-{scenario_index:02d}-{persona.code}.pdf"
                fill_form(code, {"field_values": field_values}, out_pdf)

                results.append(
                    {
                        "form": code,
                        "scenario_index": scenario_index,
                        "persona": persona.code,
                        "country": persona.birth_country,
                        "nationality": persona.nationality,
                        "gender": persona.gender,
                        "civil_status": persona.marital_status,
                        "age_group": "child" if persona.is_minor else "adult",
                        "with_representation": persona.with_representation,
                        "blank_text_values": len(blank_text),
                        "blank_text_samples": blank_text[:10],
                        "output_pdf": str(out_pdf.relative_to(ROOT)),
                    }
                )
        except Exception as exc:  # broad on purpose for audit continuity
            failures.append(f"{code}: {exc}")

    by_form: dict[str, dict[str, Any]] = {}
    for row in results:
        entry = by_form.setdefault(
            row["form"],
            {
                "form": row["form"],
                "scenarios": 0,
                "countries": set(),
                "genders": set(),
                "civil_statuses": set(),
                "age_groups": set(),
                "with_representation_count": 0,
                "without_representation_count": 0,
                "total_blank_text_values": 0,
            },
        )
        entry["scenarios"] += 1
        entry["countries"].add(row["country"])
        entry["genders"].add(row["gender"])
        entry["civil_statuses"].add(row["civil_status"])
        entry["age_groups"].add(row["age_group"])
        if row["with_representation"]:
            entry["with_representation_count"] += 1
        else:
            entry["without_representation_count"] += 1
        entry["total_blank_text_values"] += row["blank_text_values"]

    per_form_coverage: list[dict[str, Any]] = []
    for form_code in sorted(by_form):
        entry = by_form[form_code]
        per_form_coverage.append(
            {
                "form": form_code,
                "scenarios": entry["scenarios"],
                "countries": sorted(entry["countries"]),
                "genders": sorted(entry["genders"]),
                "civil_statuses": sorted(entry["civil_statuses"]),
                "age_groups": sorted(entry["age_groups"]),
                "with_representation_count": entry["with_representation_count"],
                "without_representation_count": entry["without_representation_count"],
                "total_blank_text_values": entry["total_blank_text_values"],
            }
        )

    summary = {
        "forms_tested": len(by_form),
        "total_scenarios": len(results),
        "scenarios_per_form_target": max(1, min(args.scenarios_per_form, len(PERSONAS))),
        "forms_failed": len(failures),
        "countries_covered": sorted({r["country"] for r in results}),
        "genders_covered": sorted({r["gender"] for r in results}),
        "civil_statuses_covered": sorted({r["civil_status"] for r in results}),
        "age_groups_covered": sorted({r["age_group"] for r in results}),
        "with_representation_count": sum(1 for r in results if r["with_representation"]),
        "without_representation_count": sum(1 for r in results if not r["with_representation"]),
        "forms_with_blank_text": sorted({r["form"] for r in results if r["blank_text_values"] > 0}),
        "total_blank_text_values": sum(r["blank_text_values"] for r in results),
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(
            {
                "summary": summary,
                "failures": failures,
                "per_form_coverage": per_form_coverage,
                "results": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2))
    if failures:
        print("Failures:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"Wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
