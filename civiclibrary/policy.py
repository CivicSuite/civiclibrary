"""Library policy and program Q&A helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LibraryPolicySource:
    source_id: str
    title: str
    text: str
    citation: str


@dataclass(frozen=True)
class LibraryPolicyAnswer:
    answer: str
    citations: tuple[str, ...]
    librarian_review_required: bool
    boundary: str


def answer_policy_question(
    question: str, sources: list[LibraryPolicySource]
) -> LibraryPolicyAnswer:
    citations = tuple(source.citation for source in sources if source.text)
    return LibraryPolicyAnswer(
        answer=(
            f"Draft library policy or program answer for: {question}. "
            "Verify against the cited policy before sharing."
        ),
        citations=citations,
        librarian_review_required=True,
        boundary=(
            "CivicLibrary supports library policy and program information. It does not access "
            "patron records, replace professional reference service, or act as an ILS."
        ),
    )
