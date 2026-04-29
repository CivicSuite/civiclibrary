from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civiclibrary.collection import draft_collection_guidance
from civiclibrary.programs import LibraryProgram, answer_program_question


metadata = sa.MetaData()

program_answer_records = sa.Table(
    "program_answer_records",
    metadata,
    sa.Column("answer_id", sa.String(36), primary_key=True),
    sa.Column("answer", sa.Text(), nullable=False),
    sa.Column("programs", sa.JSON(), nullable=False),
    sa.Column("accessibility_review_required", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiclibrary",
)

collection_guidance_records = sa.Table(
    "collection_guidance_records",
    metadata,
    sa.Column("guidance_id", sa.String(36), primary_key=True),
    sa.Column("topic", sa.String(255), nullable=False),
    sa.Column("considerations", sa.JSON(), nullable=False),
    sa.Column("librarian_review_required", sa.Boolean(), nullable=False),
    sa.Column("intellectual_freedom_note", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiclibrary",
)


@dataclass(frozen=True)
class StoredProgramAnswer:
    answer_id: str
    answer: str
    programs: tuple[dict[str, str], ...]
    accessibility_review_required: bool
    created_at: datetime


@dataclass(frozen=True)
class StoredCollectionGuidance:
    guidance_id: str
    topic: str
    considerations: tuple[str, ...]
    librarian_review_required: bool
    intellectual_freedom_note: str
    created_at: datetime


class LibraryWorkpaperRepository:
    """SQLAlchemy-backed program answer and collection guidance workpapers."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civiclibrary": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civiclibrary"))
        metadata.create_all(self.engine)

    def create_program_answer(
        self, *, question: str, programs: list[LibraryProgram]
    ) -> StoredProgramAnswer:
        answer = answer_program_question(question, programs)
        stored = StoredProgramAnswer(
            answer_id=str(uuid4()),
            answer=answer.answer,
            programs=tuple(program.__dict__ for program in answer.programs),
            accessibility_review_required=answer.accessibility_review_required,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                program_answer_records.insert().values(
                    answer_id=stored.answer_id,
                    answer=stored.answer,
                    programs=list(stored.programs),
                    accessibility_review_required=stored.accessibility_review_required,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_program_answer(self, answer_id: str) -> StoredProgramAnswer | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(program_answer_records).where(
                    program_answer_records.c.answer_id == answer_id
                )
            ).mappings().first()
        if row is None:
            return None
        data = dict(row)
        return StoredProgramAnswer(
            answer_id=data["answer_id"],
            answer=data["answer"],
            programs=tuple(data["programs"]),
            accessibility_review_required=data["accessibility_review_required"],
            created_at=data["created_at"],
        )

    def create_collection_guidance(
        self, *, topic: str, considerations: list[str]
    ) -> StoredCollectionGuidance:
        guidance = draft_collection_guidance(topic, considerations)
        stored = StoredCollectionGuidance(
            guidance_id=str(uuid4()),
            topic=guidance.topic,
            considerations=guidance.considerations,
            librarian_review_required=guidance.librarian_review_required,
            intellectual_freedom_note=guidance.intellectual_freedom_note,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                collection_guidance_records.insert().values(
                    guidance_id=stored.guidance_id,
                    topic=stored.topic,
                    considerations=list(stored.considerations),
                    librarian_review_required=stored.librarian_review_required,
                    intellectual_freedom_note=stored.intellectual_freedom_note,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_collection_guidance(self, guidance_id: str) -> StoredCollectionGuidance | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(collection_guidance_records).where(
                    collection_guidance_records.c.guidance_id == guidance_id
                )
            ).mappings().first()
        if row is None:
            return None
        data = dict(row)
        return StoredCollectionGuidance(
            guidance_id=data["guidance_id"],
            topic=data["topic"],
            considerations=tuple(data["considerations"]),
            librarian_review_required=data["librarian_review_required"],
            intellectual_freedom_note=data["intellectual_freedom_note"],
            created_at=data["created_at"],
        )
