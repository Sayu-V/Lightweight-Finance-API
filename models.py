from pydantic import BaseModel, Field

class Income(BaseModel):
    amount: float = Field(..., gt=0)
    source: str = Field(..., min_length=1, max_length=50)

# ✅ NEW MODEL
class Expense(BaseModel):
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
