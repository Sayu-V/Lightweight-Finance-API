from fastapi import FastAPI
from models import Income

app = FastAPI()

# In-memory storage
incomes = []

@app.get("/")
def home():
    return {"message": "Finance API is running 🚀"}

# ✅ NEW ENDPOINT
@app.post("/income")
def add_income(data: Income):
    incomes.append(data.amount)

    return {
        "message": "Income added successfully",
        "amount": data.amount,
        "source": data.source
    }
