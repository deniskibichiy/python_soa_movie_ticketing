
# Python SOA Movie Ticketing System

An implementation of a Python-based Service-Oriented Architecture (SOA) movie ticketing application.

The system consists of three services:

- **Movies:** Movie catalogue management and search.
- **Banking:** Simulated card payment processing.
- **Ticketing:** Ticket purchase orchestration and booking management.


## Architecture

The system is designed around three independently deployable services.

| Service | Responsibility | Technology |
|---|---|---|
| Movies | Movie catalogue and search | FastAPI, SQLAlchemy, PostgreSQL |
| Banking | Payment simulation and transaction records | FastAPI, SQLAlchemy, PostgreSQL |
| Ticketing | Booking management and service orchestration | FastAPI, SQLAlchemy, PostgreSQL |

Each service will own its data and expose HTTP APIs. Services will communicate through their APIs rather than accessing one another's databases.

## Technology Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- PostgreSQL 16
- Docker Compose
- Pytest
- HTTPX

## Repository Structure

```text
python_soa_movie_ticketing/
├── docs/
│   ├── api-contracts/
│   ├── architecture/
│   └── decisions/
├── infrastructure/
│   ├── docker-compose.yml
│   └── postgres/
├── scripts/
├── services/
│   ├── banking/
│   │   ├── app/
│   │   └── tests/
│   ├── movies/
│   │   ├── app/
│   │   └── tests/
│   └── ticketing/
│       ├── app/
│       └── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Current Implementation Status

### 1. Movies Service

**Port:** 8001

Responsible for managing the movie catalog.

Implemented:

- FastAPI application.
- Movie creation.
- Movie listing.
- Retrieval by movie ID.
- Replacement of a movie by ID.
- Deletion by ID.
- Search by release year.
- Sorting search results by title or director.
- Pydantic request validation.
- SQLAlchemy database integration.
- PostgreSQL persistence.

The service exposes:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/movies` | Create a movie |
| GET | `/movies` | List movies |
| GET | `/movies/{movie_id}` | Retrieve a movie |
| PUT | `/movies/{movie_id}` | Create or replace a movie at a specified ID |
| DELETE | `/movies/{movie_id}` | Delete a movie |
| GET | `/movies/find?year=2010` | Search movie IDs by year |

Interactive API documentation is available at `/docs`.


### 2. Banking Service

**Port:** 8002

Responsible for evaluating simulated card payment requests.

Implemented operations:

- `GET /health` — service health check
- `POST /charges` — process a simulated card charge

**Payment simulation rule:**

A charge succeeds when:

- The amount is greater than zero.
- The card number has an even number of characters.

Both conditions must be satisfied.

Example request:

    {
        "cardNumber": "12345678",
        "amount": 1500
    }

Example response:

    {
        "success": true
    }

**Technology:** FastAPI, Pydantic.

**Persistence:** None. The current implementation does not store payment transactions or card details.

**Important:** This is a simulation of the original Java implementation, not a real payment-processing integration.

### Infrastructure

Implemented:

- PostgreSQL 16 Docker container.
- Persistent Docker volume.
- Database health check.
- Local database connection through port 5433.



## Service Verification

| Service | Verification |
|---|---|
| Movies | API operations and PostgreSQL persistence verified |
| Banking | API operations and automated tests passed |
| Ticketing | Pending implementation and integration |

Run the Banking tests:

    python -m pytest services/banking/tests/ -v

Start Banking:

    uvicorn services.banking.app.main:app --reload --port 8002

## Local Development

### 1. Activate the Python environment

```bash
conda activate python-practice
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with the local database connection.

### 4. Start PostgreSQL

```bash
docker compose -f infrastructure/docker-compose.yml up -d
```

### 5. Start Movies

```bash
uvicorn services.movies.app.main:app --reload --port 8001
```

### 6. Access the API

- Health check: http://127.0.0.1:8001/health
- Swagger UI: http://127.0.0.1:8001/docs

## Development Approach

The system is being modernized incrementally.

The original Java implementation is used as a reference for business functionality and service contracts. The Python implementation improves persistence, validation, maintainability, and deployment.

Each service will be implemented and verified independently before integration.
