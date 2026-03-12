from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.movie import Movie

router = APIRouter(prefix="/movies", tags=["Movies"])

# ROUTERS FOR ....

@router.get("/")
def get_movies(db : Session = Depends(get_db)):
    return db.query(Movie).all()

@router.get("/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    return movie