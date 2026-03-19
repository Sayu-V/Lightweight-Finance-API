from pydantic import BaseModel, Field

# ✅ INCOME MODEL
class Income(BaseModel):
    amount: float = Field(..., gt=0)
    source: str = Field(..., min_length=1, max_length=50)

# ✅ EXPENSE MODEL
class Expense(BaseModel):
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)

# ✅ BUDGET MODEL
class Budget(BaseModel):
    limit: float = Field(..., gt=0)
