"""
Tests for the fill, preview-fill, fill-from-model, and artifact-download routes.

Every test that triggers a PDF write uses the ``tmp_fill_dir`` fixture to redirect
output away from the real forms/filled/api/ directory.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

KNOWN_FORM = "EX11"
UNKNOWN_FORM = "EX99"
EX11_FIELD_COUNT = 84


# ---------------------------------------------------------------------------
# Preview fill (dry-run, no PDF written)
# ---------------------------------------------------------------------------

class TestPreviewFill:
    def test_valid_payload_returns_200(self, client: TestClient, ex11_direct_payload):
        assert (
            client.post(f"/api/v1/forms/{KNOWN_FORM}/preview-fill", json=ex11_direct_payload).status_code == 200
        )

    def test_unknown_form_returns_404(self, client: TestClient):
        assert client.post(f"/api/v1/forms/{UNKNOWN_FORM}/preview-fill", json={}).status_code == 404

    def test_body_has_required_keys(self, client: TestClient, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/preview-fill", json=ex11_direct_payload).json()
        assert {"form_code", "assigned_fields", "assignments", "warnings"} <= body.keys()

    def test_form_code_matches(self, client: TestClient, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/preview-fill", json=ex11_direct_payload).json()
        assert body["form_code"] == KNOWN_FORM

    def test_full_payload_assigns_all_fields(self, client: TestClient, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/preview-fill", json=ex11_direct_payload).json()
        assert body["assigned_fields"] == EX11_FIELD_COUNT

    def test_assignments_dict_has_correct_count(self, client: TestClient, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/preview-fill", json=ex11_direct_payload).json()
        assert len(body["assignments"]) == EX11_FIELD_COUNT

    def test_empty_payload_assigns_zero_fields(self, client: TestClient):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/preview-fill", json={}).json()
        assert body["assigned_fields"] == 0

    def test_no_pdf_is_written(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        client.post(f"/api/v1/forms/{KNOWN_FORM}/preview-fill", json=ex11_direct_payload)
        assert list(tmp_fill_dir.iterdir()) == []


# ---------------------------------------------------------------------------
# Fill (generates PDF)
# ---------------------------------------------------------------------------

class TestFill:
    def test_valid_payload_returns_200(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        assert client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=ex11_direct_payload).status_code == 200

    def test_unknown_form_returns_404(self, client: TestClient, tmp_fill_dir):
        assert client.post(f"/api/v1/forms/{UNKNOWN_FORM}/fill", json={}).status_code == 404

    def test_body_has_fill_result_keys(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=ex11_direct_payload).json()
        assert {"form_code", "file_id", "file_name", "download_url", "output_path", "assignment_summary"} <= body.keys()

    def test_pdf_is_created_in_output_dir(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=ex11_direct_payload)
        assert len(list(tmp_fill_dir.glob("*.pdf"))) == 1

    def test_assignment_summary_counts_all_fields(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=ex11_direct_payload).json()
        assert body["assignment_summary"]["assigned_fields"] == EX11_FIELD_COUNT

    def test_custom_output_name_is_honoured(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        payload = {**ex11_direct_payload, "output_name": "my-named-output.pdf"}
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=payload).json()
        assert body["file_name"] == "my-named-output.pdf"
        assert (tmp_fill_dir / "my-named-output.pdf").exists()

    def test_download_url_points_to_artifact_endpoint(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=ex11_direct_payload).json()
        assert body["download_url"].startswith("/api/v1/artifacts/")

    def test_file_id_matches_file_name(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=ex11_direct_payload).json()
        assert body["file_id"] == body["file_name"]

    def test_warning_count_is_non_negative(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=ex11_direct_payload).json()
        assert body["assignment_summary"]["warning_count"] >= 0

    def test_output_name_without_pdf_extension_gets_extension(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        payload = {**ex11_direct_payload, "output_name": "no-extension"}
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=payload).json()
        assert body["file_name"].endswith(".pdf")


# ---------------------------------------------------------------------------
# Fill from domain model
# ---------------------------------------------------------------------------

class TestFillFromModel:
    def test_valid_model_returns_200(self, client: TestClient, tmp_fill_dir, ex11_model_payload):
        resp = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/fill-from-model",
            json={"model_payload": ex11_model_payload},
        )
        assert resp.status_code == 200

    def test_invalid_model_returns_422(self, client: TestClient, tmp_fill_dir, ex11_model_payload):
        bad = {
            **ex11_model_payload,
            "foreigner_details": {**ex11_model_payload["foreigner_details"], "gender": "MUJER"},
        }
        assert (
            client.post(f"/api/v1/forms/{KNOWN_FORM}/fill-from-model", json={"model_payload": bad}).status_code == 422
        )

    def test_invalid_model_error_code_is_model_validation_error(self, client: TestClient, tmp_fill_dir, ex11_model_payload):
        bad = {
            **ex11_model_payload,
            "foreigner_details": {**ex11_model_payload["foreigner_details"], "gender": "MUJER"},
        }
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/fill-from-model", json={"model_payload": bad}
        ).json()
        assert body["error"]["code"] == "MODEL_VALIDATION_ERROR"

    def test_invalid_model_details_name_the_bad_field(self, client: TestClient, tmp_fill_dir, ex11_model_payload):
        bad = {
            **ex11_model_payload,
            "foreigner_details": {**ex11_model_payload["foreigner_details"], "gender": "MUJER"},
        }
        details = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/fill-from-model", json={"model_payload": bad}
        ).json()["error"]["details"]
        assert any("gender" in d["path"] for d in details)

    def test_valid_model_assigns_all_fields(self, client: TestClient, tmp_fill_dir, ex11_model_payload):
        payload = {"model_payload": ex11_model_payload, "output_name": "model-fill-test.pdf"}
        body = client.post(f"/api/v1/forms/{KNOWN_FORM}/fill-from-model", json=payload).json()
        assert body["assignment_summary"]["assigned_fields"] == EX11_FIELD_COUNT

    def test_valid_model_creates_pdf(self, client: TestClient, tmp_fill_dir, ex11_model_payload):
        payload = {"model_payload": ex11_model_payload, "output_name": "model-created.pdf"}
        client.post(f"/api/v1/forms/{KNOWN_FORM}/fill-from-model", json=payload)
        assert (tmp_fill_dir / "model-created.pdf").exists()

    def test_unknown_form_returns_404(self, client: TestClient, tmp_fill_dir, ex11_model_payload):
        assert (
            client.post(
                f"/api/v1/forms/{UNKNOWN_FORM}/fill-from-model",
                json={"model_payload": ex11_model_payload},
            ).status_code
            == 404
        )

    def test_error_envelope_has_meta_with_request_id(self, client: TestClient, tmp_fill_dir, ex11_model_payload):
        bad = {
            **ex11_model_payload,
            "foreigner_details": {**ex11_model_payload["foreigner_details"], "gender": "MUJER"},
        }
        body = client.post(
            f"/api/v1/forms/{KNOWN_FORM}/fill-from-model", json={"model_payload": bad}
        ).json()
        assert "meta" in body
        assert "request_id" in body["meta"]


# ---------------------------------------------------------------------------
# Artifact download
# ---------------------------------------------------------------------------

class TestArtifactDownload:
    def test_download_after_fill_returns_200(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        payload = {**ex11_direct_payload, "output_name": "dl-test.pdf"}
        client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=payload)
        assert client.get("/api/v1/artifacts/dl-test.pdf").status_code == 200

    def test_download_returns_pdf_content_type(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        payload = {**ex11_direct_payload, "output_name": "ct-test.pdf"}
        client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=payload)
        resp = client.get("/api/v1/artifacts/ct-test.pdf")
        assert "application/pdf" in resp.headers.get("content-type", "")

    def test_download_returns_non_empty_body(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        payload = {**ex11_direct_payload, "output_name": "size-test.pdf"}
        client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=payload)
        assert len(client.get("/api/v1/artifacts/size-test.pdf").content) > 10_000

    def test_download_sets_content_disposition_filename(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        payload = {**ex11_direct_payload, "output_name": "named-dl.pdf"}
        client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=payload)
        resp = client.get("/api/v1/artifacts/named-dl.pdf")
        content_disp = resp.headers.get("content-disposition", "")
        assert "named-dl.pdf" in content_disp

    def test_unknown_artifact_returns_404(self, client: TestClient, tmp_fill_dir):
        assert client.get("/api/v1/artifacts/does-not-exist.pdf").status_code == 404

    def test_response_has_x_request_id_header(self, client: TestClient, tmp_fill_dir, ex11_direct_payload):
        payload = {**ex11_direct_payload, "output_name": "header-test.pdf"}
        client.post(f"/api/v1/forms/{KNOWN_FORM}/fill", json=payload)
        resp = client.get("/api/v1/artifacts/header-test.pdf")
        assert "x-request-id" in resp.headers
