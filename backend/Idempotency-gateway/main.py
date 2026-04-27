from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Request model
class PaymentRequest(BaseModel):
    amount: int
    currency: str

# Home route
@app.get("/")
def home():
    return {"message": "Idempotency Gateway Running Successfully"}

# Payment endpoint (basic skeleton only)
@app.post("/process-payment")
def process_payment(payment: PaymentRequest):
    return {
        "message": f"Received payment request of {payment.amount} {payment.currency}"
    }