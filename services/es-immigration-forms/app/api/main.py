from __future__ import annotations

import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.api.routers import fill, forms, health, validate

app = FastAPI(
    title="Simple Mercurio Forms API",
    version="0.1.0",
    description="HTTP API for form metadata, validation, and PDF filling.",
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "REQUEST_VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": [
                    {
                        "path": ".".join(str(item) for item in err["loc"]),
                        "message": err["msg"],
                    }
                    for err in exc.errors()
                ],
            },
            "meta": {"request_id": request_id},
        },
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "MODEL_VALIDATION_ERROR",
                "message": "Model payload validation failed",
                "details": [
                    {
                        "path": ".".join(str(item) for item in err["loc"]),
                        "message": err["msg"],
                    }
                    for err in exc.errors()
                ],
            },
            "meta": {"request_id": request_id},
        },
    )


@app.get("/")
def root() -> dict:
    return {
        "service": "simple-mercurio-forms-api",
        "version": app.version,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
    }


app.include_router(health.router)
app.include_router(forms.router, prefix="/api/v1")
app.include_router(validate.router, prefix="/api/v1")
app.include_router(fill.router, prefix="/api/v1")