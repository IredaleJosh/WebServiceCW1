from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from model import Movie, Rating, User, Genre
from dependencies import check_admin
from schemas.analytics import SortRatings, DisplayMovies, DisplayUsers, FindGenre, DisplayMovieShort, DisplayReviewNumber, DisplayMovieAvg

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Public
# Highest/ Lowest Rated Movies either most ratings or average
@router.get("/filter/SortedMovies",
            status_code=200,
            response_model=list[DisplayMovies],
            description="Users can view highest or lowest rated movies, as well as most recent or latest movies",
            responses={
                500: {"description": "Server side error"}
            })
def sort_movies(sort: SortRatings, db: Session = Depends(get_db)):
    # Get all movies and average their ratings
    rate_movies = db.query(Movie, func.avg(Rating.rating).label("avg_rating")).join(
        Rating, Rating.movies_id == Movie.id).group_by(
        Movie.id)
    year_movies = db.query(Movie)
    # if highest
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
@router.get("/filter/average", 
            status_code=200,
            response_model=DisplayMovieAvg, 
            description="View an average rating for a specific movie",
            responses={
                404: {"description": "Movie not found"},
                404: {"description": "No ratings found"},
                500: {"description": "Server side error"}
            })
def average(movie_name: str, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.name == movie_name).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie called {movie_name} not found")
    ratings = db.query(Rating).filter(Rating.movies_id == movie.id).all()
    # ratings = db.query(Rating).filter(Movie.name == movie_name).all()
    if not ratings:
        raise HTTPException(status_code=404, detail=f"No ratings for movie {movie_name} found")
    average=0
    count=0
    for r in ratings:
        average += r.rating
        count+=1
    average /= count
    return {"id": movie.id, "name": movie.name, "summary": movie.summary, "runtime": movie.runtime, "average": average}


# Search For Movies Names and list them
@router.get("/search", 
            response_model=list[DisplayMovieShort],
            status_code=200,
            description="Search for movies based on their name, and displaying movies containing the search",
            responses={
                422: {"description": "Validation Error"},
                500: {"description": "Server side error"}
            })
def search_movies_by_name(query: str, db: Session = Depends(get_db)):
    results = db.query(Movie).filter(Movie.name.ilike(f"%{query}%")).all()
    if not results:
        return {"Message" : f"No Movies with {query}, try again"}
    return [{"id": m.id, "name": m.name, "summary": m.summary, "runtime": m.runtime} for m in results]

# Filter Movies by Genres
@router.get("/filter/genre",
            response_model=list[DisplayMovieShort],
            status_code=200,
            description="Filter by genres and display movies with queried genre",
            responses={
                404: {"description": "No Movies of the genre found"},
                500: {"description": "Server side error"}
            })
def search_genre(genreQuery: FindGenre, db: Session = Depends(get_db)):
    movies = db.query(Movie).join(Movie.genre).filter(Genre.name == genreQuery.value).all()
    if not movies:
        raise HTTPException(404, f"No Movies found for {genreQuery.value}, try again")
    return [{"id": m.id, "name": m.name, "summary": m.summary, "runtime": m.runtime} for m in movies]

# Admin
# Most active users via number of ratings they did
@router.get("/admin/filter/ActiveUsers",
            response_model=list[DisplayReviewNumber],
            status_code=200,
            description="Admin can view how many reviews all users have done",
            responses={
                401: {"description": "Not Authorised"},
                500: {"description": "Server side error"}
            })
def user_reviews(db: Session = Depends(get_db), check_admin : Session = Depends(check_admin)):
    users = db.query(User, func.count(Rating.id).label("Number_of_Reviews")).join(
        Rating, Rating.users_id == User.id).group_by(
        User.id).order_by(
        func.count(Rating.id).desc()).all()
    return [{"id":m.id, "username":m.username, "review_count": Number_of_Reviews} for m, Number_of_Reviews in users]

# Search a certain user and list all reviews
@router.get("/admin/filter/SearchUser",
            response_model=DisplayUsers,
            status_code=200,
            description="Admins can view certian users",
            responses={
                401: {"description": "Not Authorised"},
                404: {"description": "User not found"},
                500: {"description": "Server side error"}
            })
def search_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user