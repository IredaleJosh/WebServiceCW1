from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.movie import Movie, Rating, User
from app.dependencies import check_admin
from app.schemas.analytics import SortRatings, DisplayMovies

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Public
# Highest/ Lowest Rated Movies either most ratings or average
@router.get("/SortedMovies", response_model=list[DisplayMovies])
def sort_movies(sort: SortRatings, db: Session = Depends(get_db)):
    # Get all movies and average their ratings
    rate_movies = db.query(Movie, func.avg(Rating.rating).label("avg_rating")).join(Rating, Rating.movies_id == Movie.id).group_by(Movie.id)
    year_movies = db.query(Movie)
    if sort.value == "Highest":
        rate_movies = rate_movies.order_by(func.avg(Rating.rating).desc()).all()
        rate_movies = [{"id":m.id, "name":m.name, "rating": float(avg_rating)} for m, avg_rating in rate_movies]
        return rate_movies
    # if lowest
    if sort.value == "Lowest":
        rate_movies = rate_movies.order_by(func.avg(Rating.rating).asc()).all()
        rate_movies = [{"id":m.id, "name":m.name, "rating": float(avg_rating)} for m, avg_rating in rate_movies]
        return rate_movies
    # by release date recent
    if sort.value == "Recent Years":
        year_movies = year_movies.order_by(Movie.release.desc()).all()
        year_movies = [{"id": m.id, "name": m.name, "release": m.release} for m in year_movies]
        return year_movies
    # by release date latest
    if sort.value == "Latest Years":
        year_movies = year_movies.order_by(Movie.release.asc()).all()
        year_movies = [{"id": m.id, "name": m.name, "release": m.release} for m in year_movies]
        return year_movies

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

# Search For Movies Names and list them
@router.get("/search")
def search_movies_by_name(query: str, db: Session = Depends(get_db)):
    results = db.query(Movie).filter(Movie.name.ilike(f"%{query}%")).all()
    if not results:
        return {"Message" : f"No Movies with {query}, try again"}
    return results

# Sort by Genres
@router.get("/filter/genre")
def search_genre(genre: str, db: Session = Depends(get_db)):
    genres = db.query(Movie).filter(Movie.name.ilike(f"%{genre}%")).all()
    return genres

# Actors in most movies

# Actors in highest rated movies

# Directors with highest rated movies

# Total number of users

# Genre popularity 

# Admin

# Most active users via ratings they did

# Search a certain user and list all reviews

