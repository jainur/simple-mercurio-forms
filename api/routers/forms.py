from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from api.security.auth import require_api_key
from api.services import catalog_service

router = APIRouter(prefix="/forms", tags=["forms"], dependencies=[Depends(require_api_key)])


@router.get("")
def list_forms() -> list[dict]:
    return [item.model_dump() for item in catalog_service.list_forms()]


@router.get("/{form_code}")
def get_form(form_code: str) -> dict:
    detail = catalog_service.get_form(form_code)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Unknown form '{form_code}'")
    return detail.model_dump()


@router.get("/{form_code}/fields")
def get_form_fields(
    form_code: str,
    field_type: str | None = Query(default=None, alias="type"),
    page: int | None = None,
    section_code: str | None = None,
) -> list[dict]:
    if catalog_service.get_form(form_code) is None:
        raise HTTPException(status_code=404, detail=f"Unknown form '{form_code}'")
    return [
        field.model_dump()
        for field in catalog_service.get_form_fields(form_code, field_type=field_type, page=page, section_code=section_code)
    ]


@router.get("/{form_code}/sections")
def get_form_sections(form_code: str) -> list[dict]:
    detail = catalog_service.get_form(form_code)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Unknown form '{form_code}'")
    return [section.model_dump() for section in detail.sections]