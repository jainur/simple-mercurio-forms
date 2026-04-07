"""
Registry that maps domain model modules to form codes and their mapper functions.

The mapping is derived by convention: models.exNN  →  form code EXNN, mapper mappers.exNN.
All 25 active form codes are declared explicitly so accidental module name drifts are caught early.
"""

from __future__ import annotations

import importlib
import re
from typing import Callable

# All active form codes in the system.
_KNOWN_CODES: frozenset[str] = frozenset({
    "EX00", "EX01", "EX02", "EX03", "EX04",
    "EX06", "EX07", "EX09", "EX10", "EX11",
    "EX13", "EX16", "EX17", "EX18", "EX19",
    "EX20", "EX21", "EX22", "EX23", "EX24",
    "EX25", "EX26", "EX28", "EX29", "EX30",
})

_MODULE_PATTERN = re.compile(r"^models\.(ex\d+)$", re.IGNORECASE)


def get_form_code_for_model_module(model_module: str) -> str:
    """
    Derive the form code from a model module name.

    Examples
    --------
    >>> get_form_code_for_model_module("models.ex21")
    'EX21'
    >>> get_form_code_for_model_module("models.ex00")
    'EX00'
    """
    match = _MODULE_PATTERN.match(model_module)
    if not match:
        raise ValueError(
            f"Cannot derive form code from module '{model_module}'. "
            "Expected pattern: models.exNN"
        )
    code = match.group(1).upper()
    if code not in _KNOWN_CODES:
        raise ValueError(
            f"Form code '{code}' derived from '{model_module}' is not in the known registry. "
            f"Known codes: {sorted(_KNOWN_CODES)}"
        )
    return code


def get_mapper_function(form_code: str) -> Callable:
    """
    Return the ``to_field_values`` callable for the given form code.

    Parameters
    ----------
    form_code : str
        Upper-case form code, e.g. ``'EX21'``.

    Returns
    -------
    Callable
        The ``to_field_values(form) -> dict`` function from the matching mapper module.
    """
    code = form_code.strip().upper()
    if code not in _KNOWN_CODES:
        raise ValueError(
            f"No mapper registered for form code '{code}'. "
            f"Known codes: {sorted(_KNOWN_CODES)}"
        )
    mapper_module_name = f"mappers.{code.lower()}"
    mapper_module = importlib.import_module(mapper_module_name)
    return mapper_module.to_field_values
