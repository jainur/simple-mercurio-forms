from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ApiErrorDetail(BaseModel):
    path: str | None = None
    message: str


class ApiError(BaseModel):
    code: str
    message: str
    details: list[ApiErrorDetail] = Field(default_factory=list)


class EnvelopeMeta(BaseModel):
    request_id: str


class SuccessEnvelope(BaseModel):
    data: Any
    meta: EnvelopeMeta


class ErrorEnvelope(BaseModel):
    error: ApiError
    meta: EnvelopeMeta