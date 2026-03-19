from fastapi import FastAPI
from models import Income, Expense

app = FastAPI()

# In-memory storage
incomes = []
expenses = []   # ✅ NEW

@app.get("/")
def home():
    return {"message": "Finance API is running 🚀"}

# Income API
@app.post("/income")
def add_income(data: Income):
    incomes.append(data.amount)

    return {
        "message": "Income added successfully",
        "amount": data.amount,
        "source": data.source
    }

# ✅ NEW Expense API
@app.post("/expense")
def add_expense(data: Expense):
    expenses.append(data.amount)

    return {
        "message": "Expense added successfully",
        "amount": data.amount,
        "category": data.category
    }
