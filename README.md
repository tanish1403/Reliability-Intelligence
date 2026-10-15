# Reliability Intelligence — Reliability Data Analysis Agent

**A locally runnable open-source reliability analytics portfolio project.** This MVP combines FastAPI, persistent datasets, deterministic statistics, structured API responses, a browser dashboard, audit events, Docker configuration, and CI. It is an educational portfolio project, not certified safety-critical software.

## Implemented features
- CSV ingestion with validation and row/upload limits.
- Synthetic demo dataset, clearly labeled as synthetic.
- Descriptive statistics and IQR outlier screening.
- Two-parameter Weibull MLE for positive, uncensored failures.
- Kaplan–Meier survival estimates that support right-censored observations.
- Typed JSON responses, methods, caveats, and basic audit events.
- Browser dashboard and interactive FastAPI docs.
- SQLite by default; PostgreSQL via Docker Compose.
- Optional Ollama connectivity status; core analytics work without an LLM.
- Pytest and GitHub Actions CI.

## Architecture
```mermaid
flowchart TD
 U[Engineer / Browser] --> API[FastAPI]
 API --> S[Validation and services]
 S --> DB[(SQLite or PostgreSQL)]
 S --> A[Deterministic analytics]
 A --> J[Typed JSON + caveats]
 S --> L[Audit events]
 API -. optional .-> O[Local Ollama status]
 CI[GitHub Actions] --> T[Pytest]
```
The model is not the source of statistical truth: Python computes the results. This MVP has an Ollama connectivity check, not yet full LLM tool orchestration.

## Quick start — Windows, Python 3.13.12
Open this folder in VS Code, then run in PowerShell:
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -m reliability_agent.seed
uvicorn reliability_agent.main:app --reload
```
Open `http://127.0.0.1:8000/` for the dashboard, `/docs` for API docs, and `/health` for the health check. In a second terminal, run `python -m pytest -q`.

If activation is blocked, call `\.venv\Scripts\python.exe -m pip install -e ".[dev]"` and `\.venv\Scripts\python.exe -m reliability_agent.seed` directly.

## API endpoints
- `GET /health`
- `GET /api/v1/datasets`
- `POST /api/v1/datasets/upload` — multipart CSV; required `duration_hours`; optional `event_observed`, `device_type`.
- `GET /api/v1/datasets/{id}/summary`
- `GET /api/v1/datasets/{id}/outliers`
- `GET /api/v1/datasets/{id}/weibull`
- `GET /api/v1/datasets/{id}/survival`
- `GET /api/v1/audit`
- `GET /api/v1/llm/status`

Example CSV:
```csv
duration_hours,event_observed,device_type
120,true,sensor-A
155,true,sensor-A
200,false,sensor-A
240,true,sensor-B
```
Upload through Swagger UI at `/docs` or the dashboard.

## Statistical assumptions
- **Summary:** sample standard deviation uses `ddof=1`.
- **Outliers:** 1.5×IQR fences flag values for review; they do not prove data is erroneous.
- **Weibull:** SciPy two-parameter MLE with location fixed to zero; at least three positive, uncensored observations. Censored Weibull fitting and confidence intervals are not implemented.
- **Kaplan–Meier:** product-limit estimate supporting right-censored observations. Median survival is null if the curve does not reach 0.5.
- Demo data is synthetic and must not be represented as real device qualification data.

## PostgreSQL (optional)
Default DB is SQLite at `./data/reliability.db`. To use PostgreSQL, set in `.env`:
```env
DATABASE_URL=postgresql+psycopg://reliability:local-dev-change-me@localhost:5432/reliability
```
Then run `python -m pip install -e ".[postgres,dev]"` and `docker compose up -d db`. The MVP creates tables at startup; add Alembic migrations before shared/production use.

## Optional local Ollama
Install Ollama separately and pull a compatible model, e.g. `ollama pull qwen2.5:3b`. Set `OLLAMA_BASE_URL` and `OLLAMA_MODEL` in `.env`. Then inspect `GET /api/v1/llm/status`. This is separate from the coding model routed through Cline + OmniRoute.

## Cline + OmniRoute
Open the extracted project root (the folder containing `pyproject.toml`) in VS Code. Workspace instructions are in `.clinerules/`. Use Cline Plan mode for substantial changes, approve one milestone at a time, inspect `git diff`, run tests, and commit known-good checkpoints. The rules explicitly require README updates whenever features, setup, dependencies, endpoints, or limitations change.

Suggested prompt:
> Read README.md and all files in .clinerules/. Run the current tests, inspect the implementation, then propose the three highest-priority improvements. For every change, update tests and README in the same task. Do not replace working code wholesale. Wait for my approval before editing.

## GitHub checklist
- [ ] `python -m pytest -q` passes.
- [ ] Run the app from a clean environment and verify `/`, `/docs`, `/health`.
- [ ] Seed the demo dataset and try all four analyses.
- [ ] Ensure `.env`, local databases, private datasets, and uploads are not committed.
- [ ] Add your own screenshot/GIF under `docs/screenshots/`.
- [ ] Review dependency, model, and dataset licenses before redistributing third-party assets.

## Roadmap
1. Alembic migrations and database lifecycle improvements.
2. Authentication, server-enforced RBAC, human approvals, protected audit trail.
3. Censored Weibull likelihood and confidence intervals.
4. Constrained Ollama tool-calling agent / LangGraph workflow.
5. OpenTelemetry, metrics, and agent evaluation.
6. Optional technical-document RAG with citations.

## License
Apache-2.0. See `LICENSE`. Third-party packages, models, and datasets retain their own licenses.
