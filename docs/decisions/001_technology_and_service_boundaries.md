
# ADR 0001: Technology Selection and Service Boundaries

- Status: Accepted
- Date: 2026-11-16

## Decisions

### Programming Language and Framework

Use Python and FastAPI for the service implementations.

### API Communication

Use HTTP APIs with JSON payloads.

### Persistence

Use PostgreSQL for persistent service data.

Each service will own its database and expose its data through APIs.

### ORM and Validation

Use SQLAlchemy 2.x for database interaction and Pydantic for
request and response validation.

### Local Infrastructure

Use Docker Compose to manage PostgreSQL during local development.

## Consequences

Benefits:
- Independent service development and deployment.
- Persistent data.
- Standard HTTP interfaces.
- Interactive API documentation.
- Easier local environment setup.

Trade-offs:
- Services must handle network failures.
- Distributed workflows require explicit consistency handling.
- Each service needs its own database configuration and migrations.