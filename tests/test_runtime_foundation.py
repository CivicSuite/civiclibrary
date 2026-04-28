from fastapi.testclient import TestClient

from civiclibrary import __version__
from civiclibrary.main import app

client = TestClient(app)


def test_root_reports_honest_current_state():
    payload = client.get("/").json()
    assert payload["name"] == "CivicLibrary"
    assert payload["version"] == __version__
    assert "patron record access" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    assert client.get("/health").json() == {
        "status": "ok",
        "service": "civiclibrary",
        "version": "0.1.0",
        "civiccore_version": "0.2.0",
    }


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civiclibrary").text
    assert "CivicLibrary v0.1.0" in text
    assert "No patron record access" in text
    assert "civiccore==0.2.0" in text


def test_api_endpoints_return_deterministic_payloads():
    policy = client.post(
        "/api/v1/civiclibrary/policy-answer",
        json={"question": "meeting rooms"},
    ).json()
    assert policy["librarian_review_required"] is True

    program = client.post(
        "/api/v1/civiclibrary/program-answer",
        json={
            "question": "teen events",
            "programs": [
                {
                    "title": "Teen craft night",
                    "audience": "teens",
                    "date": "2026-05-10",
                    "accessibility_note": "Accessible room",
                }
            ],
        },
    ).json()
    assert program["accessibility_review_required"] is True

    reference = client.post(
        "/api/v1/civiclibrary/reference-search",
        json={"query": "local history"},
    ).json()
    assert reference["patron_records_excluded"] is True

    guidance = client.post(
        "/api/v1/civiclibrary/collection-guidance",
        json={"topic": "local history", "considerations": ["community demand"]},
    ).json()
    assert guidance["librarian_review_required"] is True
