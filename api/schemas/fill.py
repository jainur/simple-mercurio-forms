from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SemanticAssignment(BaseModel):
    selector: dict[str, Any] = Field(default_factory=dict)
    value: Any = None


class FillPayload(BaseModel):
    field_values: dict[str, Any] = Field(default_factory=dict)
    semantic_values: list[SemanticAssignment] = Field(default_factory=list)
    output_name: str | None = None


class ModelFillPayload(BaseModel):
    model_payload: dict[str, Any]
    output_name: str | None = None


class FillAssignmentSummary(BaseModel):
    assigned_fields: int
    warning_count: int
    warnings: list[str] = Field(default_factory=list)


class FillResult(BaseModel):
    form_code: str
    file_id: str
    file_name: str
    download_url: str
    output_path: str
    assignment_summary: FillAssignmentSummary


class PreviewResult(BaseModel):
    form_code: str
    assigned_fields: int
    assignments: dict[str, Any]
    warnings: list[str] = Field(default_factory=list)


class ValidationIssue(BaseModel):
    path: str | None = None
    code: str
    message: str


class ValidationResult(BaseModel):
    form_code: str
    valid: bool
    errors: list[ValidationIssue] = Field(default_factory=list)
    warnings: list[ValidationIssue] = Field(default_factory=list)


class MappingValidationResult(BaseModel):
    form_code: str
    valid: bool
    assigned_fields: int
    definition_field_count: int
    missing_definition_fields: list[str] = Field(default_factory=list)
    extra_assignment_fields: list[str] = Field(default_factory=list)
    blank_text_fields: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class MappingValidationRequest(BaseModel):
    payload: FillPayload
    strict_text_fields: bool = False