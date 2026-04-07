from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from api.schemas.fill import FillPayload, ModelFillPayload
from api.security.auth import require_api_key
from api.services import catalog_service, fill_service, model_service

router = APIRouter(tags=["fill"], dependencies=[Depends(require_api_key)])


def _ensure_form(form_code: str) -> str:
    code = form_code.strip().upper()
    if catalog_service.get_form(code) is None:
        raise HTTPException(status_code=404, detail=f"Unknown form '{code}'")
    return code


@router.post("/forms/{form_code}/preview-fill")
def preview_fill(form_code: str, payload: FillPayload) -> dict:
    code = _ensure_form(form_code)
    return fill_service.preview_fill(code, payload).model_dump()


@router.post("/forms/{form_code}/fill")
def fill(form_code: str, payload: FillPayload) -> dict:
    code = _ensure_form(form_code)
    return fill_service.execute_fill(code, payload).model_dump()


@router.post("/forms/{form_code}/fill-from-model")
def fill_from_model(form_code: str, payload: ModelFillPayload) -> dict:
    code = _ensure_form(form_code)
    model = model_service.validate_model_payload(code, payload.model_payload)
    return fill_service.execute_fill_from_model(code, model, payload.output_name).model_dump()


@router.get("/artifacts/{file_id}")
def download_artifact(file_id: str) -> FileResponse:
    try:
        path = fill_service.get_artifact_path(file_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Unknown artifact '{file_id}'")
    return FileResponse(path, media_type="application/pdf", filename=path.name)