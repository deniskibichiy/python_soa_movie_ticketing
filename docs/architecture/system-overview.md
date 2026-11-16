
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

## Ticketing Service

The Ticketing service coordinates movie discovery and ticket purchases.

It is responsible for:

- Retrieve movies released in a specified year.
- Communicate with Movies to retrieve movie information.
- Submit simulated payment requests to Banking.
- Calculate ticket payment amounts.
- Maintain ticket counts grouped by movie ID.

### Service Communication

Ticketing communicates with downstream services through HTTP JSON APIs.

**Movies integration**

1. Receives a year from the client.
2. Calls `GET /movies/find` on Movies.
3. Retrieves each matching movie using `GET /movies/{id}`.
4. Returns a simplified list containing movie IDs and titles.

**Banking integration**

1. Receives a ticket purchase request.
2. Verifies that the movie exists.
3. Calculates the charge using `count * 10`.
4. Calls `POST /charges` on Banking.
5. Updates ticket counts only when payment succeeds.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/GetMovies` | Retrieve movies by year |
| POST | `/BuyTickets` | Purchase tickets |
| POST | `/GetTickets` | Retrieve ticket counts |

### Current Data Management

Ticket counts are currently stored in an in-memory dictionary.

This preserves the original Java implementation but means ticket counts are lost when the service restarts.

Persistent storage is planned as a subsequent improvement.

# 3. Integrated System Workflow

The current system has three independently running services:

1. Movies manages movie catalogue data.
2. Banking evaluates simulated card charges.
3. Ticketing orchestrates movie discovery and ticket purchases.

The services communicate through HTTP and JSON rather than directly importing one another's business logic.

# 4. Planned Client Interface

A lightweight browser interface will be added using:

- HTML for page structure.
- CSS for styling and layout.
- JavaScript for API requests and dynamic updates.

The browser interface will communicate with the Ticketing API. It will not access the Movies or Banking databases directly.


# 5. Communication

Services will communicate through HTTP APIs using JSON.

Ticketing will act as the orchestration point for the purchase workflow.

No service should directly access another service's database.

# 6. Data Ownership

Each service owns its database.

- Movies owns movie catalogue data.
- Banking owns transaction data (No persistence of transaction data has been currently implemented).
- Ticketing owns booking data.

# 7. Purchase Workflow

Planned workflow:

1. A customer requests a ticket for a movie.
2. Ticketing requests movie information from Movies.
3. Ticketing validates the requested movie.
4. Ticketing requests payment from Banking.
5. Banking processes and records the simulated transaction.
6. Ticketing records the booking outcome.
7. Ticketing returns the result to the customer.

# 8. Current Implementation

The Movies service has been implemented with FastAPI and SQLAlchemy.

PostgreSQL 16 runs in Docker and stores the movie catalogue.

Banking service has been implemented to simulate card payment requests. 

Ticketing service has been implemented.

## Containerized Deployment

The three application services and the PostgreSQL database are orchestrated through Docker Compose.

Each application service runs in its own container:

- Movies owns the movie catalogue and PostgreSQL integration.
- Banking handles simulated payment authorization.
- Ticketing coordinates movie retrieval, payment authorization, and ticket-count updates.

The services communicate over the internal Docker network using Compose service names. The database is exposed on host port 5433 for development access, while the APIs are exposed on ports 8001, 8002, and 8003.

PostgreSQL data is stored in a named Docker volume so that it survives ordinary container recreation.

The deployment configuration is maintained in `infrastructure/docker-compose.yml`.

# 9. Browser-Based Frontend

The system includes a lightweight browser interface implemented with HTML, CSS, and vanilla JavaScript.

The frontend communicates exclusively with the Ticketing API.

The interaction flow is:

1. A user searches for movies by year.
2. The frontend sends a request to Ticketing.
3. Ticketing retrieves movie information from Movies.
4. The user selects a movie and requests tickets.
5. Ticketing requests payment authorization from Banking.
6. Ticketing updates its ticket counts after successful authorization.
7. The frontend can retrieve and display ticket counts.

The frontend is served independently during development using Python's built-in HTTP server on port 5500.

CORS middleware on Ticketing permits the development frontend origins.

This keeps the frontend separate from the backend service implementations.