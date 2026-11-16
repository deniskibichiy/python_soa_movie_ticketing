
from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Movie
from .schemas import MovieCreate, MovieRead

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movies Service",
    description="Movie catalogue service in the modernized SOA system",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "movies"}


@app.post(
    "/movies",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED
)
def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db)
):
    new_movie = Movie(**movie.model_dump())

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie


@app.get("/movies", response_model=list[MovieRead])
def list_movies(db: Session = Depends(get_db)):
    statement = select(Movie).order_by(Movie.id)

    return db.scalars(statement).all()


@app.get("/movies/find")
def find_movies(
    year: int = Query(..., ge=1888, le=2100),
    orderby: str | None = None,
    db: Session = Depends(get_db)
):
    statement = select(Movie).where(Movie.year == year)

    if orderby:
        ordering = {
            "title": Movie.title,
            "director": Movie.director
        }

        column = ordering.get(orderby.lower())

        if column is None:
            raise HTTPException(
                status_code=400,
                detail="orderby must be Title or Director"
            )

        statement = statement.order_by(column)

    movies = db.scalars(statement).all()

    # Preserve the original service's search response:
    # a list of matching movie IDs.
    return {"id": [movie.id for movie in movies]}


@app.get("/movies/{movie_id}", response_model=MovieRead)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    movie = db.get(Movie, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie


@app.put("/movies/{movie_id}", response_model=MovieRead)
def replace_movie(
    movie_id: int,
    movie_data: MovieCreate,
    db: Session = Depends(get_db)
):
    movie = db.get(Movie, movie_id)

    if movie is None:
        movie = Movie(
            id=movie_id,
            **movie_data.model_dump()
        )
        db.add(movie)
    else:
        for field, value in movie_data.model_dump().items():
            setattr(movie, field, value)

    db.commit()
    db.refresh(movie)

    return movie


@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    movie = db.get(Movie, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    db.delete(movie)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
