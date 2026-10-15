# Project rules: Reliability Data Analysis Agent

## Goal
Build a locally runnable, open-source Reliability Data Analysis Agent Platform for engineering test data.

## Stack
- Python 3.13 (the developer's installed version); keep dependencies compatible with Python 3.13.
- FastAPI + Pydantic for the API and structured schemas.
- PostgreSQL + SQLAlchemy 2 + Alembic for persistence.
- Deterministic analytics with pandas, NumPy, SciPy, lifelines, and statsmodels as needed.
- Ollama for the application's local LLM; coding requests are routed separately through Cline + OmniRoute.
- pytest for tests, Docker Compose for local services, GitHub Actions for CI.
- Add Redis, LangGraph, pgvector, observability dashboards, and RAG only when the current milestone needs them.

## Working method
1. Inspect the current repository before editing.
2. Work in small milestones; do not generate the entire application in one pass.
3. Before substantial changes, summarize the plan, files to change, risks, and tests.
4. Keep API, database, analytics, agent, security, and audit logic separated.
5. Use type hints, Pydantic validation, explicit errors, and clear documentation.
6. Run tests after changes and report only checks actually run.
7. Do not weaken tests, suppress failures, or claim unverified functionality.
8. Prefer free/open-source, self-hostable runtime dependencies; do not require a paid API for the finished application.
9. Document dependency, model, and dataset licenses separately.
10. Never commit credentials, `.env`, private data, or unnecessary generated artifacts.

## Definition of done
- Relevant tests pass.
- Edge cases and failure paths are handled.
- Documentation and examples are updated.
- Security boundaries are tested.
- The summary lists changed files, commands run, test outcomes, and known limitations.
