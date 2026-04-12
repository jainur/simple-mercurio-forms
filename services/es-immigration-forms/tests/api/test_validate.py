from __future__ import annotations

from fastapi.testclient import TestClient

KNOWN_FORM = "EX11"
UNKNOWN_FORM = "EX99"


class TestValidateFillPayload:
    def test_valid_payload_is_valid(self, client: TestClient, ex11_direct_payload):
        resp = client.post(f"/api/v1/forms/{KNOWN_FORM}/validate", json=ex11_direct_payload)
        assert resp.status_code == 200
        assert resp.json()["valid"] is True

    def test_valid_payload_has_no_errors(self, client: TestClient, ex11_direct_payload):
        assert client.post(f"/api/v1/forms/{KNOWN_FORM}/validate", json=ex11_direct_payload).json()["errors"] == []

    def test_unknown_field_makes_payload_invalid(self, client: TestClient):
        payload = {"field_values": {"NonExistentFieldXYZ999": "value"}}
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/validate", json=payload).json()
        assert body["valid"] is False

    def test_unknown_field_error_has_unknown_field_code(self, client: TestClient):
        payload = {"field_values": {"NonExistentFieldXYZ999": "value"}}
        errors = client.post(f"/api/v1/forms/{KNOWN_FORM}/validate", json=payload).json()["errors"]
        assert any(e["code"] == "UNKNOWN_FIELD" for e in errors)

    def test_unknown_field_error_references_field_path(self, client: TestClient):
        payload = {"field_values": {"NonExistentFieldXYZ999": "value"}}
        errors = client.post(f"/api/v1/forms/{KNOWN_FORM}/validate", json=payload).json()["errors"]
        assert any("NonExistentFieldXYZ999" in (e.get("path") or "") for e in errors)

    def test_empty_payload_is_valid(self, client: TestClient):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/validate", json={}).json()
        assert body["valid"] is True

    def test_response_contains_form_code(self, client: TestClient, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/validate", json=ex11_direct_payload).json()
        assert body["form_code"] == KNOWN_FORM

    def test_unknown_form_returns_404(self, client: TestClient):
        assert client.post(f"/api/v1/forms/{UNKNOWN_FORM}/validate", json={}).status_code == 404


class TestValidateModel:
    def test_valid_model_is_valid(self, client: TestClient, ex11_model_payload):
        resp = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-model",
            json={"model_payload": ex11_model_payload},
        )
        assert resp.status_code == 200
        assert resp.json()["valid"] is True

    def test_valid_model_has_no_errors(self, client: TestClient, ex11_model_payload):
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-model",
            json={"model_payload": ex11_model_payload},
        ).json()
        assert body["errors"] == []

    def test_invalid_enum_value_is_invalid(self, client: TestClient, ex11_model_payload):
        bad = {
            **ex11_model_payload,
            "foreigner_details": {**ex11_model_payload["foreigner_details"], "gender": "MUJER"},
        }
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-model", json={"model_payload": bad}
        ).json()
        assert body["valid"] is False

    def test_invalid_enum_error_message_names_the_field(self, client: TestClient, ex11_model_payload):
        bad = {
            **ex11_model_payload,
            "foreigner_details": {**ex11_model_payload["foreigner_details"], "gender": "MUJER"},
        }
        errors = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-model", json={"model_payload": bad}
        ).json()["errors"]
        assert any("gender" in e["message"].lower() for e in errors)

    def test_missing_required_section_is_invalid(self, client: TestClient, ex11_model_payload):
        # Drop the required request_details section.
        incomplete = {k: v for k, v in ex11_model_payload.items() if k != "request_details"}
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-model", json={"model_payload": incomplete}
        ).json()
        assert body["valid"] is False

    def test_response_contains_form_code(self, client: TestClient, ex11_model_payload):
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-model",
            json={"model_payload": ex11_model_payload},
        ).json()
        assert body["form_code"] == KNOWN_FORM

    def test_unknown_form_returns_404(self, client: TestClient, ex11_model_payload):
        assert client.post(
            f"/api/v1/forms/{UNKNOWN_FORM}/validate-model",
            json={"model_payload": ex11_model_payload},
        ).status_code == 404


class TestValidateMapping:
    def test_full_payload_returns_200(self, client: TestClient, ex11_direct_payload):
        assert (
            client.post(
                f"/api/v1/forms/{KNOWN_FORM}/validate-mapping",
                json={"payload": ex11_direct_payload},
            ).status_code
            == 200
        )

    def test_full_payload_is_valid(self, client: TestClient, ex11_direct_payload):
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-mapping",
            json={"payload": ex11_direct_payload},
        ).json()
        assert body["valid"] is True

    def test_full_payload_assigns_all_fields(self, client: TestClient, ex11_direct_payload):
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-mapping",
            json={"payload": ex11_direct_payload},
        ).json()
        assert body["assigned_fields"] == 84

    def test_definition_field_count_is_positive(self, client: TestClient, ex11_direct_payload):
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-mapping",
            json={"payload": ex11_direct_payload},
        ).json()
        assert body["definition_field_count"] > 0

    def test_empty_payload_assigns_zero_fields(self, client: TestClient):
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-mapping", json={"payload": {}}
        ).json()
        assert body["assigned_fields"] == 0

    def test_extra_field_is_detected(self, client: TestClient):
        payload = {"field_values": {"GhostFieldABC123": "test"}}
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-mapping", json={"payload": payload}
        ).json()
        assert "GhostFieldABC123" in body["extra_assignment_fields"]

    def test_strict_mode_flags_blank_text_field(self, client: TestClient):
        payload = {"field_values": {"Texto1": ""}}
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-mapping",
            json={"payload": payload, "strict_text_fields": True},
        ).json()
        assert "Texto1" in body["blank_text_fields"]

    def test_strict_mode_off_does_not_flag_blank_field(self, client: TestClient):
        payload = {"field_values": {"Texto1": ""}}
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/validate-mapping",
            json={"payload": payload, "strict_text_fields": False},
        ).json()
        # Blanks should be in the list but valid should still be True (no missing/extra)
        assert body["valid"] is True

    def test_unknown_form_returns_404(self, client: TestClient):
        assert (
            client.post(
                f"/api/v1/forms/{UNKNOWN_FORM}/validate-mapping", json={"payload": {}}
            ).status_code
            == 404
        )
