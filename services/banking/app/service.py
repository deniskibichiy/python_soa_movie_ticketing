from services.banking.app.schemas import (
    ChargeCardRequest,
    ChargeCardResponse,
)


def charge_card(
    request: ChargeCardRequest,
) -> ChargeCardResponse:

    success = (
        request.amount > 0
        and len(request.card_number) % 2 == 0
    )

    return ChargeCardResponse(success=success)