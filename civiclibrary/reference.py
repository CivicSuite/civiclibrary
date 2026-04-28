"""Reference-assistance helpers over collection metadata, not patron records."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CollectionItem:
    item_id: str
    title: str
    subject: str
    citation: str
    patron_record: bool = False


@dataclass(frozen=True)
class ReferenceResult:
    query: str
    items: tuple[CollectionItem, ...]
    patron_records_excluded: bool
    boundary: str


def search_collection_metadata(query: str, items: list[CollectionItem]) -> ReferenceResult:
    visible = tuple(item for item in items if not item.patron_record)
    return ReferenceResult(
        query=query,
        items=visible,
        patron_records_excluded=len(visible) != len(items),
        boundary=(
            "CivicLibrary searches collection metadata only. Patron borrowing, holds, fines, "
            "and account records are excluded."
        ),
    )
