import httpx
from fastapi.testclient import TestClient

from services.ticketing.app.main import app
from services.ticketing.app.service import ticketing_service
from services.ticketing.app import service


client = TestClient(app)


def setup_function():
    ticketing_service.movie_tickets.clear()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "ticketing"


def test_get_movies(monkeypatch):
    def mock_get_movies(url, year):
        assert year == 2014
        return [
            {"id": 1, "title": "Interstellar"},
            {"id": 2, "title": "The Imitation Game"},
        ]

    monkeypatch.setattr(
        service.clients,
        "get_movies_by_year",
        mock_get_movies,
    )

    response = client.post(
        "/GetMovies",
        json={"year": 2014},
    )

    assert response.status_code == 200
    assert len(response.json()["movie"]) == 2
    assert response.json()["movie"][0]["title"] == "Interstellar"


def test_successful_ticket_purchase(monkeypatch):
    monkeypatch.setattr(
        service.clients,
        "get_movie",
        lambda url, movie_id: {"id": movie_id},
    )

    def mock_charge_card(url, card_number, amount):
        assert card_number == "12345678"
        assert amount == 30
        return True

    monkeypatch.setattr(
        service.clients,
        "charge_card",
        mock_charge_card,
    )

    response = client.post(
        "/BuyTickets",
        json={
            "movieId": 1,
            "count": 3,
            "cardNumber": "12345678",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert ticketing_service.movie_tickets[1] == 3


def test_failed_payment_does_not_update_tickets(monkeypatch):
    monkeypatch.setattr(
        service.clients,
        "get_movie",
        lambda url, movie_id: {"id": movie_id},
    )

    monkeypatch.setattr(
        service.clients,
        "charge_card",
        lambda url, card_number, amount: False,
    )

    response = client.post(
        "/BuyTickets",
        json={
            "movieId": 1,
            "count": 2,
            "cardNumber": "1234567",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": False}
    assert 1 not in ticketing_service.movie_tickets


def test_unknown_movie_is_not_charged(monkeypatch):
    def mock_get_movie(url, movie_id):
        request = httpx.Request("GET", f"{url}/movies/{movie_id}")
        response = httpx.Response(404, request=request)

        raise httpx.HTTPStatusError(
            "Movie not found",
            request=request,
            response=response,
        )

    def unexpected_charge(*args):
        raise AssertionError("Banking must not be called")

    monkeypatch.setattr(
        service.clients,
        "get_movie",
        mock_get_movie,
    )

    monkeypatch.setattr(
        service.clients,
        "charge_card",
        unexpected_charge,
    )

    response = client.post(
        "/BuyTickets",
        json={
            "movieId": 999,
            "count": 2,
            "cardNumber": "12345678",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": False}


def test_get_tickets(monkeypatch):
    monkeypatch.setattr(
        service.clients,
        "get_movie",
        lambda url, movie_id: {"id": movie_id},
    )

    monkeypatch.setattr(
        service.clients,
        "charge_card",
        lambda url, card_number, amount: True,
    )

    client.post(
        "/BuyTickets",
        json={
            "movieId": 1,
            "count": 3,
            "cardNumber": "12345678",
        },
    )

    client.post(
        "/BuyTickets",
        json={
            "movieId": 2,
            "count": 2,
            "cardNumber": "12345678",
        },
    )

    response = client.post("/GetTickets")

    assert response.status_code == 200
    assert len(response.json()["ticket"]) == 2