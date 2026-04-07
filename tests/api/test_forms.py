from __future__ import annotations

from fastapi.testclient import TestClient

EXPECTED_FORM_COUNT = 25
KNOWN_FORM = "EX11"
UNKNOWN_FORM = "EX99"
EX11_FIELD_COUNT = 84


class TestListForms:
    def test_returns_200(self, client: TestClient):
        assert client.get("/api/v1/forms").status_code == 200

    def test_returns_list(self, client: TestClient):
        assert isinstance(client.get("/api/v1/forms").json(), list)

    def test_known_form_count(self, client: TestClient):
        assert len(client.get("/api/v1/forms").json()) == EXPECTED_FORM_COUNT

    def test_each_item_has_required_keys(self, client: TestClient):
        required = {"form_code", "filename", "field_count", "page_count", "supported_fill_modes"}
        for item in client.get("/api/v1/forms").json():
            assert required <= item.keys()

    def test_supported_fill_modes_advertised(self, client: TestClient):
        expected = {"field_values", "semantic_values", "domain_model"}
        for item in client.get("/api/v1/forms").json():
            assert set(item["supported_fill_modes"]) == expected

    def test_forms_ordered_by_code(self, client: TestClient):
        codes = [item["form_code"] for item in client.get("/api/v1/forms").json()]
        assert codes == sorted(codes)


class TestGetForm:
    def test_known_form_returns_200(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{KNOWN_FORM}").status_code == 200

    def test_unknown_form_returns_404(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{UNKNOWN_FORM}").status_code == 404

    def test_body_has_correct_form_code(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{KNOWN_FORM}").json()["form_code"] == KNOWN_FORM

    def test_body_has_sections_list(self, client: TestClient):
        body = client.get(f"/api/v1/forms/{KNOWN_FORM}").json()
        assert isinstance(body["sections"], list)
        assert len(body["sections"]) > 0

    def test_body_has_positive_field_count(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{KNOWN_FORM}").json()["field_count"] > 0

    def test_body_has_positive_page_count(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{KNOWN_FORM}").json()["page_count"] > 0

    def test_lowercase_form_code_accepted(self, client: TestClient):
        assert client.get("/api/v1/forms/ex11").status_code == 200

    def test_lowercase_and_uppercase_return_same_data(self, client: TestClient):
        upper = client.get("/api/v1/forms/EX11").json()
        lower = client.get("/api/v1/forms/ex11").json()
        assert upper["form_code"] == lower["form_code"]
        assert upper["field_count"] == lower["field_count"]

    def test_has_domain_example_flag(self, client: TestClient):
        body = client.get(f"/api/v1/forms/{KNOWN_FORM}").json()
        assert "has_domain_example" in body
        assert body["has_domain_example"] is True


class TestGetFormFields:
    def test_known_form_returns_200(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{KNOWN_FORM}/fields").status_code == 200

    def test_unknown_form_returns_404(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{UNKNOWN_FORM}/fields").status_code == 404

    def test_returns_non_empty_list(self, client: TestClient):
        assert len(client.get(f"/api/v1/forms/{KNOWN_FORM}/fields").json()) > 0

    def test_count_matches_form_metadata(self, client: TestClient):
        fields = client.get(f"/api/v1/forms/{KNOWN_FORM}/fields").json()
        form = client.get(f"/api/v1/forms/{KNOWN_FORM}").json()
        assert len(fields) == form["field_count"]

    def test_each_field_has_name_and_type(self, client: TestClient):
        for field in client.get(f"/api/v1/forms/{KNOWN_FORM}/fields").json():
            assert "name" in field
            assert "type" in field
            assert field["name"]

    def test_type_filter_returns_only_text_fields(self, client: TestClient):
        body = client.get(f"/api/v1/forms/{KNOWN_FORM}/fields?type=Text").json()
        assert len(body) > 0
        assert all(f["type"] == "Text" for f in body)

    def test_type_filter_returns_only_checkbox_fields(self, client: TestClient):
        body = client.get(f"/api/v1/forms/{KNOWN_FORM}/fields?type=CheckBox").json()
        assert len(body) > 0
        assert all(f["type"] == "CheckBox" for f in body)

    def test_page_filter_returns_subset(self, client: TestClient):
        all_fields = client.get(f"/api/v1/forms/{KNOWN_FORM}/fields").json()
        page1 = client.get(f"/api/v1/forms/{KNOWN_FORM}/fields?page=1").json()
        assert 0 < len(page1) < len(all_fields)

    def test_page_filter_only_contains_that_page(self, client: TestClient):
        page1 = client.get(f"/api/v1/forms/{KNOWN_FORM}/fields?page=1").json()
        assert all(f["page"] == 1 for f in page1)

    def test_unknown_type_returns_empty_list(self, client: TestClient):
        body = client.get(f"/api/v1/forms/{KNOWN_FORM}/fields?type=NonExistentType").json()
        assert body == []

    def test_each_field_has_raw_dict(self, client: TestClient):
        for field in client.get(f"/api/v1/forms/{KNOWN_FORM}/fields?page=1").json():
            assert isinstance(field["raw"], dict)


class TestGetFormSections:
    def test_known_form_returns_200(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{KNOWN_FORM}/sections").status_code == 200

    def test_unknown_form_returns_404(self, client: TestClient):
        assert client.get(f"/api/v1/forms/{UNKNOWN_FORM}/sections").status_code == 404

    def test_returns_non_empty_list(self, client: TestClient):
        assert len(client.get(f"/api/v1/forms/{KNOWN_FORM}/sections").json()) > 0

    def test_each_section_has_field_count(self, client: TestClient):
        for section in client.get(f"/api/v1/forms/{KNOWN_FORM}/sections").json():
            assert "field_count" in section
            assert section["field_count"] > 0

    def test_section_field_counts_sum_to_total(self, client: TestClient):
        sections = client.get(f"/api/v1/forms/{KNOWN_FORM}/sections").json()
        total = sum(s["field_count"] for s in sections)
        form = client.get(f"/api/v1/forms/{KNOWN_FORM}").json()
        assert total == form["field_count"]
