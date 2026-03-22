from pydantic import BaseModel, Field


# ── Request Models (input validation) ────────────────────────────────────────

class Income(BaseModel):
    """Request body for POST /income"""
    amount: float = Field(..., gt=0, description="Income amount — must be greater than 0")
    source: str   = Field(..., min_length=1, max_length=50, description="Income source label e.g. Salary")


class Expense(BaseModel):
    """Request body for POST /expense"""
    amount:   float = Field(..., gt=0, description="Expense amount — must be greater than 0")
    category: str   = Field(..., min_length=1, max_length=50, description="Expense category e.g. Groceries")


class Budget(BaseModel):
    """Request body for POST /budget"""
    limit: float = Field(..., gt=0, description="Monthly budget limit — must be greater than 0")


# ── Response Models (output shape) ───────────────────────────────────────────

class MessageResponse(BaseModel):
    """Standard success message response"""
    message: str


class SummaryResponse(BaseModel):
    """Response body for GET /summary"""
    total_income:  float
    total_expense: float
    balance:       float


class BudgetStatusResponse(BaseModel):
    """Response body for GET /budget-status"""
    budget:    float
    spent:     float
    remaining: float
