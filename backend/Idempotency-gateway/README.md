Idempotency Gateway (Pay-Once Payment API).

This project is a backend payment system that prevents duplicate transactions using an Idempotency Key . It ensures that even if clients retry requests due to network issues, payments are processed clearly once.
### Tech Stack 

 Backend Framework: FastAPI (Python)
 API Testing: Swagger UI (FastAPI built-in)
 Data Storage: In-memory dictionary (Python Map)



## 1.  The ARCHITECTURE DESIGN

assets/architectureDiagram.png

## 2. SETUP INSTRACTIONS

-   Clone the repository
     cd ~/documents/AmaliTech-DEG-Project-based-challenges.git
-   Install the dependencies
     pip install fastapi uvicorn
-   Run the application
     uvicorn main:app --reload
-   Access the application
     http://localhost:8000

## 3.  API Documentation
    Base url: http://localhost:8000/docs
    1. home endpoints
     GET/

Description:  
 Checks if the API is running.

  Response
   {
      "message": "Idempotency Gateway Running Successfully"
    }
   ### 2. Process Payment Endpoint
       POST /process-payment
       Description:
      Processes a payment request using an Idempotency-Key to prevent duplicate transactions.
      Headers

      Idempotency-Key: abc123 
      Request Body
         {
           "amount": 100,
            "currency": "GHS"
           }
      Success Response (First Request)
          {
            "message": "Charged 100 GHS"
          }
        Status Code: 201 Created 
      Cached Response (Duplicate Request)
          {
            "message": "Charged 100 GHS"
          }
        Status Code: 200 OK
        Headers: X-Cache-Hit: true

      Behavior: Returned instantly without reprocessing the payment.
      Error Response (Same Key, Different Request Body)
          {
            "detail": "Idempotency key already used for a different request body."
          }

          Status Code: 409 Conflict
 ## 4.  DESIGN DECISIONS
### 1. FastAPI Choice
I used FastAPI because it is fast, simple to use, and gives automatic API documentation. It also checks request data easily.

### 2. Data Storage
I used a Python dictionary to store payment data and idempotency keys. This is simple and good for testing. In real systems, a database or Redis would be used.

### 3. Idempotency-Key
Each request uses an Idempotency-Key to make sure the same payment is not processed twice if the client retries the request.

### 4. Cached Response
After a payment is processed, the result is saved. If the same request comes again, the saved result is returned instead of processing again.

### 5. Request Validation
If the same Idempotency-Key is used with different data, the request is rejected with a 409 error. This prevents mistakes or fraud.
### 6. Concurrent Requests
If two requests with the same key arrive at the same time, one waits until the first one finishes. This prevents duplicate processing.
### 7. Simulated Delay
I added a 2-second delay to simulate real payment processing and test how the system handles waiting requests.

## 5. Developer’s Choice: Idempotency Key Expiration

I added a feature that makes idempotency keys expire after a fixed time (e.g. 5 minutes).

### Why I added this
In real payment systems, old keys should not be reused forever. If they are never removed, it can create security risks and use too much memory.

### How it works
 Each request stores a timestamp
 Before using an old key, the system checks its age
If the key is older than 5 minutes, it is deleted
-The request is treated as a new request

### Benefits
 Improves security
Prevents replay attacks
Saves memory
Makes the system closer to real fintech systems

       


