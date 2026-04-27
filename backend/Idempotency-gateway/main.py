from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Store idempotency data
store = {}

class PaymentRequest(BaseModel):
    amount: int
    currency: str

@app.get("/")
def home():
    return {"message": "Idempotency Gateway Running Successfully"}

@app.post("/process-payment")
async def process_payment(
    payment: PaymentRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key")
):
    body = payment.dict()
    existing = store.get(idempotency_key)

    # Key already exists → return cached response
    if existing:
        return JSONResponse(
            content=existing["response"],
            headers={"X-Cache-Hit": "true"}
        )

    # First request
    await asyncio.sleep(2)

    response_data = {
        "message": f"Charged {payment.amount} {payment.currency}"
    }

    store[idempotency_key] = {
        "request_body": body,
        "response": response_data
    }

    return JSONResponse(status_code=201, content=response_data)