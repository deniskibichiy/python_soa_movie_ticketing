from fastapi import FastAPI

from services.banking.app.schemas import (
    ChargeCardRequest,
    ChargeCardResponse,
)
from services.banking.app.service import charge_card


app = FastAPI(
    title="Banking Service",
    description="Simulated card payment service",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "banking",
    }


@app.post(
    "/charges",
    response_model=ChargeCardResponse,
)
def process_card_charge(
    request: ChargeCardRequest,
):
    return charge_card(request)