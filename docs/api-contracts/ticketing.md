# Ticketing API Contract

Base URL: `http://localhost:8003`

## Health Check

GET `/health`

## Get Movies

POST `/GetMovies`

Request:

    {
      "year": 2014
    }

Response:

    {
      "movie": [
        {
          "id": 2,
          "title": "Interstellar"
        }
      ]
    }

## Buy Tickets

POST `/BuyTickets`

Request:

    {
      "movieId": 2,
      "count": 3,
      "cardNumber": "12345678"
    }

Response:

    {
      "success": true
    }

The payment amount is calculated as:

    amount = count * 10

A failed payment or unknown movie returns `success: false`.

## Get Tickets

POST `/GetTickets`

Response:

    {
      "ticket": [
        {
          "movieId": 2,
          "count": 3
        }
      ]
    }