# Lightweight Finance API

A simple and lightweight REST API for tracking personal income, expenses, and budget — built with **FastAPI** and **Python**, containerised with **Docker**.

**IBM SkillsBuild Student Project · Yenepoya University · 2023–2026 Batch · Sayu V**

---

## Features

- Add income records with source label
- Add expense records with category label
- View financial summary (total income, total expenses, balance)
- Set a monthly budget limit
- Check budget status (spent vs remaining)
- Health check endpoint
- Input validation via Pydantic — rejects invalid data with clear error messages
- Auto-generated interactive API documentation (Swagger UI)
- Containerised with Docker for portable deployment

---

## Tech Stack

| Component        | Technology              |
|------------------|-------------------------|
| Language         | Python 3.10+            |
| API Framework    | FastAPI                 |
| Validation       | Pydantic v2             |
| Server           | Uvicorn (ASGI)          |
| Containerisation | Docker                  |
| Testing          | pytest + httpx          |
| API Docs         | Swagger UI / ReDoc      |

---

## Project Structure

```
Lightweight-Finance-API/
├── main.py               # FastAPI app — routes, handlers, storage
├── models.py             # Pydantic request and response models
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container build instructions
├── .dockerignore         # Files excluded from Docker build
├── .gitignore            # Files excluded from Git
├── README.md             # This file
├── tests/
│   ├── __init__.py
│   └── test_main.py      # Automated pytest test suite (20 tests)
└── docs/
    ├── DOC01_Project_Proposal.docx
    ├── DOC02_PRD.docx
    ├── DOC03_HLD.docx
    ├── DOC04_LLD.docx
    ├── DOC05_API_Reference.md
    ├── DOC06_Deployment_Guide.md
    ├── DOC07_Test_Report.md
    ├── DOC08_Final_Report.docx
    └── DOC09_Presentation.pptx
```

---

## API Endpoints

| Method | Endpoint         | Description                             |
|--------|------------------|-----------------------------------------|
| GET    | `/health`        | Health check — confirms API is running  |
| POST   | `/income`        | Add an income record                    |
| POST   | `/expense`       | Add an expense record                   |
| GET    | `/summary`       | Get total income, expenses, and balance |
| POST   | `/budget`        | Set monthly budget limit                |
| GET    | `/budget-status` | Get budget, amount spent, and remaining |

---

## How to Run

### Option A — Local Python (recommended for testing)

```bash
# 1. Install dependencies (use Python 3.11)
py -3.11 -m pip install fastapi uvicorn httpx pytest

# 2. Start the server
py -3.11 -m uvicorn main:app --reload

# 3. Open API docs
# http://localhost:8000/docs
```

### Option B — Docker (recommended for deployment)

```bash
# 1. Build the image
docker build -t finance-api .

# 2. Run the container
docker run -p 8000:8000 finance-api

# 3. Open API docs
# http://localhost:8000/docs
```

### Option C — Docker Compose

```bash
docker compose up --build
```

---

## API Documentation

FastAPI automatically generates interactive documentation:

| Interface    | URL                                     |
|--------------|-----------------------------------------|
| Swagger UI   | http://localhost:8000/docs              |
| ReDoc        | http://localhost:8000/redoc             |

---

## Example Requests

**Health check:**
```bash
curl http://localhost:8000/health
```

**Add income:**
```bash
curl -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000, "source": "Salary"}'
```

**Add expense:**
```bash
curl -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 150.75, "category": "Groceries"}'
```

**Get summary:**
```bash
curl http://localhost:8000/summary
```

---

## Running Tests

```bash
# Run all 20 tests (use Python 3.11)
py -3.11 -m pytest tests/test_main.py -v
```

Expected output: **20 passed**

> **Note:** Python 3.15+ does not yet have pre-built packages for pydantic-core.
> Use Python 3.11 for running the tests locally.

---

## Design Notes

- **In-memory storage:** All data is stored in Python lists and resets when the server restarts. This is intentional for v1 — the architecture is designed so PostgreSQL can be added in v2 with minimal changes to the API layer.
- **Stateless design:** No server-side sessions. Every request is self-contained, making the API ready for horizontal scaling and cloud deployment.
- **Validation:** Pydantic v2 models reject invalid inputs before they reach business logic — amounts must be > 0, strings cannot be empty or exceed 50 characters. Invalid amounts return HTTP 422.

---

## Known Limitations (v1)

- Data is not persistent — resets on server restart
- Single user only — no authentication
- No frontend UI
- No per-category budget tracking

These are planned for v2 (PostgreSQL + JWT auth + React dashboard).

---

## Documentation

Full project documentation is in the `docs/` folder:

| Document | Description |
|----------|-------------|
| DOC01 — Project Proposal | Problem, objectives, methodology, timeline |
| DOC02 — PRD | 30 functional requirements, data models, acceptance criteria |
| DOC03 — HLD | System architecture, data flow, cloud readiness |
| DOC04 — LLD | Endpoint contracts, pseudocode, source code, traceability |
| DOC05 — API Reference | Complete endpoint reference with curl examples |
| DOC06 — Deployment Guide | Local + Docker setup, troubleshooting |
| DOC07 — Test Report | 39 test cases, 100% pass rate |
| DOC08 — Final Report | Academic report covering full project lifecycle |
| DOC09 — Presentation | 12-slide deck for project presentation |

---

## License

For academic use — IBM SkillsBuild Student Project Programme.
