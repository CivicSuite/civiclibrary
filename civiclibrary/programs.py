"""Library program and event Q&A helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LibraryProgram:
    title: str
    audience: str
    date: str
    accessibility_note: str


@dataclass(frozen=True)
class ProgramAnswer:
    answer: str
    programs: tuple[LibraryProgram, ...]
    accessibility_review_required: bool


def answer_program_question(question: str, programs: list[LibraryProgram]) -> ProgramAnswer:
    return ProgramAnswer(
        answer=f"Draft program and event answer for: {question}",
        programs=tuple(programs),
        accessibility_review_required=True,
    )
