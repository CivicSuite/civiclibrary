# CivicLibrary Architecture

CivicLibrary v0.1.0 is a deterministic FastAPI module over CivicCore. It supports library policy answers, program and event questions, collection-metadata reference assistance, and collection-development guidance while explicitly avoiding patron records, ILS integration, live connectors, legal advice, and professional-reference replacement.

![CivicLibrary architecture](architecture-civiclibrary.svg)

## Shipped

- Library policy answer drafts with citations and staff-review language.
- Program and event answer drafts with accessibility review prompts.
- Collection-metadata reference search that excludes patron records.
- Collection-development guidance with intellectual-freedom and accessibility reminders.
- Public sample UI and release gates.

## Not Shipped

- Patron record access, ingestion, exposure, holds, fines, or borrowing history.
- ILS integration.
- Replacement for professional librarian reference service.
- Legal advice.
- Live library connectors.
- Live LLM calls.
