# TierTrace-573
Evidence-backed supplier/timeline claims from NHTSA Part 573 filings; local 4B agent with deterministic verifier.
Status: Week 1 scaffold. Parsers are untested on real PDFs; `tt fetch` is blocked on the URL-enumeration gate.
Setup: `python3 -m venv .venv && . .venv/bin/activate && pip install -e ".[dev]" && pytest`
