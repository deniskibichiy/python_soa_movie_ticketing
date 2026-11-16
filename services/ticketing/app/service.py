import os
from threading import Lock

import httpx

from services.ticketing.app import clients
from services.ticketing.app.schemas import (
    BuyTicketsRequest,
    BuyTicketsResponse,
    GetMoviesResponse,
    GetTicketsResponse,
    MovieSummary,
    Ticket,
)


class TicketingService:
    def __init__(self):
        self.movies_url = os.getenv(
            "MOVIES_SERVICE_URL",
            "http://localhost:8001",
        )

        self.banking_url = os.getenv(
            "BANKING_SERVICE_URL",
            "http://localhost:8002",
        )

        self.movie_tickets: dict[int, int] = {}
        self.lock = Lock()

    def get_movies(self, year: int) -> GetMoviesResponse:
        movies = clients.get_movies_by_year(
            self.movies_url,
            year,
        )

        return GetMoviesResponse(
            movie=[
                MovieSummary(**movie)
                for movie in movies
            ]
        )

    def buy_tickets(
        self,
        request: BuyTicketsRequest,
    ) -> BuyTicketsResponse:

        # Verify that the requested movie exists.
        try:
            clients.get_movie(
                self.movies_url,
                request.movie_id,
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return BuyTicketsResponse(success=False)
            raise

        # Original Java rule: amount = count * 10.
        amount = request.count * 10

        success = clients.charge_card(
            self.banking_url,
            request.card_number,
            amount,
        )

        if success:
            with self.lock:
                current_count = self.movie_tickets.get(
                    request.movie_id,
                    0,
                )

                self.movie_tickets[request.movie_id] = (
                    current_count + request.count
                )

        return BuyTicketsResponse(success=success)

    def get_tickets(self) -> GetTicketsResponse:
        with self.lock:
            tickets = [
                Ticket(movieId=movie_id, count=count)
                for movie_id, count in self.movie_tickets.items()
            ]

        return GetTicketsResponse(ticket=tickets)


ticketing_service = TicketingService()