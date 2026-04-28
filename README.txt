CivicLibrary

CivicLibrary v0.1.1 ships municipal library support foundations: cited library policy Q&A, program and event Q&A, reference assistance over collection metadata, collection development guidance, FastAPI runtime, public sample UI, docs, tests, browser QA, and release gates.

It is not an integrated library system, patron-record access path, circulation workflow, holds or fines system, replacement for professional reference service, live LLM runtime, or library connector.

Install:
python -m pip install -e ".[dev]"
python -m uvicorn civiclibrary.main:app --host 127.0.0.1 --port 8143

CivicLibrary v0.1.1 is pinned to civiccore==0.3.0.

Apache 2.0 code. CC BY 4.0 docs.
