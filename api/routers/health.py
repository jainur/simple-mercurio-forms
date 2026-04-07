from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health/live")
def live() -> dict:
    return {"status": "ok"}


@router.get("/health/ready")
def ready() -> dict:
    root = Path(__file__).resolve().parents[2]
    db_exists = (root / "forms.db").exists()
    definitions_exist = (root / "forms" / "definitions").exists()
    return {
        "status": "ok" if db_exists and definitions_exist else "degraded",
        "checks": {
            "forms_db": db_exists,
            "definitions_dir": definitions_exist,
        },
    }