"""
Tests for API key authentication.

The ``require_api_key`` dependency reads ``MERCURIO_API_KEY`` at request time,
so ``monkeypatch`` (function-scoped) is sufficient to control it per test even
though ``client`` is session-scoped.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

_API_READ_ROUTE = "/api/v1/forms"
_TEST_KEY = "test-secret-key-abc"


class TestNoKeyConfigured:
    def test_request_without_credentials_succeeds(self, client: TestClient, monkeypatch):
        monkeypatch.delenv("MERCURIO_API_KEY", raising=False)
        assert client.get(_API_READ_ROUTE).status_code == 200

    def test_request_with_any_header_still_succeeds(self, client: TestClient, monkeypatch):
        monkeypatch.delenv("MERCURIO_API_KEY", raising=False)
        resp = client.get(_API_READ_ROUTE, headers={"Authorization": "Bearer whatever"})
        assert resp.status_code == 200


class TestKeyConfigured:
    def test_missing_credentials_returns_401(self, client: TestClient, monkeypatch):
        monkeypatch.setenv("MERCURIO_API_KEY", _TEST_KEY)
        assert client.get(_API_READ_ROUTE).status_code == 401

    def test_wrong_bearer_token_returns_401(self, client: TestClient, monkeypatch):
        monkeypatch.setenv("MERCURIO_API_KEY", _TEST_KEY)
        resp = client.get(_API_READ_ROUTE, headers={"Authorization": "Bearer wrong-key"})
        assert resp.status_code == 401

    def test_correct_bearer_token_returns_200(self, client: TestClient, monkeypatch):
        monkeypatch.setenv("MERCURIO_API_KEY", _TEST_KEY)
        resp = client.get(_API_READ_ROUTE, headers={"Authorization": f"Bearer {_TEST_KEY}"})
        assert resp.status_code == 200

    def test_correct_x_api_key_header_returns_200(self, client: TestClient, monkeypatch):
        monkeypatch.setenv("MERCURIO_API_KEY", _TEST_KEY)
        # FastAPI maps x_api_key parameter to header name "x-api-key"
        resp = client.get(_API_READ_ROUTE, headers={"x-api-key": _TEST_KEY})
        assert resp.status_code == 200

    def test_bearer_prefix_is_case_insensitive(self, client: TestClient, monkeypatch):
        monkeypatch.setenv("MERCURIO_API_KEY", _TEST_KEY)
        resp = client.get(_API_READ_ROUTE, headers={"Authorization": f"BEARER {_TEST_KEY}"})
        assert resp.status_code == 200

    def test_401_response_has_detail(self, client: TestClient, monkeypatch):
        monkeypatch.setenv("MERCURIO_API_KEY", _TEST_KEY)
        body = client.get(_API_READ_ROUTE).json()
        assert "detail" in body
