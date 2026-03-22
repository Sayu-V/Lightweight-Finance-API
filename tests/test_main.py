"""
tests/test_main.py
Automated test suite for the Lightweight Finance API.

Run with:
    py -3.11 -m pytest tests/test_main.py -v

Uses FastAPI TestClient — no server required.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app, incomes, expenses
import main as main_module


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_state():
    """Reset all in-memory storage before and after every test."""
    incomes.clear()
    expenses.clear()
    main_module.budget = 0
    yield
    incomes.clear()
    expenses.clear()
    main_module.budget = 0


@pytest.fixture
def client():
    return TestClient(app)


# ── Health check ──────────────────────────────────────────────────────────────

def test_health_check(client):
    """GET /health returns 200 and running status."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "API is running"


# ── Happy path tests ──────────────────────────────────────────────────────────

def test_add_income_valid(client):
    """Valid income returns 200 and success message."""
    r = client.post("/income", json={"amount": 5000.0, "source": "Salary"})
    assert r.status_code == 200
    assert r.json() == {"message": "Income added successfully"}


def test_add_expense_valid(client):
    """Valid expense returns 200 and success message."""
    r = client.post("/expense", json={"amount": 150.75, "category": "Groceries"})
    assert r.status_code == 200
    assert r.json() == {"message": "Expense added successfully"}


def test_get_summary_empty(client):
    """Summary returns zeros when no data added."""
    r = client.get("/summary")
    assert r.status_code == 200
    assert r.json() == {"total_income": 0, "total_expense": 0, "balance": 0}


def test_get_summary_with_data(client):
    """Summary reflects correct totals after adding records."""
    client.post("/income",  json={"amount": 5000.0, "source": "Salary"})
    client.post("/income",  json={"amount": 2500.0, "source": "Freelance"})
    client.post("/expense", json={"amount": 150.75, "category": "Groceries"})
    client.post("/expense", json={"amount": 80.0,   "category": "Transport"})
    r = client.get("/summary")
    assert r.status_code == 200
    d = r.json()
    assert d["total_income"]  == 7500.0
    assert d["total_expense"] == 230.75
    assert d["balance"]       == 7269.25


def test_set_budget_valid(client):
    """Valid budget returns 200 and success message."""
    r = client.post("/budget", json={"limit": 10000.0})
    assert r.status_code == 200
    assert r.json() == {"message": "Budget set successfully"}


def test_get_budget_status(client):
    """Budget status reflects correct values after setup."""
    client.post("/budget",  json={"limit": 10000.0})
    client.post("/expense", json={"amount": 150.75, "category": "Groceries"})
    client.post("/expense", json={"amount": 80.0,   "category": "Transport"})
    r = client.get("/budget-status")
    assert r.status_code == 200
    d = r.json()
    assert d["budget"]    == 10000.0
    assert d["spent"]     == 230.75
    assert d["remaining"] == 9769.25


# ── Validation & error tests ──────────────────────────────────────────────────

def test_income_zero_amount(client):
    """Amount = 0 rejected by Pydantic gt=0 rule — returns HTTP 422."""
    r = client.post("/income", json={"amount": 0, "source": "Test"})
    assert r.status_code == 422


def test_income_negative_amount(client):
    """Negative amount rejected by Pydantic gt=0 rule — returns HTTP 422."""
    r = client.post("/income", json={"amount": -500, "source": "Test"})
    assert r.status_code == 422


def test_income_missing_source(client):
    """Missing source field returns HTTP 422."""
    r = client.post("/income", json={"amount": 1000})
    assert r.status_code == 422


def test_income_empty_source(client):
    """Empty source string returns HTTP 422."""
    r = client.post("/income", json={"amount": 1000, "source": ""})
    assert r.status_code == 422


def test_expense_negative_amount(client):
    """Negative expense amount rejected by Pydantic gt=0 rule — returns HTTP 422."""
    r = client.post("/expense", json={"amount": -1, "category": "Food"})
    assert r.status_code == 422


def test_expense_missing_category(client):
    """Missing category returns HTTP 422."""
    r = client.post("/expense", json={"amount": 100})
    assert r.status_code == 422


def test_expense_empty_category(client):
    """Empty category string returns HTTP 422."""
    r = client.post("/expense", json={"amount": 100, "category": ""})
    assert r.status_code == 422


def test_budget_zero_limit(client):
    """Budget limit = 0 returns HTTP 422."""
    r = client.post("/budget", json={"limit": 0})
    assert r.status_code == 422


def test_budget_negative_limit(client):
    """Negative budget limit returns HTTP 422."""
    r = client.post("/budget", json={"limit": -500})
    assert r.status_code == 422


# ── Edge case tests ───────────────────────────────────────────────────────────

def test_budget_overwrite(client):
    """Second POST /budget overwrites first value — SET not ADD."""
    client.post("/budget", json={"limit": 5000})
    client.post("/budget", json={"limit": 8000})
    r = client.get("/budget-status")
    assert r.json()["budget"] == 8000.0


def test_over_budget_negative_remaining(client):
    """Spending over budget gives negative remaining — no error raised."""
    client.post("/budget",  json={"limit": 100})
    client.post("/expense", json={"amount": 150, "category": "Shopping"})
    d = client.get("/budget-status").json()
    assert d["budget"]    == 100.0
    assert d["spent"]     == 150.0
    assert d["remaining"] == -50.0


def test_invalid_does_not_affect_state(client):
    """A rejected request does not modify stored data."""
    client.post("/income", json={"amount": 1000, "source": "Valid"})
    client.post("/income", json={"amount": -999, "source": "Bad"})
    assert client.get("/summary").json()["total_income"] == 1000.0


# ── Integration test ──────────────────────────────────────────────────────────

def test_full_workflow(client):
    """Full end-to-end workflow across all 5 endpoints."""
    client.post("/income",  json={"amount": 6000, "source": "Salary"})
    client.post("/income",  json={"amount": 1500, "source": "Freelance"})
    client.post("/expense", json={"amount": 800,  "category": "Rent"})
    client.post("/expense", json={"amount": 250,  "category": "Groceries"})
    client.post("/expense", json={"amount": 100,  "category": "Transport"})

    s = client.get("/summary").json()
    assert s["total_income"]  == 7500.0
    assert s["total_expense"] == 1150.0
    assert s["balance"]       == 6350.0

    client.post("/budget", json={"limit": 5000})
    b = client.get("/budget-status").json()
    assert b["budget"]    == 5000.0
    assert b["spent"]     == 1150.0
    assert b["remaining"] == 3850.0
