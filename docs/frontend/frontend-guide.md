# Frontend Guide

## 1. Overview

The project includes a basic browser-based interface built using:

- HTML5 for page structure.
- CSS3 for styling and responsive layout.
- Vanilla JavaScript for application logic and API communication.

No frontend framework is used.

The frontend communicates with the Ticketing service. It does not communicate directly with the Movies service, Banking service, or PostgreSQL database.

## 2. Directory Structure

```text
frontend/
├── index.html
├── css/
│   └── styles.css
└── js/
    └── app.js
```
## 3. Application Features
### Movie Search
Users can search for movies by release year.

The frontend sends a POST request to:
```bash
/GetMovies
```
Example request:
```JSON
{
  "year": 2026
}
```

The Ticketing service retrieves matching movies from the Movies service and returns their IDs and titles.
### Ticket Purchase
Users select a movie, enter the number of tickets, and provide a demonstration card number.

The frontend sends a POST request to:
```bash
/BuyTickets
```
Example request:

```JSON
{
  "movieId": 3,
  "count": 2,
  "cardNumber": "123456"
}
```


Ticketing calculates the amount, requests payment authorization from Banking, and updates the ticket count when payment succeeds.

The payment mechanism is simulated. The frontend must not be used with real payment card details.
### Ticket Records
Users can retrieve ticket counts through:

```bash
/GetTickets
```

The frontend displays the returned movie IDs and ticket counts.

## 4. API Configuration
The frontend currently uses:
```bash
http://localhost:8003
```
This is the host-accessible address of the Ticketing service.

The frontend only needs to know the Ticketing API address because Ticketing handles communication with the other backend services.

## 5. CORS Configuration
The frontend and Ticketing API run on different origins:
- Frontend: `http://localhost:5500`
- Ticketing:`http://localhost:8003`
The Ticketing service uses FastAPI's CORSMiddleware to allow requests from the frontend development origins:
- `http://localhost:5500`
- `http://127.0.0.1:5500`
This permits browser requests, including JSON POST requests and their preflight OPTIONS requests.
## 6. Running the Frontend
Start the backend services:
```bash
sudo docker compose -f infrastructure/docker-compose.
yml up -d
```

Start the frontend development server from the project root:
```bash
python -m http.server 5500 --directory frontend
```

Open:
```bash
http://localhost:5500
``` 
The backend APIs must be running for the frontend operations to work.