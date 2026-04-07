from __future__ import annotations

import sqlite3
from pathlib import Path

from api.schemas.forms import FormDetail, FormField, FormSection, FormSummary

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "forms.db"
DEFINITIONS_DIR = ROOT_DIR / "forms" / "definitions"
EXAMPLES_DIR = ROOT_DIR / "examples"


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def list_forms() -> list[FormSummary]:
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT form_code, filename, title, page_count, field_count
            FROM forms
            ORDER BY form_code
            """
        ).fetchall()

    return [
        FormSummary(
            form_code=row["form_code"],
            filename=row["filename"],
            title=row["title"],
            page_count=row["page_count"],
            field_count=row["field_count"],
            has_domain_example=(EXAMPLES_DIR / f"{row['form_code'].lower()}_domain_example.py").exists(),
            supported_fill_modes=["field_values", "semantic_values", "domain_model"],
        )
        for row in rows
    ]


def get_form(form_code: str) -> FormDetail | None:
    code = form_code.strip().upper()
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT form_code, filename, title, page_count, field_count
            FROM forms
            WHERE form_code = ?
            """,
            (code,),
        ).fetchone()

        if row is None:
            return None

        section_rows = connection.execute(
            """
            SELECT section_code, section_title, section_level, COUNT(*) AS field_count
            FROM form_fields
            WHERE form_id = (SELECT id FROM forms WHERE form_code = ?)
            GROUP BY section_code, section_title, section_level
            ORDER BY MIN(page), MIN(id)
            """,
            (code,),
        ).fetchall()

    return FormDetail(
        form_code=row["form_code"],
        filename=row["filename"],
        title=row["title"],
        page_count=row["page_count"],
        field_count=row["field_count"],
        has_domain_example=(EXAMPLES_DIR / f"{code.lower()}_domain_example.py").exists(),
        supported_fill_modes=["field_values", "semantic_values", "domain_model"],
        sections=[
            FormSection(
                section_code=section_row["section_code"],
                section_title=section_row["section_title"],
                section_level=section_row["section_level"],
                field_count=section_row["field_count"],
            )
            for section_row in section_rows
        ],
    )


def get_form_fields(
    form_code: str,
    field_type: str | None = None,
    page: int | None = None,
    section_code: str | None = None,
) -> list[FormField]:
    code = form_code.strip().upper()
    clauses = ["forms.form_code = ?"]
    params: list[object] = [code]

    if field_type:
        clauses.append("form_fields.type = ?")
        params.append(field_type)
    if page is not None:
        clauses.append("form_fields.page = ?")
        params.append(page)
    if section_code:
        clauses.append("form_fields.section_code = ?")
        params.append(section_code)

    query = f"""
        SELECT
            form_fields.name,
            form_fields.type,
            form_fields.page,
            form_fields.label,
            form_fields.section_code,
            form_fields.section_title,
            form_fields.normalized_group,
            form_fields.normalized_role,
            form_fields.normalized_parent_label,
            form_fields.checkbox_option_text,
            form_fields.label_pdf,
            form_fields.label_inferred,
            form_fields.label_source,
            form_fields.label_confidence,
            form_fields.default_value,
            form_fields.max_length,
            form_fields.choices,
            form_fields.on_state,
            form_fields.multiline,
            form_fields.required,
            form_fields.read_only
        FROM form_fields
        JOIN forms ON forms.id = form_fields.form_id
        WHERE {' AND '.join(clauses)}
        ORDER BY form_fields.page, form_fields.id
    """

    with _connect() as connection:
        rows = connection.execute(query, params).fetchall()

    fields: list[FormField] = []
    for row in rows:
        raw = dict(row)
        fields.append(
            FormField(
                name=row["name"],
                type=row["type"],
                page=row["page"],
                label=row["label"],
                section_code=row["section_code"],
                section_title=row["section_title"],
                normalized_group=row["normalized_group"],
                normalized_role=row["normalized_role"],
                normalized_parent_label=row["normalized_parent_label"],
                checkbox_option_text=row["checkbox_option_text"],
                raw=raw,
            )
        )
    return fields


def get_form_sections(form_code: str) -> list[FormSection]:
    detail = get_form(form_code)
    return [] if detail is None else detail.sections