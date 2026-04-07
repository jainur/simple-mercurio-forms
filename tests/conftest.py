"""
Shared pytest fixtures for the API test suite.

Scope strategy
--------------
- ``client``               session-scoped: one TestClient for the whole run (fast).
- ``ex11_direct_payload``  session-scoped: read once from disk.
- ``ex11_model_payload``   session-scoped: static dict.
- ``tmp_fill_dir``         function-scoped: redirects fill output to pytest's tmp_path
                           so tests never write into the real forms/filled/api/ directory.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Shared HTTP client
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def client() -> TestClient:
    """Single TestClient reused for all read-only and non-file-writing tests."""
    return TestClient(app)


# ---------------------------------------------------------------------------
# EX11 payload fixtures (known-good form with full example data)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def ex11_direct_payload() -> dict:
    """
    Raw field_values payload from examples/ex11-input.json.
    The _comment key is stripped before return.
    """
    data = json.loads((ROOT / "examples" / "ex11-input.json").read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


@pytest.fixture(scope="session")
def ex11_model_payload() -> dict:
    """
    Valid EX11 domain model dict.
    Enum values must use raw enum codes (e.g. 'M' for GenderEnum.FEMALE).
    """
    return {
        "foreigner_details": {
            "passport": "AB1234567",
            "nie": None,
            "first_surname": "GARCIA",
            "second_surname": "LOPEZ",
            "name": "ANA",
            "gender": "M",
            "date_of_birth": "1988-04-16",
            "birth_place": "Quito",
            "birth_country": "Ecuador",
            "nationality": "Ecuatoriana",
            "father_name": "CARLOS GARCIA",
            "mother_name": "MARTA LOPEZ",
            "address": "Calle Serrano",
            "address_number": "45",
            "floor_door": "2A",
            "city": "Madrid",
            "postal_code": "28001",
            "province": "Madrid",
            "mobile_phone": "600111999",
            "email": "ana.garcia@example.com",
            "legal_guardian_name": None,
            "legal_guardian_id": None,
            "legal_guardian_title": None,
            "marital_status": "S",
            "children_in_school_age": False,
        },
        "filing_representative": {
            "name_or_company": "GESTORIA INTEGRAL SL",
            "id_number": "B22446688",
            "address": "Paseo de la Castellana",
            "address_number": "100",
            "floor_door": "5",
            "city": "Madrid",
            "postal_code": "28046",
            "province": "Madrid",
            "mobile_phone": "911223344",
            "email": "tramites@gestoriaintegral.es",
            "legal_rep_name": "LAURA RAMOS",
            "legal_rep_id": "11223344Z",
            "legal_rep_title": "Apoderada",
        },
        "notification_address": {
            "name_or_company": "GESTORIA INTEGRAL SL",
            "id_number": "B22446688",
            "address": "Paseo de la Castellana",
            "address_number": "100",
            "floor_door": "5",
            "city": "Madrid",
            "postal_code": "28046",
            "province": "Madrid",
            "mobile_phone": "911223344",
            "email": "notificaciones@gestoriaintegral.es",
            "consent_electronic_notifications": True,
        },
        "request_details": {
            "authorization_family": "RESIDENCIA_LARGA_DURACION",
            "ld_subtype": "GENERAL_5_YEARS_ART_183_1",
            "ld_ue_subtype": None,
        },
        "signature": {
            "place": "Madrid",
            "day": "06",
            "month": "04",
            "year": "2026",
            "name": "ANA GARCIA LOPEZ",
        },
        "office": {
            "target_office": "Oficina de Extranjeria de Madrid",
            "dir3_code": "E04921901",
            "province": "Madrid",
        },
    }


# ---------------------------------------------------------------------------
# Fill output isolation
# ---------------------------------------------------------------------------

@pytest.fixture()
def tmp_fill_dir(tmp_path, monkeypatch):
    """
    Redirect api.services.fill_service.API_FILLED_DIR to a fresh tmp directory.

    This prevents fill tests from writing into forms/filled/api/ and ensures
    each test starts with an empty output directory.
    """
    import api.services.fill_service as fill_svc
    monkeypatch.setattr(fill_svc, "API_FILLED_DIR", tmp_path)
    return tmp_path
