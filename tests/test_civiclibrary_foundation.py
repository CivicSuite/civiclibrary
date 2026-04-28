from civiclibrary import __version__
from civiclibrary.collection import draft_collection_guidance
from civiclibrary.policy import LibraryPolicySource, answer_policy_question
from civiclibrary.programs import LibraryProgram, answer_program_question
from civiclibrary.reference import CollectionItem, search_collection_metadata


def test_version_is_release_version():
    assert __version__ == "0.1.0"


def test_policy_answer_is_cited_and_reviewed():
    answer = answer_policy_question(
        "What is the meeting-room policy?",
        [LibraryPolicySource("p1", "Meeting Room Policy", "Rooms close at 8.", "Policy 4")],
    )
    assert answer.citations == ("Policy 4",)
    assert answer.librarian_review_required is True
    assert "does not access patron records" in answer.boundary


def test_program_answer_keeps_accessibility_review():
    response = answer_program_question(
        "What events are for teens?",
        [LibraryProgram("Teen craft night", "teens", "2026-05-10", "Accessible room")],
    )
    assert response.accessibility_review_required is True
    assert response.programs[0].title == "Teen craft night"


def test_reference_search_excludes_patron_records():
    result = search_collection_metadata(
        "history",
        [
            CollectionItem("book", "Town History", "history", "Catalog 1"),
            CollectionItem("patron", "Checked out by resident", "restricted", "Patron", True),
        ],
    )
    assert len(result.items) == 1
    assert result.patron_records_excluded is True
    assert "Patron borrowing" in result.boundary


def test_collection_guidance_requires_librarian_review():
    guidance = draft_collection_guidance("local history", ["community demand"])
    assert guidance.librarian_review_required is True
    assert "intellectual freedom" in guidance.intellectual_freedom_note
