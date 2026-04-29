"""FastAPI runtime foundation for CivicLibrary."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civiclibrary import __version__
from civiclibrary.collection import draft_collection_guidance
from civiclibrary.policy import LibraryPolicySource, answer_policy_question
from civiclibrary.persistence import (
    LibraryWorkpaperRepository,
    StoredCollectionGuidance,
    StoredProgramAnswer,
)
from civiclibrary.programs import LibraryProgram, answer_program_question
from civiclibrary.public_ui import render_public_lookup_page
from civiclibrary.reference import CollectionItem, search_collection_metadata

app = FastAPI(
    title="CivicLibrary",
    version=__version__,
    description="Library policy, program, reference, and collection support foundation.",
)

_workpaper_repository: LibraryWorkpaperRepository | None = None
_workpaper_db_url: str | None = None

@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Return an empty favicon response so browser QA has a clean console."""

    return Response(status_code=204)

POLICY_SOURCES = [
    LibraryPolicySource(
        "policy-1",
        "Library service policy",
        "Program information must be accessible and patron records remain private.",
        "Library Policy 1",
    )
]

SAMPLE_ITEMS = [
    CollectionItem("book-1", "Local History Atlas", "local history", "Catalog record 1"),
    CollectionItem("patron-1", "Borrowing history", "restricted", "Patron record", True),
]


class PolicyQuestionRequest(BaseModel):
    question: str


class ProgramQuestionRequest(BaseModel):
    question: str
    programs: list[LibraryProgram]


class ReferenceSearchRequest(BaseModel):
    query: str


class CollectionGuidanceRequest(BaseModel):
    topic: str
    considerations: list[str]


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CivicLibrary",
        "version": __version__,
        "status": "library policy and reference foundation",
        "message": (
            "CivicLibrary policy Q&A, program Q&A, collection-metadata reference support, "
            "collection guidance, optional database-backed program/collection workpapers, and "
            "public UI foundation are online; patron record access, "
            "ILS replacement, circulation actions, live LLM calls, and connector runtime are "
            "not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: read-only ILS metadata adapter design",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "civiclibrary",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civiclibrary", response_class=HTMLResponse)
def public_page() -> str:
    return render_public_lookup_page()


@app.post("/api/v1/civiclibrary/policy-answer")
def policy_answer(request: PolicyQuestionRequest) -> dict[str, object]:
    return answer_policy_question(request.question, POLICY_SOURCES).__dict__


@app.post("/api/v1/civiclibrary/program-answer")
def program_answer(request: ProgramQuestionRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        stored = _get_workpaper_repository().create_program_answer(
            question=request.question,
            programs=request.programs,
        )
        return _stored_program_response(stored)
    payload = answer_program_question(request.question, request.programs).__dict__
    payload["answer_id"] = None
    return payload


@app.get("/api/v1/civiclibrary/program-answer/{answer_id}")
def get_program_answer(answer_id: str) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(status_code=503, detail={"message":"CivicLibrary workpaper persistence is not configured.","fix":"Set CIVICLIBRARY_WORKPAPER_DB_URL to retrieve persisted program answers."})
    stored = _get_workpaper_repository().get_program_answer(answer_id)
    if stored is None:
        raise HTTPException(status_code=404, detail={"message":"Program answer record not found.","fix":"Use an answer_id returned by POST /api/v1/civiclibrary/program-answer."})
    return _stored_program_response(stored)


@app.post("/api/v1/civiclibrary/reference-search")
def reference_search(request: ReferenceSearchRequest) -> dict[str, object]:
    return search_collection_metadata(request.query, SAMPLE_ITEMS).__dict__


@app.post("/api/v1/civiclibrary/collection-guidance")
def collection_guidance(request: CollectionGuidanceRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        stored = _get_workpaper_repository().create_collection_guidance(
            topic=request.topic,
            considerations=request.considerations,
        )
        return _stored_guidance_response(stored)
    payload = draft_collection_guidance(request.topic, request.considerations).__dict__
    payload["guidance_id"] = None
    return payload


@app.get("/api/v1/civiclibrary/collection-guidance/{guidance_id}")
def get_collection_guidance(guidance_id: str) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(status_code=503, detail={"message":"CivicLibrary workpaper persistence is not configured.","fix":"Set CIVICLIBRARY_WORKPAPER_DB_URL to retrieve persisted collection guidance."})
    stored = _get_workpaper_repository().get_collection_guidance(guidance_id)
    if stored is None:
        raise HTTPException(status_code=404, detail={"message":"Collection guidance record not found.","fix":"Use a guidance_id returned by POST /api/v1/civiclibrary/collection-guidance."})
    return _stored_guidance_response(stored)


def _workpaper_database_url() -> str | None:
    return os.environ.get("CIVICLIBRARY_WORKPAPER_DB_URL")


def _get_workpaper_repository() -> LibraryWorkpaperRepository:
    global _workpaper_db_url, _workpaper_repository
    db_url = _workpaper_database_url()
    if db_url is None:
        raise RuntimeError("CIVICLIBRARY_WORKPAPER_DB_URL is not configured.")
    if _workpaper_repository is None or db_url != _workpaper_db_url:
        _dispose_workpaper_repository()
        _workpaper_db_url = db_url
        _workpaper_repository = LibraryWorkpaperRepository(db_url=db_url)
    return _workpaper_repository


def _dispose_workpaper_repository() -> None:
    global _workpaper_repository
    if _workpaper_repository is not None:
        _workpaper_repository.engine.dispose()
        _workpaper_repository = None


def _stored_program_response(stored: StoredProgramAnswer) -> dict[str, object]:
    return {
        "answer_id": stored.answer_id,
        "answer": stored.answer,
        "programs": list(stored.programs),
        "accessibility_review_required": stored.accessibility_review_required,
        "created_at": stored.created_at.isoformat(),
    }


def _stored_guidance_response(stored: StoredCollectionGuidance) -> dict[str, object]:
    return {
        "guidance_id": stored.guidance_id,
        "topic": stored.topic,
        "considerations": list(stored.considerations),
        "librarian_review_required": stored.librarian_review_required,
        "intellectual_freedom_note": stored.intellectual_freedom_note,
        "created_at": stored.created_at.isoformat(),
    }
