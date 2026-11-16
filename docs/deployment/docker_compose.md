# Docker Compose Deployment

## Overview

The application is composed of four containers:

| Container | Responsibility | Host port |
|---|---|---:|
| movies-db | PostgreSQL database for Movies | 5433 |
| movies | Movie catalogue API | 8001 |
| banking | Simulated card-payment API | 8002 |
| ticketing | Ticket booking and service orchestration API | 8003 |

The services are orchestrated using Docker Compose through:

`infrastructure/docker-compose.yml`

## Container communication

Docker Compose creates an internal network for the services. Containers communicate using their Compose service names rather than `localhost`.

| Source | Destination |
|---|---|
| Movies | `movies-db:5432` |
| Ticketing | `http://movies:8001` |
| Ticketing | `http://banking:8002` |

Host applications can access the APIs through `localhost` and their published ports.

## Database configuration

PostgreSQL uses the `postgres:16-alpine` image.

The database is configured with:

- Database: `movies_db`
- User: `soa_user`
- Internal port: `5432`
- Published host port: `5433`

The named Docker volume `movies_postgres_data` stores PostgreSQL data independently of the database container lifecycle.

The Movies service connects using the internal database hostname when running in Docker.

## Health checks and startup

The database uses `pg_isready` to report its readiness.

The Movies, Banking, and Ticketing services expose `/health` endpoints. Docker Compose uses these endpoints to monitor service health.

The services are configured with restart policies and startup dependencies in the Compose configuration.

## Running the application

Start all containers:

```bash
sudo docker compose -f infrastructure/docker-compose.yml up -d --build
```
Inspect container status:
```bash
sudo docker compose -f infrastructure/docker-compose.yml ps
```
View logs:
```bash
sudo docker compose -f infrastructure/docker-compose.yml logs -f
```
Stop the application:

```bash
sudo docker compose -f infrastructure/docker-compose.yml down
```

## Verification
The following checks were completed:
1. PostgreSQL container reported healthy.
2. Movies API reported healthy on port 8001.
3. Banking API reported healthy on port 8002.
4. Ticketing API reported healthy on port 8003.
5. A movie was created through the Movies API.
6. Ticketing retrieved movies for the requested year through the Movies service.
7. Ticketing successfully processed a ticket purchase through the Banking service.
8. The ticket count endpoint returned the updated count.