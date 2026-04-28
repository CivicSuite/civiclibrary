"""FastAPI runtime foundation for CivicLibrary."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civiclibrary import __version__
from civiclibrary.collection import draft_collection_guidance
from civiclibrary.policy import LibraryPolicySource, answer_policy_question
from civiclibrary.programs import LibraryProgram, answer_program_question
from civiclibrary.public_ui import render_public_lookup_page
from civiclibrary.reference import CollectionItem, search_collection_metadata

app = FastAPI(
    title="CivicLibrary",
    version=__version__,
    description="Library policy, program, reference, and collection support foundation.",
)

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
            "collection guidance, and public UI foundation are online; patron record access, "
            "ILS replacement, circulation actions, live LLM calls, and connector runtime are "
            "not implemented yet."
        ),
        "next_step": "Post-v0.1.0 roadmap: read-only ILS metadata adapter design",
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
    return answer_program_question(request.question, request.programs).__dict__


@app.post("/api/v1/civiclibrary/reference-search")
def reference_search(request: ReferenceSearchRequest) -> dict[str, object]:
    return search_collection_metadata(request.query, SAMPLE_ITEMS).__dict__


@app.post("/api/v1/civiclibrary/collection-guidance")
def collection_guidance(request: CollectionGuidanceRequest) -> dict[str, object]:
    return draft_collection_guidance(request.topic, request.considerations).__dict__
