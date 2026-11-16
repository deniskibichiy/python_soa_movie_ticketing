
# System Architecture Overview

## 1. Background

The project implements a SOA movie ticketing application.

The implementation uses three services:
Movies, Banking, and Ticketing.

The implementation uses Python and FastAPI, with PostgreSQL
for persistence and Docker for local infrastructure.

## 2. Service Responsibilities

### Movies Service

Owns the movie catalogue.

Responsibilities:
- Create movie records.
- Retrieve movies.
- Update movies.
- Delete movies.
- Search movies by release year.
- Order search results by title or director.

### Banking Service

Owns payment processing and transaction records.

Planned responsibilities:
- Accept simulated card payment requests.
- Process payment outcomes.
- Record transactions.
- Return payment success or failure.

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

Banking and Ticketing remain pending.

## 7. Architecture Evolution

The initial implementation prioritizes a working service and clear boundaries.

Further improvements will introduce:
- Alembic database migrations.
- Explicit service and repository layers.
- Automated tests.
- Inter-service failure handling.
- More robust booking and payment consistency.
EOF