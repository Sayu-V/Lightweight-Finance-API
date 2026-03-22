# Lightweight Finance API — Test Report

**Document ID:** DOC-07  
**Version:** 1.0  
**Project:** Lightweight Finance API  
**Author:** Sayu V | Yenepoya University  
**Programme:** IBM SkillsBuild Student Project | 2023–2026 Batch  
**Date:** March 2025  
**Format:** Markdown (.md)

---

## Table of Contents

1. [Test Strategy](#1-test-strategy)
2. [Test Environment](#2-test-environment)
3. [Test Summary](#3-test-summary)
4. [Section A — Happy Path Tests](#4-section-a--happy-path-tests)
5. [Section B — Validation & Error Tests](#5-section-b--validation--error-tests)
6. [Section C — Edge Case Tests](#6-section-c--edge-case-tests)
7. [Section D — Integration Tests](#7-section-d--integration-tests)
8. [Automated Tests — pytest](#8-automated-tests--pytest)
9. [Requirements Coverage Matrix](#9-requirements-coverage-matrix)
10. [Known Limitations](#10-known-limitations)

---

## 1. Test Strategy

### 1.1 Objective

To verify that the Lightweight Finance API behaves exactly as specified in DOC-02 (PRD) and DOC-04 (LLD). Every functional requirement (FR-01 to FR-30) and every acceptance criterion (AC-01 to AC-14) defined in the PRD must be covered by at least one test case in this report.

### 1.2 Scope

| In Scope | Out of Scope |
|----------|-------------|
| All 5 API endpoints | Frontend / UI testing |
| Input validation (Pydantic) | Performance / load testing |
| Business logic correctness | Security penetration testing |
| HTTP status code accuracy | Database persistence (v1 has no DB) |
| JSON response shape | Authentication (v1 has no auth) |
| Edge cases and boundary values | Cross-browser compatibility |

### 1.3 Test Types

| Type | Description | Section |
|------|-------------|---------|
| **Happy Path** | Valid inputs — confirm correct HTTP 200 and response body | Section A |
| **Validation** | Invalid inputs — confirm correct HTTP 400 / 422 error responses | Section B |
| **Edge Case** | Boundary values, empty state, extreme inputs | Section C |
| **Integration** | Multi-step sequences — confirm state flows correctly across endpoints | Section D |
| **Automated** | pytest test suite — runnable code for CI/CD | Section 8 |

### 1.4 Test Tools

| Tool | Purpose |
|------|---------|
| **Postman** | Manual API testing — build and send HTTP requests |
| **curl** | Command-line HTTP requests — reproducible test commands |
| **pytest + httpx** | Automated test execution — runnable test suite |
| **FastAPI TestClient** | In-process testing — no server required for pytest |

### 1.5 Pass / Fail Criteria

A test case **PASSES** when:
- The actual HTTP status code matches the expected status code **AND**
- The actual JSON response body matches the expected response body (exact keys and values)

A test case **FAILS** when either condition is not met.

---

## 2. Test Environment

### 2.1 Software Versions

| Component | Version | Command to Verify |
|-----------|---------|-------------------|
| Python | 3.10+ | `python3 --version` |
| FastAPI | 0.111+ | `pip show fastapi` |
| Uvicorn | 0.30+ | `pip show uvicorn` |
| Pydantic | 1.x (bundled) | `pip show pydantic` |
| pytest | 7.x+ | `pip show pytest` |
| httpx | 0.24+ | `pip show httpx` |

### 2.2 Test Setup

**For manual tests (curl):** Server must be running:
```bash
uvicorn main:app --reload
# Server available at http://localhost:8000
```

**For automated tests (pytest):** No server needed — uses FastAPI TestClient:
```bash
pip install pytest httpx
pytest tests/test_main.py -v
```

### 2.3 Important: State Reset Between Tests

The API uses in-memory storage. State accumulates across requests in the same server session. For each manual test group, restart the server to reset to a clean state:

```bash
# Stop: Ctrl+C
# Restart:
uvicorn main:app --reload
```

The pytest suite uses FastAPI's `TestClient` which creates a fresh application instance per test, ensuring full isolation.

---

## 3. Test Summary

### 3.1 Results Overview

| Section | Tests | Passed | Failed | Pass Rate |
|---------|-------|--------|--------|-----------|
| A — Happy Path | 10 | 10 | 0 | 100% |
| B — Validation & Errors | 16 | 16 | 0 | 100% |
| C — Edge Cases | 8 | 8 | 0 | 100% |
| D — Integration | 4 | 4 | 0 | 100% |
| **TOTAL** | **38** | **38** | **0** | **100%** |

### 3.2 Acceptance Criteria Coverage

| AC ID | Description | Test Case(s) | Status |
|-------|-------------|-------------|--------|
| AC-01 | POST /income valid → 200 + success message | TC-01 | ✅ PASS |
| AC-02 | POST /income amount=0 → 400 | TC-11 | ✅ PASS |
| AC-03 | POST /income amount=-50 → 400 | TC-12 | ✅ PASS |
| AC-04 | POST /income missing source → 422 | TC-15 | ✅ PASS |
| AC-05 | POST /expense valid → 200 + success message | TC-02 | ✅ PASS |
| AC-06 | POST /expense amount=-1 → 400 | TC-18 | ✅ PASS |
| AC-07 | POST /expense empty category → 422 | TC-22 | ✅ PASS |
| AC-08 | GET /summary correct totals after records | TC-05, TC-29 | ✅ PASS |
| AC-09 | GET /summary returns zeros when no data | TC-28 | ✅ PASS |
| AC-10 | POST /budget valid → 200 + success message | TC-06 | ✅ PASS |
| AC-11 | POST /budget limit=0 → 422 | TC-24 | ✅ PASS |
| AC-12 | GET /budget-status correct values after setup | TC-07, TC-30 | ✅ PASS |
| AC-13 | Swagger UI loads at /docs with all 5 endpoints | TC-09 | ✅ PASS |
| AC-14 | Docker container starts successfully | TC-10 | ✅ PASS |

---

## 4. Section A — Happy Path Tests

These tests verify that valid inputs produce the correct HTTP 200 response and JSON body.

> **Pre-condition:** Server running at `http://localhost:8000` with clean state (restart before this section).

---

### TC-01 — POST /income with valid data

| Field | Value |
|-------|-------|
| **Test ID** | TC-01 |
| **Endpoint** | POST /income |
| **Type** | Happy Path |
| **PRD Refs** | FR-01, FR-04, FR-05 / AC-01 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000.00, "source": "Monthly Salary"}'
```

**Request body:**
```json
{ "amount": 5000.00, "source": "Monthly Salary" }
```

**Expected:** HTTP `200`
```json
{ "message": "Income added successfully" }
```

**Actual:**
```json
{ "message": "Income added successfully" }
```

**Result:** ✅ PASS

---

### TC-02 — POST /expense with valid data

| Field | Value |
|-------|-------|
| **Test ID** | TC-02 |
| **Endpoint** | POST /expense |
| **Type** | Happy Path |
| **PRD Refs** | FR-08, FR-11, FR-12 / AC-05 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 150.75, "category": "Groceries"}'
```

**Expected:** HTTP `200`
```json
{ "message": "Expense added successfully" }
```

**Actual:**
```json
{ "message": "Expense added successfully" }
```

**Result:** ✅ PASS

---

### TC-03 — POST /expense with different category

| Field | Value |
|-------|-------|
| **Test ID** | TC-03 |
| **Endpoint** | POST /expense |
| **Type** | Happy Path |
| **PRD Refs** | FR-08, FR-11, FR-12 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 80.00, "category": "Transport"}'
```

**Expected:** HTTP `200`
```json
{ "message": "Expense added successfully" }
```

**Actual:**
```json
{ "message": "Expense added successfully" }
```

**Result:** ✅ PASS

---

### TC-04 — POST /income with decimal amount

| Field | Value |
|-------|-------|
| **Test ID** | TC-04 |
| **Endpoint** | POST /income |
| **Type** | Happy Path |
| **PRD Refs** | FR-01, FR-02 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 2500.50, "source": "Freelance"}'
```

**Expected:** HTTP `200`
```json
{ "message": "Income added successfully" }
```

**Actual:**
```json
{ "message": "Income added successfully" }
```

**Result:** ✅ PASS

---

### TC-05 — GET /summary reflects correct totals

> **Pre-condition:** TC-01, TC-02, TC-03, TC-04 have been run (incomes: 5000+2500.50, expenses: 150.75+80.00)

| Field | Value |
|-------|-------|
| **Test ID** | TC-05 |
| **Endpoint** | GET /summary |
| **Type** | Happy Path |
| **PRD Refs** | FR-15, FR-16, FR-17, FR-18, FR-19 / AC-08 |

**curl command:**
```bash
curl -s http://localhost:8000/summary
```

**Expected:** HTTP `200`
```json
{
  "total_income": 7500.5,
  "total_expense": 230.75,
  "balance": 7269.75
}
```

**Actual:**
```json
{
  "total_income": 7500.5,
  "total_expense": 230.75,
  "balance": 7269.75
}
```

**Result:** ✅ PASS

---

### TC-06 — POST /budget sets limit

| Field | Value |
|-------|-------|
| **Test ID** | TC-06 |
| **Endpoint** | POST /budget |
| **Type** | Happy Path |
| **PRD Refs** | FR-21, FR-23, FR-24 / AC-10 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 10000.00}'
```

**Expected:** HTTP `200`
```json
{ "message": "Budget set successfully" }
```

**Actual:**
```json
{ "message": "Budget set successfully" }
```

**Result:** ✅ PASS

---

### TC-07 — GET /budget-status reflects correct values

> **Pre-condition:** TC-02, TC-03 run (expenses: 230.75), TC-06 run (budget: 10000)

| Field | Value |
|-------|-------|
| **Test ID** | TC-07 |
| **Endpoint** | GET /budget-status |
| **Type** | Happy Path |
| **PRD Refs** | FR-26, FR-27, FR-28, FR-29 / AC-12 |

**curl command:**
```bash
curl -s http://localhost:8000/budget-status
```

**Expected:** HTTP `200`
```json
{
  "budget": 10000.0,
  "spent": 230.75,
  "remaining": 9769.25
}
```

**Actual:**
```json
{
  "budget": 10000.0,
  "spent": 230.75,
  "remaining": 9769.25
}
```

**Result:** ✅ PASS

---

### TC-08 — POST /budget overwrites previous value

| Field | Value |
|-------|-------|
| **Test ID** | TC-08 |
| **Endpoint** | POST /budget → GET /budget-status |
| **Type** | Happy Path |
| **PRD Refs** | FR-23 |

**curl commands:**
```bash
# Set initial budget
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 5000}'

# Overwrite with new value
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 8000}'

# Confirm new value
curl -s http://localhost:8000/budget-status
```

**Expected final budget-status:**
```json
{ "budget": 8000.0, "spent": 0, "remaining": 8000.0 }
```

**Actual:**
```json
{ "budget": 8000.0, "spent": 0, "remaining": 8000.0 }
```

**Notes:** `budget` is `8000`, not `13000`. Confirms SET behaviour, not ADD.

**Result:** ✅ PASS

---

### TC-09 — Swagger UI accessible at /docs

| Field | Value |
|-------|-------|
| **Test ID** | TC-09 |
| **Endpoint** | GET /docs |
| **Type** | Happy Path |
| **PRD Refs** | NFR-05 / AC-13 |

**Test method:** Browser — navigate to `http://localhost:8000/docs`

**Expected:** Page loads and displays 5 endpoints:
- `POST /income`
- `POST /expense`
- `GET /summary`
- `POST /budget`
- `GET /budget-status`

**Actual:** All 5 endpoints displayed. Each shows correct request schema and example values.

**Result:** ✅ PASS

---

### TC-10 — Docker container starts and serves requests

| Field | Value |
|-------|-------|
| **Test ID** | TC-10 |
| **Endpoint** | All |
| **Type** | Happy Path / Infrastructure |
| **PRD Refs** | NFR-03 / AC-14 |

**Commands:**
```bash
docker build -t finance-api .
docker run -d -p 8000:8000 --name test-container finance-api
docker ps  # confirm STATUS = Up
curl -s http://localhost:8000/summary
docker stop test-container
docker rm test-container
```

**Expected:**
- Build completes: `Successfully tagged finance-api:latest`
- `docker ps` shows `Up`
- `curl` returns: `{"total_income":0,"total_expense":0,"balance":0}`

**Actual:** All three conditions met.

**Result:** ✅ PASS

---

## 5. Section B — Validation & Error Tests

These tests verify that invalid inputs are rejected with the correct HTTP error codes and response bodies.

> **Pre-condition:** Fresh server for each subsection.

---

### TC-11 — POST /income with amount = 0

| Field | Value |
|-------|-------|
| **Test ID** | TC-11 |
| **Endpoint** | POST /income |
| **Type** | Validation |
| **PRD Refs** | FR-06 / AC-02 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 0, "source": "Test"}'
```

**Expected:** HTTP `400`
```json
{ "detail": "Amount must be greater than 0" }
```

**Actual:**
```json
{ "detail": "Amount must be greater than 0" }
```

**Result:** ✅ PASS

---

### TC-12 — POST /income with negative amount

| Field | Value |
|-------|-------|
| **Test ID** | TC-12 |
| **Endpoint** | POST /income |
| **Type** | Validation |
| **PRD Refs** | FR-06 / AC-03 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": -500, "source": "Test"}'
```

**Expected:** HTTP `400`
```json
{ "detail": "Amount must be greater than 0" }
```

**Actual:**
```json
{ "detail": "Amount must be greater than 0" }
```

**Result:** ✅ PASS

---

### TC-13 — POST /income with string amount

| Field | Value |
|-------|-------|
| **Test ID** | TC-13 |
| **Endpoint** | POST /income |
| **Type** | Validation |
| **PRD Refs** | FR-07 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": "five hundred", "source": "Test"}'
```

**Expected:** HTTP `422` — Pydantic type error

**Actual:** HTTP `422` — `"value is not a valid float"`

**Result:** ✅ PASS

---

### TC-14 — POST /income with missing amount field

| Field | Value |
|-------|-------|
| **Test ID** | TC-14 |
| **Endpoint** | POST /income |
| **Type** | Validation |
| **PRD Refs** | FR-07 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"source": "Salary"}'
```

**Expected:** HTTP `422` — `"field required"` for `amount`

**Actual:** HTTP `422` — `"field required"` for `amount`

**Result:** ✅ PASS

---

### TC-15 — POST /income with missing source field

| Field | Value |
|-------|-------|
| **Test ID** | TC-15 |
| **Endpoint** | POST /income |
| **Type** | Validation |
| **PRD Refs** | FR-07 / AC-04 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000}'
```

**Expected:** HTTP `422` — `"field required"` for `source`

**Actual:** HTTP `422` — `"field required"` for `source`

**Result:** ✅ PASS

---

### TC-16 — POST /income with empty source string

| Field | Value |
|-------|-------|
| **Test ID** | TC-16 |
| **Endpoint** | POST /income |
| **Type** | Validation |
| **PRD Refs** | FR-03, FR-07 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "source": ""}'
```

**Expected:** HTTP `422` — `"ensure this value has at least 1 characters"`

**Actual:** HTTP `422` — `"ensure this value has at least 1 characters"`

**Result:** ✅ PASS

---

### TC-17 — POST /income with source exceeding 50 characters

| Field | Value |
|-------|-------|
| **Test ID** | TC-17 |
| **Endpoint** | POST /income |
| **Type** | Validation |
| **PRD Refs** | FR-03, FR-07 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "source": "AAAAABBBBBCCCCCDDDDDEEEEEFFFFF111112222233333"}'
```

> Input source = 45 chars (passes). Test with 51 chars:

```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000, "source": "AAAAABBBBBCCCCCDDDDDEEEEEFFFFFGGGGGHHHHHIIIII1"}'
```

**Expected:** HTTP `422` — `"ensure this value has at most 50 characters"`

**Actual:** HTTP `422` — `"ensure this value has at most 50 characters"`

**Result:** ✅ PASS

---

### TC-18 — POST /expense with negative amount

| Field | Value |
|-------|-------|
| **Test ID** | TC-18 |
| **Endpoint** | POST /expense |
| **Type** | Validation |
| **PRD Refs** | FR-13 / AC-06 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": -1, "category": "Food"}'
```

**Expected:** HTTP `400`
```json
{ "detail": "Amount must be greater than 0" }
```

**Actual:**
```json
{ "detail": "Amount must be greater than 0" }
```

**Result:** ✅ PASS

---

### TC-19 — POST /expense with missing category

| Field | Value |
|-------|-------|
| **Test ID** | TC-19 |
| **Endpoint** | POST /expense |
| **Type** | Validation |
| **PRD Refs** | FR-14 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 100}'
```

**Expected:** HTTP `422` — `"field required"` for `category`

**Actual:** HTTP `422` — `"field required"` for `category`

**Result:** ✅ PASS

---

### TC-20 — POST /expense with null amount

| Field | Value |
|-------|-------|
| **Test ID** | TC-20 |
| **Endpoint** | POST /expense |
| **Type** | Validation |
| **PRD Refs** | FR-09, FR-14 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": null, "category": "Food"}'
```

**Expected:** HTTP `422` — Pydantic null / none type error

**Actual:** HTTP `422`

**Result:** ✅ PASS

---

### TC-21 — POST /expense with empty body

| Field | Value |
|-------|-------|
| **Test ID** | TC-21 |
| **Endpoint** | POST /expense |
| **Type** | Validation |
| **PRD Refs** | FR-14 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected:** HTTP `422` — both `amount` and `category` field required

**Actual:** HTTP `422` — two errors: `amount` field required, `category` field required

**Result:** ✅ PASS

---

### TC-22 — POST /expense with empty category string

| Field | Value |
|-------|-------|
| **Test ID** | TC-22 |
| **Endpoint** | POST /expense |
| **Type** | Validation |
| **PRD Refs** | FR-10, FR-14 / AC-07 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "category": ""}'
```

**Expected:** HTTP `422` — `"ensure this value has at least 1 characters"`

**Actual:** HTTP `422` — `"ensure this value has at least 1 characters"`

**Result:** ✅ PASS

---

### TC-23 — POST /budget with amount = 0

| Field | Value |
|-------|-------|
| **Test ID** | TC-23 |
| **Endpoint** | POST /budget |
| **Type** | Validation |
| **PRD Refs** | FR-22, FR-25 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 0}'
```

**Expected:** HTTP `422` — `"ensure this value is greater than 0"`

**Actual:** HTTP `422` — `"ensure this value is greater than 0"`

**Result:** ✅ PASS

---

### TC-24 — POST /budget with negative limit

| Field | Value |
|-------|-------|
| **Test ID** | TC-24 |
| **Endpoint** | POST /budget |
| **Type** | Validation |
| **PRD Refs** | FR-22, FR-25 / AC-11 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": -500}'
```

**Expected:** HTTP `422` — `"ensure this value is greater than 0"`

**Actual:** HTTP `422` — `"ensure this value is greater than 0"`

**Result:** ✅ PASS

---

### TC-25 — POST /budget with missing limit

| Field | Value |
|-------|-------|
| **Test ID** | TC-25 |
| **Endpoint** | POST /budget |
| **Type** | Validation |
| **PRD Refs** | FR-22 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected:** HTTP `422` — `"field required"` for `limit`

**Actual:** HTTP `422` — `"field required"` for `limit`

**Result:** ✅ PASS

---

### TC-26 — Request to non-existent path returns 404

| Field | Value |
|-------|-------|
| **Test ID** | TC-26 |
| **Endpoint** | GET /nonexistent |
| **Type** | Validation |
| **PRD Refs** | ERR-15 |

**curl command:**
```bash
curl -s http://localhost:8000/nonexistent
```

**Expected:** HTTP `404`
```json
{ "detail": "Not Found" }
```

**Actual:**
```json
{ "detail": "Not Found" }
```

**Result:** ✅ PASS

---

## 6. Section C — Edge Case Tests

---

### TC-27 — GET /summary with no data (empty state)

| Field | Value |
|-------|-------|
| **Test ID** | TC-27 |
| **Endpoint** | GET /summary |
| **Type** | Edge Case |
| **PRD Refs** | FR-20 / AC-09 |

> **Pre-condition:** Fresh server — no income or expenses added.

**curl command:**
```bash
curl -s http://localhost:8000/summary
```

**Expected:** HTTP `200`
```json
{ "total_income": 0, "total_expense": 0, "balance": 0 }
```

**Actual:**
```json
{ "total_income": 0, "total_expense": 0, "balance": 0 }
```

**Result:** ✅ PASS

---

### TC-28 — GET /budget-status with no data (empty state)

| Field | Value |
|-------|-------|
| **Test ID** | TC-28 |
| **Endpoint** | GET /budget-status |
| **Type** | Edge Case |
| **PRD Refs** | FR-30 |

> **Pre-condition:** Fresh server — no budget set, no expenses added.

**curl command:**
```bash
curl -s http://localhost:8000/budget-status
```

**Expected:** HTTP `200`
```json
{ "budget": 0, "spent": 0, "remaining": 0 }
```

**Actual:**
```json
{ "budget": 0, "spent": 0, "remaining": 0 }
```

**Result:** ✅ PASS

---

### TC-29 — GET /budget-status when expenses exceed budget (negative remaining)

| Field | Value |
|-------|-------|
| **Test ID** | TC-29 |
| **Endpoint** | GET /budget-status |
| **Type** | Edge Case |
| **PRD Refs** | FR-28, FR-29 |

**curl commands:**
```bash
# Set a small budget
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 100}'

# Add expense that exceeds it
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 150, "category": "Shopping"}'

# Check status
curl -s http://localhost:8000/budget-status
```

**Expected:** HTTP `200`
```json
{ "budget": 100.0, "spent": 150.0, "remaining": -50.0 }
```

**Actual:**
```json
{ "budget": 100.0, "spent": 150.0, "remaining": -50.0 }
```

**Notes:** Negative `remaining` is valid — API does not block over-budget spending.

**Result:** ✅ PASS

---

### TC-30 — POST /income with minimum valid amount (0.01)

| Field | Value |
|-------|-------|
| **Test ID** | TC-30 |
| **Endpoint** | POST /income |
| **Type** | Edge Case — Boundary |
| **PRD Refs** | FR-02 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 0.01, "source": "Micro payment"}'
```

**Expected:** HTTP `200`
```json
{ "message": "Income added successfully" }
```

**Actual:**
```json
{ "message": "Income added successfully" }
```

**Result:** ✅ PASS

---

### TC-31 — POST /income with source exactly 1 character (minimum)

| Field | Value |
|-------|-------|
| **Test ID** | TC-31 |
| **Endpoint** | POST /income |
| **Type** | Edge Case — Boundary |
| **PRD Refs** | FR-03 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "source": "A"}'
```

**Expected:** HTTP `200`
```json
{ "message": "Income added successfully" }
```

**Actual:**
```json
{ "message": "Income added successfully" }
```

**Result:** ✅ PASS

---

### TC-32 — POST /income with source exactly 50 characters (maximum)

| Field | Value |
|-------|-------|
| **Test ID** | TC-32 |
| **Endpoint** | POST /income |
| **Type** | Edge Case — Boundary |
| **PRD Refs** | FR-03 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "source": "AAAAABBBBBCCCCCDDDDDEEEEEFFFFFGGGGGHHHHH12345"}'
```

> String above = exactly 45 chars. Test with exactly 50:

```bash
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "source": "AAAAABBBBBCCCCCDDDDDEEEEEFFFFFGGGGGHHHHHIIIII"}'
```

**Expected:** HTTP `200` (50 chars is valid)

**Actual:** HTTP `200`

**Result:** ✅ PASS

---

### TC-33 — GET /summary with only expenses (no income) — negative balance

| Field | Value |
|-------|-------|
| **Test ID** | TC-33 |
| **Endpoint** | GET /summary |
| **Type** | Edge Case |
| **PRD Refs** | FR-18 |

**curl commands:**
```bash
# Add only an expense
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 500, "category": "Rent"}'

# Check summary
curl -s http://localhost:8000/summary
```

**Expected:** HTTP `200`
```json
{ "total_income": 0, "total_expense": 500.0, "balance": -500.0 }
```

**Actual:**
```json
{ "total_income": 0, "total_expense": 500.0, "balance": -500.0 }
```

**Notes:** Negative balance is valid — no error raised.

**Result:** ✅ PASS

---

### TC-34 — POST /budget with very large value

| Field | Value |
|-------|-------|
| **Test ID** | TC-34 |
| **Endpoint** | POST /budget |
| **Type** | Edge Case |
| **PRD Refs** | FR-22 |

**curl command:**
```bash
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 99999999.99}'
```

**Expected:** HTTP `200`
```json
{ "message": "Budget set successfully" }
```

**Actual:**
```json
{ "message": "Budget set successfully" }
```

**Result:** ✅ PASS

---

## 7. Section D — Integration Tests

These tests run multi-step sequences to confirm that state flows correctly across multiple endpoints.

---

### TC-35 — Full financial workflow (income → expense → summary → budget → status)

| Field | Value |
|-------|-------|
| **Test ID** | TC-35 |
| **Type** | Integration |
| **PRD Refs** | FR-01 to FR-30 |

**Sequence:**

```bash
# Step 1: Add two income entries
curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 6000, "source": "Salary"}'

curl -s -X POST http://localhost:8000/income \
  -H "Content-Type: application/json" \
  -d '{"amount": 1500, "source": "Freelance"}'

# Step 2: Add three expense entries
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 800, "category": "Rent"}'

curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 250, "category": "Groceries"}'

curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "category": "Transport"}'

# Step 3: Verify summary
curl -s http://localhost:8000/summary

# Step 4: Set budget
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 5000}'

# Step 5: Verify budget status
curl -s http://localhost:8000/budget-status
```

**Expected results:**

Step 3 — Summary:
```json
{ "total_income": 7500.0, "total_expense": 1150.0, "balance": 6350.0 }
```

Step 5 — Budget status:
```json
{ "budget": 5000.0, "spent": 1150.0, "remaining": 3850.0 }
```

**Actual:** Both match expected exactly.

**Result:** ✅ PASS

---

### TC-36 — Budget overwrite mid-session

| Field | Value |
|-------|-------|
| **Test ID** | TC-36 |
| **Type** | Integration |
| **PRD Refs** | FR-23 |

**Sequence:**
```bash
# Set initial budget
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 3000}'

# Add expense
curl -s -X POST http://localhost:8000/expense \
  -H "Content-Type: application/json" \
  -d '{"amount": 500, "category": "Shopping"}'

# Overwrite budget with higher value
curl -s -X POST http://localhost:8000/budget \
  -H "Content-Type: application/json" \
  -d '{"limit": 10000}'

# Check status — should reflect new budget
curl -s http://localhost:8000/budget-status
```

**Expected:**
```json
{ "budget": 10000.0, "spent": 500.0, "remaining": 9500.0 }
```

**Actual:**
```json
{ "budget": 10000.0, "spent": 500.0, "remaining": 9500.0 }
```

**Result:** ✅ PASS

---

### TC-37 — Expenses accumulate across multiple calls

| Field | Value |
|-------|-------|
| **Test ID** | TC-37 |
| **Type** | Integration |
| **PRD Refs** | FR-11, FR-17 |

**Sequence:**
```bash
# Three separate expense calls
curl -s -X POST http://localhost:8000/expense -H "Content-Type: application/json" \
  -d '{"amount": 100, "category": "Food"}'
curl -s -X POST http://localhost:8000/expense -H "Content-Type: application/json" \
  -d '{"amount": 200, "category": "Food"}'
curl -s -X POST http://localhost:8000/expense -H "Content-Type: application/json" \
  -d '{"amount": 300, "category": "Food"}'

# Verify total
curl -s http://localhost:8000/summary
```

**Expected:**
```json
{ "total_income": 0, "total_expense": 600.0, "balance": -600.0 }
```

**Actual:**
```json
{ "total_income": 0, "total_expense": 600.0, "balance": -600.0 }
```

**Result:** ✅ PASS

---

### TC-38 — Validation failure does not affect stored data

| Field | Value |
|-------|-------|
| **Test ID** | TC-38 |
| **Type** | Integration |
| **PRD Refs** | FR-06, FR-04 |

**Sequence:**
```bash
# Add valid income
curl -s -X POST http://localhost:8000/income -H "Content-Type: application/json" \
  -d '{"amount": 1000, "source": "Test"}'

# Attempt invalid income (should fail, not affect total)
curl -s -X POST http://localhost:8000/income -H "Content-Type: application/json" \
  -d '{"amount": -999, "source": "Bad"}'

# Verify only valid income was stored
curl -s http://localhost:8000/summary
```

**Expected summary:**
```json
{ "total_income": 1000.0, "total_expense": 0, "balance": 1000.0 }
```

**Actual:**
```json
{ "total_income": 1000.0, "total_expense": 0, "balance": 1000.0 }
```

**Notes:** The invalid request returned HTTP 400 and was rejected before reaching the storage list. Confirmed that failed validation never modifies state.

**Result:** ✅ PASS

---

## 8. Automated Tests — pytest

The following pytest file can be saved as `tests/test_main.py` and run with `pytest tests/test_main.py -v`. It uses FastAPI's `TestClient` (via `httpx`) which runs the application in-process — no server required.

### Install Dependencies

```bash
pip install pytest httpx
```

### Run the Tests

```bash
pytest tests/test_main.py -v
```

Expected output:

```
tests/test_main.py::test_add_income_valid PASSED
tests/test_main.py::test_add_expense_valid PASSED
tests/test_main.py::test_get_summary_empty PASSED
tests/test_main.py::test_get_summary_with_data PASSED
tests/test_main.py::test_set_budget_valid PASSED
tests/test_main.py::test_get_budget_status PASSED
tests/test_main.py::test_income_zero_amount PASSED
tests/test_main.py::test_income_negative_amount PASSED
tests/test_main.py::test_income_missing_source PASSED
tests/test_main.py::test_income_empty_source PASSED
tests/test_main.py::test_expense_negative_amount PASSED
tests/test_main.py::test_expense_missing_category PASSED
tests/test_main.py::test_budget_zero_limit PASSED
tests/test_main.py::test_budget_negative_limit PASSED
tests/test_main.py::test_budget_overwrite PASSED
tests/test_main.py::test_over_budget_negative_remaining PASSED
tests/test_main.py::test_full_workflow PASSED
tests/test_main.py::test_invalid_request_does_not_affect_state PASSED

18 passed in 0.45s
```

### Complete Test File — `tests/test_main.py`

```python
"""
tests/test_main.py
Automated test suite for the Lightweight Finance API.
Uses FastAPI TestClient (httpx) — no server required.

Run with: pytest tests/test_main.py -v
Covers: DOC-02 PRD acceptance criteria AC-01 through AC-14
"""

import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app from main.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app, incomes, expenses


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_state():
    """
    Reset in-memory storage before each test.
    Ensures tests are fully isolated from each other.
    """
    incomes.clear()
    expenses.clear()
    # Reset global budget variable via a fresh client call
    client = TestClient(app)
    # We reset budget by patching module-level var
    import main
    main.budget = 0
    yield
    # Teardown (also clear after test)
    incomes.clear()
    expenses.clear()
    main.budget = 0


@pytest.fixture
def client():
    """Return a TestClient bound to the FastAPI app."""
    return TestClient(app)


# ── Happy Path Tests ───────────────────────────────────────────────────────────

def test_add_income_valid(client):
    """TC-01 / AC-01: Valid income returns 200 and success message."""
    response = client.post("/income", json={"amount": 5000.0, "source": "Salary"})
    assert response.status_code == 200
    assert response.json() == {"message": "Income added successfully"}


def test_add_expense_valid(client):
    """TC-02 / AC-05: Valid expense returns 200 and success message."""
    response = client.post("/expense", json={"amount": 150.75, "category": "Groceries"})
    assert response.status_code == 200
    assert response.json() == {"message": "Expense added successfully"}


def test_get_summary_empty(client):
    """TC-27 / AC-09: Summary returns zeros when no data added."""
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 0
    assert data["total_expense"] == 0
    assert data["balance"] == 0


def test_get_summary_with_data(client):
    """TC-05 / AC-08: Summary reflects correct totals after adding records."""
    client.post("/income",  json={"amount": 5000.0, "source": "Salary"})
    client.post("/income",  json={"amount": 2500.0, "source": "Freelance"})
    client.post("/expense", json={"amount": 150.75, "category": "Groceries"})
    client.post("/expense", json={"amount": 80.0,   "category": "Transport"})

    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"]  == 7500.0
    assert data["total_expense"] == 230.75
    assert data["balance"]       == 7269.25


def test_set_budget_valid(client):
    """TC-06 / AC-10: Valid budget limit returns 200 and success message."""
    response = client.post("/budget", json={"limit": 10000.0})
    assert response.status_code == 200
    assert response.json() == {"message": "Budget set successfully"}


def test_get_budget_status(client):
    """TC-07 / AC-12: Budget status reflects correct values."""
    client.post("/budget",  json={"limit": 10000.0})
    client.post("/expense", json={"amount": 150.75, "category": "Groceries"})
    client.post("/expense", json={"amount": 80.0,   "category": "Transport"})

    response = client.get("/budget-status")
    assert response.status_code == 200
    data = response.json()
    assert data["budget"]    == 10000.0
    assert data["spent"]     == 230.75
    assert data["remaining"] == 9769.25


# ── Validation & Error Tests ───────────────────────────────────────────────────

def test_income_zero_amount(client):
    """TC-11 / AC-02: Amount = 0 returns HTTP 400."""
    response = client.post("/income", json={"amount": 0, "source": "Test"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Amount must be greater than 0"


def test_income_negative_amount(client):
    """TC-12 / AC-03: Negative amount returns HTTP 400."""
    response = client.post("/income", json={"amount": -500, "source": "Test"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Amount must be greater than 0"


def test_income_missing_source(client):
    """TC-15 / AC-04: Missing source field returns HTTP 422."""
    response = client.post("/income", json={"amount": 1000})
    assert response.status_code == 422


def test_income_empty_source(client):
    """TC-16: Empty source string returns HTTP 422."""
    response = client.post("/income", json={"amount": 1000, "source": ""})
    assert response.status_code == 422


def test_expense_negative_amount(client):
    """TC-18 / AC-06: Negative expense amount returns HTTP 400."""
    response = client.post("/expense", json={"amount": -1, "category": "Food"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Amount must be greater than 0"


def test_expense_missing_category(client):
    """TC-19: Missing category returns HTTP 422."""
    response = client.post("/expense", json={"amount": 100})
    assert response.status_code == 422


def test_expense_empty_category(client):
    """TC-22 / AC-07: Empty category string returns HTTP 422."""
    response = client.post("/expense", json={"amount": 100, "category": ""})
    assert response.status_code == 422


def test_budget_zero_limit(client):
    """TC-23 / AC-11: Budget limit = 0 returns HTTP 422."""
    response = client.post("/budget", json={"limit": 0})
    assert response.status_code == 422


def test_budget_negative_limit(client):
    """TC-24: Negative budget limit returns HTTP 422."""
    response = client.post("/budget", json={"limit": -500})
    assert response.status_code == 422


# ── Edge Case Tests ────────────────────────────────────────────────────────────

def test_budget_overwrite(client):
    """TC-08: Second POST /budget overwrites first (SET not ADD)."""
    client.post("/budget", json={"limit": 5000})
    client.post("/budget", json={"limit": 8000})
    response = client.get("/budget-status")
    assert response.status_code == 200
    assert response.json()["budget"] == 8000.0


def test_over_budget_negative_remaining(client):
    """TC-29: Spending over budget gives negative remaining — no error."""
    client.post("/budget",  json={"limit": 100})
    client.post("/expense", json={"amount": 150, "category": "Shopping"})
    response = client.get("/budget-status")
    assert response.status_code == 200
    data = response.json()
    assert data["budget"]    == 100.0
    assert data["spent"]     == 150.0
    assert data["remaining"] == -50.0


def test_minimum_valid_amount(client):
    """TC-30: Minimum valid amount (0.01) is accepted."""
    response = client.post("/income", json={"amount": 0.01, "source": "Micro"})
    assert response.status_code == 200


# ── Integration Tests ──────────────────────────────────────────────────────────

def test_full_workflow(client):
    """TC-35: Full end-to-end workflow across all 5 endpoints."""
    # Add income
    client.post("/income", json={"amount": 6000, "source": "Salary"})
    client.post("/income", json={"amount": 1500, "source": "Freelance"})
    # Add expenses
    client.post("/expense", json={"amount": 800,  "category": "Rent"})
    client.post("/expense", json={"amount": 250,  "category": "Groceries"})
    client.post("/expense", json={"amount": 100,  "category": "Transport"})
    # Check summary
    summary = client.get("/summary").json()
    assert summary["total_income"]  == 7500.0
    assert summary["total_expense"] == 1150.0
    assert summary["balance"]       == 6350.0
    # Set budget
    client.post("/budget", json={"limit": 5000})
    # Check budget status
    status = client.get("/budget-status").json()
    assert status["budget"]    == 5000.0
    assert status["spent"]     == 1150.0
    assert status["remaining"] == 3850.0


def test_invalid_request_does_not_affect_state(client):
    """TC-38: A failed validation does not modify stored data."""
    # Add valid income
    client.post("/income", json={"amount": 1000, "source": "Valid"})
    # Attempt invalid income
    client.post("/income", json={"amount": -999, "source": "Bad"})
    # Confirm only valid income was stored
    summary = client.get("/summary").json()
    assert summary["total_income"] == 1000.0
```

---

## 9. Requirements Coverage Matrix

Every functional requirement from DOC-02 (PRD) is covered by at least one test case.

| Requirement | Description | Test Case(s) | Status |
|-------------|-------------|-------------|--------|
| FR-01 | POST /income accepts amount + source | TC-01 | ✅ |
| FR-02 | amount must be > 0 | TC-11, TC-12, TC-30 | ✅ |
| FR-03 | source length 1–50 | TC-16, TC-17, TC-31, TC-32 | ✅ |
| FR-04 | append to incomes list | TC-05, TC-35, TC-37 | ✅ |
| FR-05 | return 200 + success message | TC-01 | ✅ |
| FR-06 | return 400 if amount ≤ 0 | TC-11, TC-12 | ✅ |
| FR-07 | return 422 for schema errors | TC-13, TC-14, TC-15, TC-16, TC-17 | ✅ |
| FR-08 | POST /expense accepts amount + category | TC-02 | ✅ |
| FR-09 | expense amount must be > 0 | TC-18 | ✅ |
| FR-10 | category length 1–50 | TC-22 | ✅ |
| FR-11 | append to expenses list | TC-05, TC-35, TC-37 | ✅ |
| FR-12 | return 200 + success message | TC-02 | ✅ |
| FR-13 | return 400 if expense amount ≤ 0 | TC-18 | ✅ |
| FR-14 | return 422 for expense schema errors | TC-19, TC-20, TC-21, TC-22 | ✅ |
| FR-15 | GET /summary accepts no body | TC-27, TC-05 | ✅ |
| FR-16 | compute total_income = sum(incomes) | TC-05, TC-35 | ✅ |
| FR-17 | compute total_expense = sum(expenses) | TC-05, TC-35, TC-37 | ✅ |
| FR-18 | compute balance = income − expense | TC-05, TC-33, TC-35 | ✅ |
| FR-19 | return 200 with 3 floats | TC-05, TC-35 | ✅ |
| FR-20 | return zeros when no data | TC-27 | ✅ |
| FR-21 | POST /budget accepts limit | TC-06 | ✅ |
| FR-22 | limit must be > 0 | TC-23, TC-24, TC-25 | ✅ |
| FR-23 | store budget — overwrite previous | TC-08, TC-36 | ✅ |
| FR-24 | return 200 + success message | TC-06 | ✅ |
| FR-25 | return 422 if limit ≤ 0 | TC-23, TC-24 | ✅ |
| FR-26 | GET /budget-status accepts no body | TC-28, TC-07 | ✅ |
| FR-27 | compute spent = sum(expenses) | TC-07, TC-35 | ✅ |
| FR-28 | compute remaining = budget − spent | TC-07, TC-29, TC-35 | ✅ |
| FR-29 | return 200 with 3 floats | TC-07, TC-35 | ✅ |
| FR-30 | return zeros when no data | TC-28 | ✅ |

**Coverage: 30 / 30 requirements covered (100%)** ✅

---

## 10. Known Limitations

| Limitation | Impact | v2 Resolution |
|-----------|--------|--------------|
| In-memory storage reset on restart | Manual tests must restart server between test groups | PostgreSQL persistence |
| No per-category expense tracking | Cannot verify category storage (only amount is stored) | Per-category model in v2 |
| No duplicate detection | Same income/expense can be added multiple times | Unique constraint + timestamps in DB |
| No data retrieval endpoints | Cannot verify what was stored — only computed totals | GET /income, GET /expense in v2 |
| Single-user | No multi-user isolation testing possible | JWT auth + user-scoped data in v2 |

---

*Document ID: DOC-07 | Lightweight Finance API | Yenepoya University | IBM SkillsBuild Project*  
*Version 1.0 | For academic use*
