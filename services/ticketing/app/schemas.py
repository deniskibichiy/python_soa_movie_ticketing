from pydantic import BaseModel, ConfigDict, Field


class GetMoviesRequest(BaseModel):
    year: int


class MovieSummary(BaseModel):
    id: int
    title: str


class GetMoviesResponse(BaseModel):
    movie: list[MovieSummary] = Field(default_factory=list)


class BuyTicketsRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    movie_id: int = Field(alias="movieId")
    count: int
    card_number: str = Field(alias="cardNumber")


class BuyTicketsResponse(BaseModel):
    success: bool


class Ticket(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    movie_id: int = Field(alias="movieId")
    count: int


class GetTicketsResponse(BaseModel):
    ticket: list[Ticket] = Field(default_factory=list)