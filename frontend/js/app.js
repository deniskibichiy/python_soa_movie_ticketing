const API_URL = "http://localhost:8003";

const movieSearchForm = document.querySelector("#movie-search-form");
const movieResults = document.querySelector("#movie-results");

const purchaseForm = document.querySelector("#purchase-form");
const purchaseResult = document.querySelector("#purchase-result");

const loadTicketsButton = document.querySelector("#load-tickets-button");
const ticketResults = document.querySelector("#ticket-results");

const appMessage = document.querySelector("#app-message");

let availableMovies = [];


async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_URL}${endpoint}`, options);

    if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
    }

    return response.json();
}


function displayMessage(element, message) {
    element.textContent = message;
}


function renderMovies(movies) {
    movieResults.replaceChildren();

    if (movies.length === 0) {
        movieResults.textContent = "No movies found for this year.";
        return;
    }

    movies.forEach(movie => {
        const card = document.createElement("article");
        card.className = "movie-card";

        const title = document.createElement("h3");
        title.textContent = movie.title;

        const id = document.createElement("p");
        id.textContent = `Movie ID: ${movie.id}`;

        const button = document.createElement("button");
        button.type = "button";
        button.textContent = "Select Movie";

        button.addEventListener("click", () => {
            document.querySelector("#movie-id").value = movie.id;
        });

        card.append(title, id, button);
        movieResults.appendChild(card);
    });
}


movieSearchForm.addEventListener("submit", async event => {
    event.preventDefault();

    const year = document.querySelector("#year").value;

    try {
        displayMessage(appMessage, "Searching movies...");

        const data = await apiRequest("/GetMovies", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                year: Number(year)
            })
        });

        availableMovies = data.movie;
        renderMovies(availableMovies);

        displayMessage(appMessage, `${availableMovies.length} movie(s) found.`);
    } catch (error) {
        displayMessage(appMessage, `Movie search failed: ${error.message}`);
    }
});


purchaseForm.addEventListener("submit", async event => {
    event.preventDefault();

    const movieId = Number(document.querySelector("#movie-id").value);
    const count = Number(document.querySelector("#ticket-count").value);
    const cardNumber = document.querySelector("#card-number").value.trim();

    if (!Number.isInteger(movieId) || movieId <= 0 ||
        !Number.isInteger(count) || count <= 0) {
        displayMessage(purchaseResult, "Enter a valid movie ID and ticket count.");
        return;
    }

    try {
        displayMessage(purchaseResult, "Processing purchase...");

        const data = await apiRequest("/BuyTickets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                movieId,
                count,
                cardNumber
            })
        });

        if (data.success) {
            displayMessage(purchaseResult, "Purchase successful.");
        } else {
            displayMessage(purchaseResult, "Payment declined or movie unavailable.");
        }
    } catch (error) {
        displayMessage(purchaseResult, `Purchase failed: ${error.message}`);
    }
});


loadTicketsButton.addEventListener("click", async () => {
    try {
        const data = await apiRequest("/GetTickets", {
            method: "POST"
        });

        ticketResults.replaceChildren();

        if (data.ticket.length === 0) {
            ticketResults.textContent = "No tickets have been purchased.";
            return;
        }

        const table = document.createElement("table");
        const header = document.createElement("tr");

        ["Movie ID", "Ticket Count"].forEach(label => {
            const th = document.createElement("th");
            th.textContent = label;
            header.appendChild(th);
        });

        table.appendChild(header);

        data.ticket.forEach(ticket => {
            const row = document.createElement("tr");

            const movieCell = document.createElement("td");
            movieCell.textContent = ticket.movieId;

            const countCell = document.createElement("td");
            countCell.textContent = ticket.count;

            row.append(movieCell, countCell);
            table.appendChild(row);
        });

        ticketResults.appendChild(table);
    } catch (error) {
        ticketResults.textContent = `Could not load tickets: ${error.message}`;
    }
});