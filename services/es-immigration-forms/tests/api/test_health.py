from __future__ import annotations

from fastapi.testclient import TestClient


class TestHealthLive:
    def test_returns_200(self, client: TestClient):
        assert client.get("/health/live").status_code == 200

    def test_body_is_ok(self, client: TestClient):
        assert client.get("/health/live").json() == {"status": "ok"}


class TestHealthReady:
    def test_returns_200(self, client: TestClient):
        assert client.get("/health/ready").status_code == 200

    def test_body_has_status_and_checks_keys(self, client: TestClient):
        body = client.get("/health/ready").json()
        assert "status" in body
        assert "checks" in body

    def test_checks_contains_db_and_definitions(self, client: TestClient):
        checks = client.get("/health/ready").json()["checks"]
        assert "forms_db" in checks
        assert "definitions_dir" in checks

    def test_status_is_ok_when_deps_present(self, client: TestClient):
        # The workspace always has forms.db and forms/definitions/ present.
        assert client.get("/health/ready").json()["status"] == "ok"

    def test_db_check_is_true(self, client: TestClient):
        assert client.get("/health/ready").json()["checks"]["forms_db"] is True

    def test_definitions_check_is_true(self, client: TestClient):
        assert client.get("/health/ready").json()["checks"]["definitions_dir"] is True
