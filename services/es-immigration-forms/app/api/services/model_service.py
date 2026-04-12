from __future__ import annotations

import importlib
from typing import Any

from pydantic import BaseModel


def get_form_model_class(form_code: str) -> type[BaseModel]:
    code = form_code.strip().upper()
    module = importlib.import_module(f"app.models.{code.lower()}")
    class_name = f"{code}FormSchema"
    model_class = getattr(module, class_name, None)
    if model_class is None:
        raise ValueError(f"Model class '{class_name}' not found for form {code}")
    return model_class


def validate_model_payload(form_code: str, payload: dict[str, Any]) -> BaseModel:
    model_class = get_form_model_class(form_code)
    return model_class.model_validate(payload)