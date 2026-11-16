import httpx


def get_movies_by_year(
    movies_url: str,
    year: int,
) -> list[dict]:

    response = httpx.get(
        f"{movies_url}/movies/find",
        params={
            "year": year,
            "orderby": "Title",
        },
        timeout=5.0,
    )
    response.raise_for_status()

    movie_ids = response.json().get("id", [])

    movies = []

    for movie_id in movie_ids:
        movie_response = httpx.get(
            f"{movies_url}/movies/{movie_id}",
            timeout=5.0,
        )
        movie_response.raise_for_status()

        movie = movie_response.json()

        movies.append({
            "id": movie_id,
            "title": movie["title"],
        })

    return movies


def get_movie(
    movies_url: str,
    movie_id: int,
) -> dict:

    response = httpx.get(
        f"{movies_url}/movies/{movie_id}",
        timeout=5.0,
    )
    response.raise_for_status()

    return response.json()


def charge_card(
    banking_url: str,
    card_number: str,
    amount: int,
) -> bool:

    response = httpx.post(
        f"{banking_url}/charges",
        json={
            "cardNumber": card_number,
            "amount": amount,
        },
        timeout=5.0,
    )
    response.raise_for_status()

    return response.json()["success"]