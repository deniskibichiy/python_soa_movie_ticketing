from fastapi.testclient import TestClient

from services.banking.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_successful_charge():
    response = client.post(
        "/charges",
        json={
            "cardNumber": "12345678",
            "amount": 1500,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}


def test_charge_with_odd_card_number_length():
    response = client.post(
        "/charges",
        json={
            "cardNumber": "1234567",
            "amount": 1500,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": False}


def test_charge_with_zero_amount():
    response = client.post(
        "/charges",
        json={
            "cardNumber": "12345678",
            "amount": 0,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": False}


def test_charge_with_negative_amount():
    response = client.post(
        "/charges",
        json={
            "cardNumber": "12345678",
            "amount": -100,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": False}


def test_missing_card_number():
    response = client.post(
        "/charges",
        json={"amount": 1500},
    )

    assert response.status_code == 422