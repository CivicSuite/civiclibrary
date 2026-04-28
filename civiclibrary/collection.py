"""Collection development guidance helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CollectionGuidance:
    topic: str
    considerations: tuple[str, ...]
    librarian_review_required: bool
    intellectual_freedom_note: str


def draft_collection_guidance(topic: str, considerations: list[str]) -> CollectionGuidance:
    return CollectionGuidance(
        topic=topic,
        considerations=tuple(considerations),
        librarian_review_required=True,
        intellectual_freedom_note=(
            "Draft only: review against the library's intellectual freedom, reconsideration, "
            "and collection development policies."
        ),
    )
