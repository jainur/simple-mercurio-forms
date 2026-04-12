from __future__ import annotations

import re
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel

from scripts.fill_form import build_assignments, fill_form, fill_form_from_model, load_form_definition
from scripts.forms_registry import get_mapper_function

from app.api.schemas.fill import FillAssignmentSummary, FillPayload, FillResult, PreviewResult

ROOT_DIR = Path(__file__).resolve().parents[3]
API_FILLED_DIR = ROOT_DIR / "data" / "forms" / "filled" / "api"

_SAFE_NAME_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_output_name(form_code: str, raw_name: str | None) -> str:
    if raw_name:
        cleaned = _SAFE_NAME_PATTERN.sub("-", raw_name).strip("-.")
        if cleaned:
            return cleaned if cleaned.lower().endswith(".pdf") else f"{cleaned}.pdf"
    return f"{form_code}-{uuid4().hex}.pdf"


def preview_fill(form_code: str, payload: FillPayload) -> PreviewResult:
    definition = load_form_definition(form_code)
    assignments, warnings = build_assignments(definition, payload.model_dump(mode="python"))
    return PreviewResult(
        form_code=form_code,
        assigned_fields=len(assignments),
        assignments=assignments,
        warnings=warnings,
    )


def execute_fill(form_code: str, payload: FillPayload) -> FillResult:
    preview = preview_fill(form_code, payload)
    API_FILLED_DIR.mkdir(parents=True, exist_ok=True)
    file_name = _safe_output_name(form_code, payload.output_name)
    output_path = API_FILLED_DIR / file_name
    filled_path = fill_form(form_code, payload.model_dump(mode="python", exclude_none=True), output_path)
    try:
        rel_path = str(filled_path.relative_to(ROOT_DIR))
    except ValueError:
        rel_path = str(filled_path)
    return FillResult(
        form_code=form_code,
        file_id=file_name,
        file_name=file_name,
        download_url=f"/api/v1/artifacts/{file_name}",
        output_path=rel_path,
        assignment_summary=FillAssignmentSummary(
            assigned_fields=preview.assigned_fields,
            warning_count=len(preview.warnings),
            warnings=preview.warnings,
        ),
    )


def execute_fill_from_model(form_code: str, model: BaseModel, output_name: str | None = None) -> FillResult:
    API_FILLED_DIR.mkdir(parents=True, exist_ok=True)
    file_name = _safe_output_name(form_code, output_name)
    output_path = API_FILLED_DIR / file_name
    mapper = get_mapper_function(form_code)
    field_values = mapper(model)
    mapper_output = fill_form_from_model(model, output_path)
    try:
        rel_path = str(mapper_output.relative_to(ROOT_DIR))
    except ValueError:
        rel_path = str(mapper_output)
    return FillResult(
        form_code=form_code,
        file_id=file_name,
        file_name=file_name,
        download_url=f"/api/v1/artifacts/{file_name}",
        output_path=rel_path,
        assignment_summary=FillAssignmentSummary(
            assigned_fields=len(field_values),
            warning_count=0,
            warnings=[],
        ),
    )


def get_artifact_path(file_id: str) -> Path:
    candidate = API_FILLED_DIR / file_id
    resolved = candidate.resolve()
    if API_FILLED_DIR.resolve() not in resolved.parents or not resolved.exists():
        raise FileNotFoundError(file_id)
    return resolved