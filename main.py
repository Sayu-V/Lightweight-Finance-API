from fastapi import FastAPI, HTTPException
from models import (
    Income, Expense, Budget,
    MessageResponse, SummaryResponse, BudgetStatusResponse
)

app = FastAPI(
    title="Lightweight Finance API",
    description="A simple REST API for tracking personal income, expenses, and budget. Built with FastAPI and Python.",
    version="1.0.0"
)

# ── In-memory storage ─────────────────────────────────────────────────────────
incomes:  list = []    # stores income amounts (float)
expenses: list = []    # stores expense amounts (float)
budget:   float = 0    # stores the monthly budget limit


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"], summary="Health check")
async def health_check():
    """Returns API health status. Useful for monitoring and Docker health probes."""
    return {"status": "API is running"}


# ── Income ────────────────────────────────────────────────────────────────────
@app.post("/income", response_model=MessageResponse, tags=["Finance"], summary="Add income")
def add_income(data: Income):
    """
    Record a new income entry.

    - **amount**: must be greater than 0
    - **source**: label for the income source (e.g. Salary, Freelance)
    """
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    incomes.append(data.amount)
    return {"message": "Income added successfully"}


# ── Expense ───────────────────────────────────────────────────────────────────
@app.post("/expense", response_model=MessageResponse, tags=["Finance"], summary="Add expense")
def add_expense(data: Expense):
    """
    Record a new expense entry.

    - **amount**: must be greater than 0
    - **category**: label for the expense category (e.g. Groceries, Rent)
    """
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    expenses.append(data.amount)
    return {"message": "Expense added successfully"}


# ── Summary ───────────────────────────────────────────────────────────────────
@app.get("/summary", response_model=SummaryResponse, tags=["Finance"], summary="Get financial summary")
def get_summary():
    """
    Returns the current financial summary.

    - **total_income**: sum of all income entries
    - **total_expense**: sum of all expense entries
    - **balance**: total_income minus total_expense (can be negative)
    """
    total_income  = sum(incomes)
    total_expense = sum(expenses)
    return {
        "total_income":  total_income,
        "total_expense": total_expense,
        "balance":       total_income - total_expense
    }


# ── Budget ────────────────────────────────────────────────────────────────────
@app.post("/budget", response_model=MessageResponse, tags=["Budget"], summary="Set monthly budget")
def set_budget(data: Budget):
    """
    Set the monthly spending budget limit.

    - **limit**: must be greater than 0
    - Calling this again overwrites the previous budget (it does not add to it)
    """
    global budget
    budget = data.limit
    return {"message": "Budget set successfully"}


@app.get("/budget-status", response_model=BudgetStatusResponse, tags=["Budget"], summary="Get budget status")
def get_budget_status():
    """
    Returns the current budget status.

    - **budget**: the limit set via POST /budget (0 if never set)
    - **spent**: total amount spent so far (sum of all expenses)
    - **remaining**: budget minus spent (negative means over budget)
    """
    total_expense = sum(expenses)
    return {
        "budget":    budget,
        "spent":     total_expense,
        "remaining": budget - total_expense
    }
