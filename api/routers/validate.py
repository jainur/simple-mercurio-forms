from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.schemas.fill import FillPayload, MappingValidationRequest, ModelFillPayload
from api.security.auth import require_api_key
from api.services import catalog_service, validation_service

router = APIRouter(prefix="/forms", tags=["validation"], dependencies=[Depends(require_api_key)])


def _ensure_form(form_code: str) -> str:
    code = form_code.strip().upper()
    if catalog_service.get_form(code) is None:
        raise HTTPException(status_code=404, detail=f"Unknown form '{code}'")
    return code


@router.post("/{form_code}/validate")
def validate_fill(form_code: str, payload: FillPayload) -> dict:
    code = _ensure_form(form_code)
    return validation_service.validate_fill_payload(code, payload).model_dump()


@router.post("/{form_code}/validate-model")
def validate_model(form_code: str, payload: ModelFillPayload) -> dict:
    code = _ensure_form(form_code)
    return validation_service.validate_model_request(code, payload.model_payload).model_dump()


@router.post("/{form_code}/validate-mapping")
def validate_mapping(form_code: str, request: MappingValidationRequest) -> dict:
    code = _ensure_form(form_code)
    return validation_service.validate_mapping(code, request.payload, request.strict_text_fields).model_dump()