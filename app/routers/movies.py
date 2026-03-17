from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.movie import Movie, Rating, User
from app.dependencies import check_admin
from app.schemas.movies import MovieCreate, MovieUpdate, MovieRead

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

# Search For Movies Names and list them
@router.get("/search")
def search_movies_by_name(query: str, db: Session = Depends(get_db)):
    results = db.query(Movie).filter(Movie.name.ilike(f"%{query}%")).all()
    if not results:
        return {"Message" : f"No Movies with {query}, try again"}
    return results

# Return top rated movies

# Overview of the Movie - Shows Ratings
@router.get("/{movie_id}", response_model=MovieRead)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    return movie

# Average Rating for a Movie
@router.get("/{movie_id}/avg")
def average(movie_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.movies_id == movie_id).all()
    if not ratings:
        return {"Message : No Ratings Available"}
    average=0
    count=0
    for r in ratings:
        average += r.rating
        count+=1
    average /= count
    return {"Average Ratings" : average}

# UPDATE
@router.put("/{movie_id}")
def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
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
def delete_movie(movie_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not Found")
    db.delete(movie)
    db.commit()
    return {"Message : Deleted Movie"}
