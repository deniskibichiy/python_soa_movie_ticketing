import httpx

from fastapi import FastAPI, HTTPException

from services.ticketing.app.schemas import (
    BuyTicketsRequest,
    BuyTicketsResponse,
    GetMoviesRequest,
    GetMoviesResponse,
    GetTicketsResponse,
)
from services.ticketing.app.service import ticketing_service


app = FastAPI(
    title="Ticketing Service",
    description="Coordinates movie ticket purchases",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ticketing",
    }


@app.post(
    "/GetMovies",
    response_model=GetMoviesResponse,
)
def get_movies(request: GetMoviesRequest):
    try:
        return ticketing_service.get_movies(request.year)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve movies from Movies service",
        ) from exc


@app.post(
    "/BuyTickets",
    response_model=BuyTicketsResponse,
)
def buy_tickets(request: BuyTicketsRequest):
    try:
        return ticketing_service.buy_tickets(request)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to complete payment through Banking service",
        ) from exc


@app.post(
    "/GetTickets",
    response_model=GetTicketsResponse,
)
def get_tickets():
    return ticketing_service.get_tickets()