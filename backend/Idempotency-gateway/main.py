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

# Payment endpoint
@app.post("/process-payment")
async def process_payment(payment: PaymentRequest, idempotency_key: str = Header(..., alias="Idempotency-Key")):

    body = payment.dict()
    existing = store.get(idempotency_key)

    # 1. If key exists already
    if existing:

        if existing["request_body"] != body:
            raise HTTPException(status_code=409, detail="Idempotency key already used for a different request body.")

        # Wait if still processing
        if existing.get("status") == "processing":
            while store[idempotency_key]["status"] != "completed":
                await asyncio.sleep(0.1)

        return JSONResponse(content=existing["response"])

    # 2. MARK AS PROCESSING (THIS IS WHERE YOU PUT IT)
    store[idempotency_key] = {
        "status": "processing",
        "request_body": body,
        "response": None
    }

    # 3. Simulate processing
    await asyncio.sleep(2)

    response_data = {
        "message": f"Charged {payment.amount} {payment.currency}"
    }

    # 4. Mark completed
    store[idempotency_key]["status"] = "completed"
    store[idempotency_key]["response"] = response_data

    return JSONResponse(status_code=201, content=response_data)
       
