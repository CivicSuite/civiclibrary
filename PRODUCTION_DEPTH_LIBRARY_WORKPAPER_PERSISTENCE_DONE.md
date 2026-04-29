# Production Depth: Library Workpaper Persistence

## Summary

CivicLibrary now supports optional SQLAlchemy-backed program answer and collection-guidance records through `CIVICLIBRARY_WORKPAPER_DB_URL`.

## Shipped

- `LibraryWorkpaperRepository` with schema-aware SQLAlchemy tables.
- Persisted program answer records with `answer_id`.
- Persisted collection-guidance records with `guidance_id`.
- Retrieval endpoints:
  - `GET /api/v1/civiclibrary/program-answer/{answer_id}`
  - `GET /api/v1/civiclibrary/collection-guidance/{guidance_id}`
- Actionable `503` guidance when persistence is not configured.
- Regression tests for repository reload, API round trip, missing-record `404`, no-config `503`, and stateless fallback behavior.

## Still Not Shipped

- Patron-record access.
- Integrated library system replacement.
- Circulation actions, holds, or fines.
- Live LLM calls.
- Library connector runtime.
