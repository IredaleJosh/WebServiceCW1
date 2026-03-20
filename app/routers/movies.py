from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Movie, User, Genre
from app.dependencies import check_admin
from app.schemas.movies import MovieCreate, MovieUpdate, MovieRead, MovieDelete

router = APIRouter(prefix="/movies", tags=["Movies"])

# CRUD
# CREATE - ADMIN ONLY Create a new movie
@router.post("/create", 
            response_model=MovieRead,
            status_code=200, 
            description="Admins create a new movie",
            responses={
                401: {"description":"Not Authorised"},
                400: {"description":"Genres aren't Valid"},
                422: {"description":"Validation Error"}
            })
def create_movie(movie: MovieCreate, db : Session = Depends(get_db), check_admin : Session = Depends(check_admin)):
    # Check if genres available
    genres = db.query(Genre).filter(Genre.name.in_(movie.genres)).all()
    if not genres:
        raise HTTPException(400, "Genres aren't Valid")
    # make movie
    new_movie = Movie(
        name=movie.name, summary=movie.summary, release=movie.release, runtime=movie.runtime,
        director=movie.director, revenue=movie.revenue
    )
    # using names, as easier for testing and UI
    new_movie.genre = genres
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

# Overview of the Movie inc. ratings and genres
@router.get("/{movie_id}/overview", 
            response_model=MovieRead,
            status_code=200, 
            description="Overview of the Movie including their ratings and genres",
            responses={
                 404: {"description":"Movie not Found"},
                 422: {"description":"Validation Error"}
            })
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    return movie

# UPDATE - Change details of the movie ADMIN ONLY
@router.put("/{movie_id}/update", 
            response_model=MovieUpdate,
            status_code=200,
            description="Admins can change the details of a movie",
            responses={
                401: {"description":"Not Authorised"},
                404: {"description":"Movie not Found"},
                422: {"description":"Validation Error"}
            })
def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_db), check_admin : Session = Depends(check_admin)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    for key, value in movie_update.dict(exclude_unset=True).items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie

# DELETE - Delete a movie ADMIN ONLY
@router.delete("/{movie_id}/delete", 
            response_model=MovieDelete,
            status_code=200, 
            description="Admins can delete a movie and their ratings, but not their genres",
            responses={
                401: {"description":"Not Authorised"},
                404: {"description":"Movie not Found"},
                422: {"description":"Validation Error"}
            })               
def delete_movie(movie_id: int, db: Session = Depends(get_db), check_admin : Session = Depends(check_admin)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    temp_movie = movie
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    db.delete(movie)
    db.commit()
    return {"id":temp_movie.id, "name":temp_movie.name, "summary":temp_movie.summary, "release":temp_movie.release, 
            "runtime":temp_movie.runtime, "director":temp_movie.director,"revenue":temp_movie.revenue, "genre":temp_movie.genre, 
            "message": "Deleted Movie"}