
from pydantic import BaseModel, ConfigDict, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    year: int = Field(ge=1888, le=2100)
    director: str = Field(min_length=1, max_length=150)
    actors: list[str] = Field(default_factory=list)


class MovieRead(MovieCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
