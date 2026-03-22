# Lightweight Finance API — API Reference

**Document ID:** DOC-05  
**Version:** 1.0  
**Project:** Lightweight Finance API  
**Author:** Sayu V | Yenepoya University  
**Programme:** IBM SkillsBuild Student Project | 2023–2026 Batch  
**Date:** $(date '+%d %B %Y')  
**Format:** Markdown (.md) — renders on GitHub and any Markdown viewer

---

## Table of Contents

1. [Overview](#1-overview)
2. [Base URL & Connection](#2-base-url--connection)
3. [Request & Response Format](#3-request--response-format)
4. [Authentication](#4-authentication)
5. [Endpoints](#5-endpoints)
   - [GET /health](#50-get-health)
   - [POST /income](#51-post-income)
   - [POST /expense](#52-post-expense)
   - [GET /summary](#53-get-summary)
   - [POST /budget](#54-post-budget)
   - [GET /budget-status](#55-get-budget-status)
6. [Error Reference](#6-error-reference)
7. [Data Models](#7-data-models)
8. [Quick Test Sequence](#8-quick-test-sequence)
9. [Interactive Documentation](#9-interactive-documentation)
10. [Changelog](#10-changelog)

---

## 1. Overview

The **Lightweight Finance API** is a RESTful backend service for tracking personal income and expenses, setting a monthly budget, and monitoring financial balance. It is built with **FastAPI** (Python) and returns **JSON** for all operations.

| Property         | Value                                      |
|------------------|--------------------------------------------|
| API Style        | REST                                       |
| Data Format      | JSON (application/json)                    |
| Authentication   | None (v1 — single user)                   |
| Total Endpoints  | 6                                          |
| Server           | Uvicorn (ASGI)                             |
| Framework        | FastAPI (latest stable)                    |
| Python Version   | 3.10+                                      |
| Container        | Docker (python:3.10 base image)            |
| Auto-Docs        | Swagger UI at `/docs`, ReDoc at `/redoc`   |

---

## 2. Base URL & Connection

### Running Locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

**Base URL:** `http://localhost:8000`

### Running with Docker

```bash
docker build -t finance-api .
docker run -p 8000:8000 finance-api
```

**Base URL:** `http://localhost:8000`

> **Note:** All data is stored in memory. Restarting the server clears all income, expense, and budget data.

---

## 3. Request & Response Format

### Requests

- All `POST` endpoints accept a JSON body
- Set the `Content-Type` header to `application/json`
- `GET` endpoints require no request body

### Responses

- All responses are JSON (`application/json`)
- All successful responses return **HTTP 200**
- Error responses follow the format described in [Section 6](#6-error-reference)

### Numeric Types

All `amount`, `limit`, and computed financial values are **64-bit floating point numbers** (`float`).

```
✅ Valid:   150.75   |   5000   |   0.01   |   99999.99
❌ Invalid: 0   |   -50   |   "150"   |   null
```

---

## 4. Authentication

**v1: No authentication required.**

All endpoints are publicly accessible. There is no login, no API key, and no session management in this version. Authentication (JWT Bearer tokens) is planned for v2.

---

## 5. Endpoints

---

### 5.0 GET /health

Check that the API is running. Useful for confirming the server started correctly before testing other endpoints, and for Docker health monitoring.

```
GET http://localhost:8000/health
```

#### Request Headers

None required.

#### Request Body

None — this is a `GET` endpoint.

#### Example Request

```bash
curl http://localhost:8000/health
```

#### Success Response — HTTP 200

```json
{
  "status": "API is running"
}
```

#### Notes

- This endpoint always returns HTTP 200 when the server is up.
- No error states — if the server is down, the request simply fails to connect.
- Use this as your first test after starting the server to confirm everything is working before calling other endpoints.

---

### 5.1 POST /income

Add a new income record to the in-memory income list.

```
POST http://localhost:8000/income
```

#### Request Headers

| Header         | Value              | Required |
|----------------|--------------------|----------|
| Content-Type   | application/json   | Yes      |

#### Request Body

| Field    | Type    | Required | Constraints              | Description                          |
|----------|---------|----------|--------------------------|--------------------------------------|
| `amount` | float   | Yes      | Must be > 0              | Income amount (e.g. salary, payment) |
| `source` | string  | Yes      | Length: 1–50 characters  | Source label (e.g. "Salary", "Freelance") |

#### Example Request

```bash
curl -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000.00,
    "source": "Monthly Salary"
  }'
```

```json
{
  "amount": 5000.00,
  "source": "Monthly Salary"
}
```

#### Success Response — HTTP 200

```json
{
  "message": "Income added successfully"
}
```

#### Error Responses

| HTTP Status | Condition                          | Response Body                                           |
|-------------|------------------------------------|---------------------------------------------------------|
| `400`       | `amount` is 0 or negative          | `{"detail": "Amount must be greater than 0"}`           |
| `422`       | `amount` is missing                | `{"detail": [{"loc": ["body","amount"], "msg": "field required", "type": "value_error.missing"}]}` |
| `422`       | `amount` is not a number           | `{"detail": [{"loc": ["body","amount"], "msg": "value is not a valid float", "type": "type_error.float"}]}` |
| `422`       | `source` is missing                | `{"detail": [{"loc": ["body","source"], "msg": "field required", "type": "value_error.missing"}]}` |
| `422`       | `source` is empty string `""`      | `{"detail": [{"loc": ["body","source"], "msg": "ensure this value has at least 1 characters", "type": "value_error.any_str.min_length"}]}` |
| `422`       | `source` exceeds 50 characters     | `{"detail": [{"loc": ["body","source"], "msg": "ensure this value has at most 50 characters", "type": "value_error.any_str.max_length"}]}` |

#### Notes

- The `source` value is validated but **not stored separately** — only the `amount` (float) is appended to the income list.
- Calling this endpoint multiple times accumulates amounts. There is no duplicate check.
- To retrieve the running total, call `GET /summary`.

---

### 5.2 POST /expense

Add a new expense record to the in-memory expense list.

```
POST http://localhost:8000/expense
```

#### Request Headers

| Header         | Value              | Required |
|----------------|--------------------|----------|
| Content-Type   | application/json   | Yes      |

#### Request Body

| Field      | Type    | Required | Constraints              | Description                                |
|------------|---------|----------|--------------------------|--------------------------------------------|
| `amount`   | float   | Yes      | Must be > 0              | Expense amount                             |
| `category` | string  | Yes      | Length: 1–50 characters  | Category label (e.g. "Groceries", "Rent")  |

#### Example Request

```bash
curl -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 150.75,
    "category": "Groceries"
  }'
```

```json
{
  "amount": 150.75,
  "category": "Groceries"
}
```

#### Success Response — HTTP 200

```json
{
  "message": "Expense added successfully"
}
```

#### Error Responses

| HTTP Status | Condition                          | Response Body                                           |
|-------------|------------------------------------|---------------------------------------------------------|
| `400`       | `amount` is 0 or negative          | `{"detail": "Amount must be greater than 0"}`           |
| `422`       | `amount` is missing                | `{"detail": [{"loc": ["body","amount"], "msg": "field required", "type": "value_error.missing"}]}` |
| `422`       | `amount` is not a number           | `{"detail": [{"loc": ["body","amount"], "msg": "value is not a valid float", "type": "type_error.float"}]}` |
| `422`       | `category` is missing              | `{"detail": [{"loc": ["body","category"], "msg": "field required", "type": "value_error.missing"}]}` |
| `422`       | `category` is empty string `""`    | `{"detail": [{"loc": ["body","category"], "msg": "ensure this value has at least 1 characters", "type": "value_error.any_str.min_length"}]}` |
| `422`       | `category` exceeds 50 characters   | `{"detail": [{"loc": ["body","category"], "msg": "ensure this value has at most 50 characters", "type": "value_error.any_str.max_length"}]}` |

#### Notes

- Like `/income`, the `category` string is validated but only the `amount` float is stored.
- Expenses are used by both `GET /summary` (total) and `GET /budget-status` (spent vs limit).
- There is no per-category tracking in v1 — all amounts go into a single list.

---

### 5.3 GET /summary

Returns the current financial summary: total income, total expenses, and the resulting balance.

```
GET http://localhost:8000/summary
```

#### Request Headers

None required.

#### Request Body

None — this is a `GET` endpoint.

#### Example Request

```bash
curl http://localhost:8000/summary
```

#### Success Response — HTTP 200

```json
{
  "total_income": 7500.00,
  "total_expense": 230.75,
  "balance": 7269.25
}
```

| Field           | Type  | Description                                              |
|-----------------|-------|----------------------------------------------------------|
| `total_income`  | float | Sum of all amounts added via `POST /income`              |
| `total_expense` | float | Sum of all amounts added via `POST /expense`             |
| `balance`       | float | `total_income` minus `total_expense` (can be negative)   |

#### Empty State Response — HTTP 200

When no income or expenses have been recorded yet:

```json
{
  "total_income": 0,
  "total_expense": 0,
  "balance": 0
}
```

#### Edge Cases

| Scenario                          | Response                                                     |
|-----------------------------------|--------------------------------------------------------------|
| No data added yet                 | All three values are `0`                                     |
| Only expenses, no income          | `total_income: 0`, `balance` is negative                    |
| Only income, no expenses          | `total_expense: 0`, `balance` equals `total_income`         |
| Expenses exceed income            | `balance` is a negative float — this is valid and expected  |

#### Notes

- This endpoint always returns HTTP 200 — there are no error states.
- Calculations use Python's built-in `sum()` on the in-memory lists.
- `balance` can be negative; the API does not enforce a non-negative balance.

---

### 5.4 POST /budget

Set the global monthly budget limit. Calling this endpoint again overwrites the previous value.

```
POST http://localhost:8000/budget
```

#### Request Headers

| Header         | Value              | Required |
|----------------|--------------------|----------|
| Content-Type   | application/json   | Yes      |

#### Request Body

| Field   | Type  | Required | Constraints | Description                          |
|---------|-------|----------|-------------|--------------------------------------|
| `limit` | float | Yes      | Must be > 0 | Monthly spending budget ceiling       |

#### Example Request

```bash
curl -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{
    "limit": 10000.00
  }'
```

```json
{
  "limit": 10000.00
}
```

#### Success Response — HTTP 200

```json
{
  "message": "Budget set successfully"
}
```

#### Error Responses

| HTTP Status | Condition                     | Response Body                                                                     |
|-------------|-------------------------------|-----------------------------------------------------------------------------------|
| `422`       | `limit` is 0                  | `{"detail": [{"loc": ["body","limit"], "msg": "ensure this value is greater than 0", "type": "value_error.number.not_gt"}]}` |
| `422`       | `limit` is negative           | `{"detail": [{"loc": ["body","limit"], "msg": "ensure this value is greater than 0", "type": "value_error.number.not_gt"}]}` |
| `422`       | `limit` is missing            | `{"detail": [{"loc": ["body","limit"], "msg": "field required", "type": "value_error.missing"}]}` |
| `422`       | `limit` is not a number       | `{"detail": [{"loc": ["body","limit"], "msg": "value is not a valid float", "type": "type_error.float"}]}` |

#### Notes

- This endpoint **sets** the budget — it does not add to it. Calling `POST /budget` with `limit: 8000` after a previous call with `limit: 5000` results in a budget of `8000`, not `13000`.
- The budget is a single global value — there is no per-category budget in v1.
- To check budget usage after setting it, call `GET /budget-status`.

---

### 5.5 GET /budget-status

Returns the current budget state: the set limit, total amount spent, and the amount remaining.

```
GET http://localhost:8000/budget-status
```

#### Request Headers

None required.

#### Request Body

None — this is a `GET` endpoint.

#### Example Request

```bash
curl http://localhost:8000/budget-status
```

#### Success Response — HTTP 200

```json
{
  "budget": 10000.00,
  "spent": 550.75,
  "remaining": 9449.25
}
```

| Field       | Type  | Description                                                              |
|-------------|-------|--------------------------------------------------------------------------|
| `budget`    | float | The limit set via `POST /budget` (0 if never set)                        |
| `spent`     | float | Sum of all amounts added via `POST /expense`                             |
| `remaining` | float | `budget` minus `spent` — negative if over budget, positive if under     |

#### Edge Cases

| Scenario                           | Response                                                              |
|------------------------------------|-----------------------------------------------------------------------|
| Budget never set, no expenses      | `{"budget": 0, "spent": 0, "remaining": 0}`                         |
| Budget set, no expenses yet        | `{"budget": X, "spent": 0, "remaining": X}`                         |
| Expenses exactly equal budget      | `{"budget": X, "spent": X, "remaining": 0}`                         |
| Expenses exceed budget             | `{"budget": X, "spent": Y, "remaining": -Z}` — negative remaining   |

#### Notes

- This endpoint always returns HTTP 200 — there are no error states.
- A negative `remaining` value means you are over budget. The API does not block further expenses when over budget.
- `spent` is always the same value as `total_expense` in `GET /summary`.

---

## 6. Error Reference

### HTTP Status Codes

| Status | Category           | Meaning in This API                                                            |
|--------|--------------------|--------------------------------------------------------------------------------|
| `200`  | Success            | Request processed successfully; response body contains result                  |
| `400`  | Client Error       | Business rule violation — `amount` or `limit` is 0 or negative (manual check) |
| `404`  | Not Found          | Requested path does not exist (FastAPI default)                                |
| `405`  | Method Not Allowed | Wrong HTTP method — e.g. `GET` on a `POST`-only endpoint (FastAPI default)     |
| `422`  | Validation Error   | Pydantic schema validation failed — missing field, wrong type, constraint violated |
| `500`  | Server Error       | Unhandled exception — should not occur in normal operation                     |

### Validation Error Format (HTTP 422)

All HTTP 422 responses follow this Pydantic format:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "human-readable error message",
      "type": "error_type_identifier"
    }
  ]
}
```

Multiple validation failures in the same request are returned together:

```json
{
  "detail": [
    {
      "loc": ["body", "amount"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "source"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Business Rule Error Format (HTTP 400)

```json
{
  "detail": "Amount must be greater than 0"
}
```

### Complete Error Code Table

| Error ID | Endpoint         | Status | Trigger Condition                | `msg` in Response                               |
|----------|------------------|--------|----------------------------------|-------------------------------------------------|
| ERR-01   | POST /income     | 400    | `amount` is 0 or negative        | `"Amount must be greater than 0"`               |
| ERR-02   | POST /income     | 422    | `amount` is not a float          | `"value is not a valid float"`                  |
| ERR-03   | POST /income     | 422    | `amount` field missing           | `"field required"`                              |
| ERR-04   | POST /income     | 422    | `source` field missing           | `"field required"`                              |
| ERR-05   | POST /income     | 422    | `source` is `""`                 | `"ensure this value has at least 1 characters"` |
| ERR-06   | POST /income     | 422    | `source` > 50 chars              | `"ensure this value has at most 50 characters"` |
| ERR-07   | POST /expense    | 400    | `amount` is 0 or negative        | `"Amount must be greater than 0"`               |
| ERR-08   | POST /expense    | 422    | `amount` is not a float          | `"value is not a valid float"`                  |
| ERR-09   | POST /expense    | 422    | `amount` field missing           | `"field required"`                              |
| ERR-10   | POST /expense    | 422    | `category` field missing         | `"field required"`                              |
| ERR-11   | POST /expense    | 422    | `category` is `""`               | `"ensure this value has at least 1 characters"` |
| ERR-12   | POST /expense    | 422    | `category` > 50 chars            | `"ensure this value has at most 50 characters"` |
| ERR-13   | POST /budget     | 422    | `limit` is 0 or negative         | `"ensure this value is greater than 0"`         |
| ERR-14   | POST /budget     | 422    | `limit` field missing            | `"field required"`                              |
| ERR-15   | Any endpoint     | 404    | Path does not exist              | FastAPI default 404                             |
| ERR-16   | Any endpoint     | 405    | Wrong HTTP method                | FastAPI default 405                             |

---

## 7. Data Models

### Income (Request Body)

```python
class Income(BaseModel):
    amount: float = Field(..., gt=0)                          # > 0
    source: str   = Field(..., min_length=1, max_length=50)   # 1–50 chars
```

### Expense (Request Body)

```python
class Expense(BaseModel):
    amount:   float = Field(..., gt=0)                        # > 0
    category: str   = Field(..., min_length=1, max_length=50) # 1–50 chars
```

### Budget (Request Body)

```python
class Budget(BaseModel):
    limit: float = Field(..., gt=0)                           # > 0
```

### In-Memory Storage

The API stores all data in three module-level Python variables:

```python
incomes:  list  = []   # List of income amounts (float)
expenses: list  = []   # List of expense amounts (float)
budget:   float = 0    # Single global budget limit
```

> **Important:** All data is lost when the server process stops or restarts. There is no persistent storage in v1.

---

## 8. Quick Test Sequence

Use this sequence to verify all 6 endpoints are working correctly after starting the server:

### Step 1 — Check the API is running

```bash
curl http://localhost:8000/health
```

Expected: `{"status": "API is running"}`

---

### Step 2 — Add income

```bash
curl -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 8000, "source": "Salary"}'
```

Expected: `{"message": "Income added successfully"}`

---

### Step 3 — Add expenses

```bash
curl -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 200, "category": "Groceries"}'
```

```bash
curl -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 150, "category": "Transport"}'
```

Expected: `{"message": "Expense added successfully"}` (twice)

---

### Step 3 — Check summary

```bash
curl http://localhost:8000/summary
```

Expected:

```json
{
  "total_income": 8000.0,
  "total_expense": 350.0,
  "balance": 7650.0
}
```

---

### Step 4 — Set budget

```bash
curl -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 5000}'
```

Expected: `{"message": "Budget set successfully"}`

---

### Step 5 — Check budget status

```bash
curl http://localhost:8000/budget-status
```

Expected:

```json
{
  "budget": 5000.0,
  "spent": 350.0,
  "remaining": 4650.0
}
```

---

### Step 6 — Test validation (error case)

```bash
curl -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": -100, "source": "Test"}'
```

Expected: HTTP 422 — Pydantic rejects amount=-100 (gt=0 rule violated)

---

## 9. Interactive Documentation

FastAPI automatically generates two interactive documentation interfaces. Both are available once the server is running:

| Interface   | URL                               | Description                                       |
|-------------|-----------------------------------|---------------------------------------------------|
| Swagger UI  | `http://localhost:8000/docs`      | Interactive — try endpoints directly in browser   |
| ReDoc       | `http://localhost:8000/redoc`     | Readable — clean reference layout                 |
| OpenAPI JSON| `http://localhost:8000/openapi.json` | Machine-readable API schema (OpenAPI 3.0)      |

> **Tip:** The Swagger UI at `/docs` is the fastest way to test the API without writing any code. Click on an endpoint, click **Try it out**, fill in the JSON body, and click **Execute**.

---

## 10. Changelog

| Version | Date  | Change |
|---------|-------|--------|
| 1.0     | 2025  | Initial release — 5 endpoints, in-memory storage |
| 1.0     | 2025  | Added Pydantic field constraints (gt=0, min/max len) |
| 1.0     | 2025  | Added Dockerfile for containerised deployment |
| 1.1     | 2026  | Added GET /health endpoint — now 6 endpoints total |
| 1.1     | 2026  | Added response models (SummaryResponse, BudgetStatusResponse, MessageResponse) |
| 1.1     | 2026  | Added Swagger tags, summaries, and docstrings to all endpoints |
| 1.1     | 2026  | Added automated pytest suite — 20 tests, 100% pass rate |
| 1.1     | 2026  | HTTP 422 returned for invalid amounts (Pydantic v2 gt=0 enforcement) |

### Planned for v2

- `GET /income` — list all recorded income entries with source labels
- `GET /expense` — list all expenses with category filter support
- `DELETE /income/{id}` — remove a specific income record
- `DELETE /expense/{id}` — remove a specific expense record
- PostgreSQL persistence via SQLModel
- JWT authentication (Bearer token)
- Per-category budget support

---

*Document ID: DOC-05 | Lightweight Finance API | Yenepoya University | IBM SkillsBuild Project*  
*Version 1.0 | For academic use*
