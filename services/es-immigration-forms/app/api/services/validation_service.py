from __future__ import annotations

from scripts.fill_form import TEXT_TYPES, build_assignments, load_form_definition

from app.api.schemas.fill import FillPayload, MappingValidationResult, ValidationIssue, ValidationResult
from app.api.services.model_service import validate_model_payload


def validate_fill_payload(form_code: str, payload: FillPayload) -> ValidationResult:
    definition = load_form_definition(form_code)
    field_names = {field["name"] for field in definition.get("fields", [])}

    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    for field_name in payload.field_values:
        if field_name not in field_names:
            errors.append(
                ValidationIssue(
                    path=f"field_values.{field_name}",
                    code="UNKNOWN_FIELD",
                    message=f"Field '{field_name}' does not exist in definition {form_code}",
                )
            )

    assignments, assignment_warnings = build_assignments(definition, payload.model_dump(mode="python"))
    for warning in assignment_warnings:
        warnings.append(ValidationIssue(code="SEMANTIC_WARNING", message=warning))

    return ValidationResult(
        form_code=form_code,
        valid=not errors,
        errors=errors,
        warnings=warnings,
    )


def validate_model_request(form_code: str, model_payload: dict) -> ValidationResult:
    try:
        validate_model_payload(form_code, model_payload)
    except Exception as exc:
        return ValidationResult(
            form_code=form_code,
            valid=False,
            errors=[ValidationIssue(code="MODEL_VALIDATION_ERROR", message=str(exc))],
        )

    return ValidationResult(form_code=form_code, valid=True)


def validate_mapping(form_code: str, payload: FillPayload, strict_text_fields: bool) -> MappingValidationResult:
    definition = load_form_definition(form_code)
    fields = definition.get("fields", [])
    assignments, warnings = build_assignments(definition, payload.model_dump(mode="python"))

    definition_names = {field["name"] for field in fields}
    submitted_names = set(payload.field_values)
    # Extra fields: keys in the submitted payload that are not in the form definition.
    # build_assignments silently drops unknown fields, so we compute this from the raw payload.
    extra_assignment_fields = sorted(submitted_names - definition_names)
    # Missing fields: definition fields not present in the assignments (informational only).
    missing_definition_fields = sorted(definition_names - set(assignments))

    blank_text_fields = sorted(
        field["name"]
        for field in fields
        if field.get("type") in TEXT_TYPES
        and field["name"] in assignments
        and (assignments[field["name"]] is None or str(assignments[field["name"]]).strip() == "")
    )

    # A mapping is valid when there are no ghost fields. Missing definition fields
    # just means a partial payload, which is acceptable.
    is_valid = not extra_assignment_fields
    if strict_text_fields:
        is_valid = is_valid and not blank_text_fields

    return MappingValidationResult(
        form_code=form_code,
        valid=is_valid,
        assigned_fields=len(assignments),
        definition_field_count=len(fields),
        missing_definition_fields=missing_definition_fields,
        extra_assignment_fields=extra_assignment_fields,
        blank_text_fields=blank_text_fields,
        warnings=warnings,
    )