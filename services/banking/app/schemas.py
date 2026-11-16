from pydantic import BaseModel, ConfigDict, Field


class ChargeCardRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    card_number: str = Field(alias="cardNumber")
    amount: int


class ChargeCardResponse(BaseModel):
    success: bool