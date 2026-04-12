from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class FormSummary(BaseModel):
    form_code: str
    title: str | None = None
    filename: str
    page_count: int | None = None
    field_count: int | None = None
    has_definition: bool = True
    has_domain_example: bool
    supported_fill_modes: list[str] = Field(default_factory=list)


class FormField(BaseModel):
    name: str
    type: str
    page: int | None = None
    label: str | None = None
    section_code: str | None = None
    section_title: str | None = None
    normalized_group: str | None = None
    normalized_role: str | None = None
    normalized_parent_label: str | None = None
    checkbox_option_text: str | None = None
    raw: dict[str, Any]


class FormSection(BaseModel):
    section_code: str | None = None
    section_title: str | None = None
    section_level: int | None = None
    field_count: int


class FormDetail(FormSummary):
    sections: list[FormSection] = Field(default_factory=list)