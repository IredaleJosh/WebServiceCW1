from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.movie import Movie
from app.schemas.movies import MovieCreate, MovieUpdate

router = APIRouter(prefix="/movies", tags=["Movies"])

# CRUD
# CREATE
@router.post("/")
def create_movie(movie: MovieCreate, db : Session = Depends(get_db)):
    new_movie = Movie(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

# READ 
@router.get("/{movie_id}")
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    return movie

# UPDATE
@router.put("/{movie_id}")
def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    
    for key, value in movie_update.dict(exclude_unset=True).items():
        setattr(movie, key, value)
    
    db.commit()
    db.refresh(movie)
    return movie

# DELETE
@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    db.delete(movie)
    db.commit()
    return {"Message : Deleted Movie"}