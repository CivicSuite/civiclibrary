from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civiclibrary.main import app, _dispose_workpaper_repository
from civiclibrary.persistence import LibraryWorkpaperRepository
from civiclibrary.programs import LibraryProgram


client = TestClient(app)
PROGRAM = LibraryProgram("Teen craft night", "teens", "2026-05-10", "Accessible room")


def test_repository_persists_program_answer_and_collection_guidance(tmp_path: Path) -> None:
    db_path = tmp_path / "civiclibrary.db"
    db_url = f"sqlite+pysqlite:///{db_path.as_posix()}"
    repository = LibraryWorkpaperRepository(db_url=db_url)
    answer = repository.create_program_answer(question="teen events", programs=[PROGRAM])
    guidance = repository.create_collection_guidance(
        topic="local history", considerations=["community demand"]
    )
    repository.engine.dispose()
    reloaded = LibraryWorkpaperRepository(db_url=db_url)
    stored_answer = reloaded.get_program_answer(answer.answer_id)
    stored_guidance = reloaded.get_collection_guidance(guidance.guidance_id)
    reloaded.engine.dispose()
    assert stored_answer is not None
    assert stored_answer.accessibility_review_required is True
    assert stored_guidance is not None
    assert stored_guidance.librarian_review_required is True
    db_path.unlink()


def test_library_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiclibrary-api.db"
    monkeypatch.setenv("CIVICLIBRARY_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()
    created_answer = client.post(
        "/api/v1/civiclibrary/program-answer",
        json={"question": "teen events", "programs": [PROGRAM.__dict__]},
    )
    answer_id = created_answer.json()["answer_id"]
    fetched_answer = client.get(f"/api/v1/civiclibrary/program-answer/{answer_id}")
    created_guidance = client.post(
        "/api/v1/civiclibrary/collection-guidance",
        json={"topic": "local history", "considerations": ["community demand"]},
    )
    guidance_id = created_guidance.json()["guidance_id"]
    fetched_guidance = client.get(f"/api/v1/civiclibrary/collection-guidance/{guidance_id}")
    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICLIBRARY_WORKPAPER_DB_URL")
    assert created_answer.status_code == 200
    assert fetched_answer.status_code == 200
    assert fetched_answer.json()["programs"][0]["title"] == "Teen craft night"
    assert created_guidance.status_code == 200
    assert fetched_guidance.status_code == 200
    assert fetched_guidance.json()["topic"] == "local history"
    db_path.unlink()


def test_get_program_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICLIBRARY_WORKPAPER_DB_URL", raising=False)
    _dispose_workpaper_repository()
    response = client.get("/api/v1/civiclibrary/program-answer/example")
    assert response.status_code == 503
    assert "Set CIVICLIBRARY_WORKPAPER_DB_URL" in response.json()["detail"]["fix"]


def test_get_guidance_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiclibrary-missing.db"
    monkeypatch.setenv("CIVICLIBRARY_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()
    response = client.get("/api/v1/civiclibrary/collection-guidance/missing")
    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICLIBRARY_WORKPAPER_DB_URL")
    assert response.status_code == 404
    assert "POST /api/v1/civiclibrary/collection-guidance" in response.json()["detail"]["fix"]
    db_path.unlink()
