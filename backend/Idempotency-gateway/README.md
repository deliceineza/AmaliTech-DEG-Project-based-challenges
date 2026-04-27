Idempotency Gateway (Pay-Once Payment API).

This project is a backend payment system that prevents duplicate transactions using an Idempotency Key . It ensures that even if clients retry requests due to network issues, payments are processed clearly once.



1.  The Architecture Diagram

assets/architectureDiagram.png

2. SETUP INSTRACTIONS

-   Clone the repository
     cd ~/documents/AmaliTech-DEG-Project-based-challenges.git
-   Install the dependencies
     pip install fastapi uvicorn
-   Run the application
     uvicorn main:app --reload
-   Access the application
     http://localhost:8000

3.  API Documentation
    Base url: http://localhost:8000
    1. home endpoints
     GET/

**Description:**  
 Checks if the API is running.

  **Response:**
   {
      "message": "Idempotency Gateway Running Successfully"
    }
  2. Process Payment Endpoint
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
       


