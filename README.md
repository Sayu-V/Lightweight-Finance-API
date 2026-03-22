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
- Input validation via Pydantic — rejects invalid data with clear error messages
- Auto-generated interactive API documentation (Swagger UI)
- Containerised with Docker for portable deployment

---

## Tech Stack

| Component      | Technology              |
|----------------|------------------------|
| Language       | Python 3.10+            |
| API Framework  | FastAPI                 |
| Validation     | Pydantic v1             |
| Server         | Uvicorn (ASGI)          |
| Containerisation | Docker               |
| Testing        | pytest + httpx          |
| API Docs       | Swagger UI / ReDoc      |

---

## Project Structure

```
Lightweight-Finance-API/
├── main.py               # FastAPI app — routes, handlers, storage
├── models.py             # Pydantic request and response models
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container build instructions
├── README.md             # This file
├── tests/
│   └── test_main.py      # Automated pytest test suite (19 tests)
└── docs/
    ├── PROPOSAL.md       # Project Proposal
    ├── HLD.md            # High-Level Design
    ├── LLD.md            # Low-Level Design
    └── FINAL_REPORT.md   # Final Report
```

---

## API Endpoints

| Method | Endpoint         | Description                        |
|--------|------------------|------------------------------------|
| GET    | `/health`        | Health check — confirms API is running |
| POST   | `/income`        | Add an income record               |
| POST   | `/expense`       | Add an expense record              |
| GET    | `/summary`       | Get total income, expenses, balance |
| POST   | `/budget`        | Set monthly budget limit           |
| GET    | `/budget-status` | Get budget, amount spent, remaining |

---

## How to Run

### Option A — Local Python

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --reload

# 3. Open API docs
# http://localhost:8000/docs
```

### Option B — Docker

```bash
# 1. Build the image
docker build -t finance-api .

# 2. Run the container
docker run -p 8000:8000 finance-api

# 3. Open API docs
# http://localhost:8000/docs
```

---

## API Documentation

FastAPI automatically generates interactive documentation:

| Interface   | URL                                  |
|-------------|--------------------------------------|
| Swagger UI  | http://localhost:8000/docs           |
| ReDoc       | http://localhost:8000/redoc          |

---

## Example Requests

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
# Install test dependencies
pip install pytest httpx

# Run all tests
pytest tests/test_main.py -v
```

Expected output: **19 tests passing**

---

## Design Notes

- **In-memory storage:** All data is stored in Python lists and reset when the server restarts. This is intentional for v1 — the architecture is designed for PostgreSQL to be added in v2 with minimal changes.
- **Stateless design:** No server-side sessions. Every request is self-contained, making the API ready for horizontal scaling and cloud deployment.
- **Validation:** Pydantic models reject invalid inputs before they reach business logic — amounts must be > 0, strings cannot be empty or exceed 50 characters.

---

## Known Limitations (v1)

- Data is not persistent — resets on server restart
- Single user only — no authentication
- No frontend UI
- No per-category budget tracking

These are planned for v2 (PostgreSQL + JWT auth + React dashboard).

---

## License

For academic use — IBM SkillsBuild Student Project Programme.
