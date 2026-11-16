from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    director: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    actors: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list
    )