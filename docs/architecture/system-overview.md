
# System Architecture Overview

# 1. Background

The project implements a SOA movie ticketing application.

The implementation uses three services:
Movies, Banking, and Ticketing.

The implementation uses Python and FastAPI, with PostgreSQL
for persistence and Docker for local infrastructure.

# 2. Service Responsibilities

## Movies Service

Owns the movie catalogue.

Responsibilities:
- Create movie records.
- Retrieve movies.
- Update movies.
- Delete movies.
- Search movies by release year.
- Order search results by title or director.


## Banking Service

The Banking service evaluates simulated card payment requests.

It is responsible for:

- Accepting charge requests through HTTP.
- Validating request structure using Pydantic.
- Applying the simulated payment decision rule.
- Returning a payment success or failure result.

### Payment Processing Flow

1. A client submits a charge request.
2. FastAPI validates the incoming JSON.
3. The service applies the payment decision rule.
4. The service returns a JSON response indicating success or failure.

### API Contract

**Endpoint:** `POST /charges`

Request:

    {
        "cardNumber": "12345678",
        "amount": 1500
    }

Response:

    {
        "success": true
    }

### Business Rule

    success = amount > 0 AND len(card_number) % 2 == 0


### Data Ownership

The Banking service currently has no database.

It does not persist card details or transaction records. Its current responsibility is limited to evaluating charge requests.

### Communication

The Ticketing service will communicate with Banking through its HTTP API.

Ticketing will use the returned `success` value to determine whether a booking can proceed.

### Ticketing Service

Owns ticket bookings.

Planned responsibilities:
- Retrieve movies through the Movies API.
- Accept ticket purchase requests.
- Coordinate payment through Banking.
- Record and retrieve bookings.

## 3. Communication

Services will communicate through HTTP APIs using JSON.

Ticketing will act as the orchestration point for the purchase workflow.

No service should directly access another service's database.

## 4. Data Ownership

Each service will own its database.

- Movies owns movie catalogue data.
- Banking owns transaction data.
- Ticketing owns booking data.

## 5. Purchase Workflow

Planned workflow:

1. A customer requests a ticket for a movie.
2. Ticketing requests movie information from Movies.
3. Ticketing validates the requested movie.
4. Ticketing requests payment from Banking.
5. Banking processes and records the simulated transaction.
6. Ticketing records the booking outcome.
7. Ticketing returns the result to the customer.

## 6. Current Implementation

The Movies service has been implemented with FastAPI and SQLAlchemy.

PostgreSQL 16 runs in Docker and stores the movie catalogue.

Banking service has been implemented to simulate card payment requests. 

Ticketing remain pending.

## 7. Architecture Evolution

The initial implementation prioritizes a working service and clear boundaries.

Further improvements will introduce:
- Alembic database migrations.
- Explicit service and repository layers.
- Automated tests.
- Inter-service failure handling.
- More robust booking and payment consistency.
