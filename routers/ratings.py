from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_curr_user
from model import Rating, User, Movie
from schemas.ratings import RatingDisplay, RatingCreate, RatingUpdate, RatingDelete

router = APIRouter(prefix="/ratings", tags=["Ratings"])

# CREATE - Current user creates a review and stores it to their account for said movie
@router.post("/{movie_id}", 
            response_model=RatingDisplay,
            status_code=200,
            description="Current user creates a review and stores it to their account for said movie",
            responses={
                401: {"description":"Not Authorised"},
                404: {"description":"Already Reviewed Movie"},
                422: {"description":"Validation Error"}
            })
def create_rating(movie_id : int, rating: RatingCreate, 
    db : Session = Depends(get_db), curr_user : User = Depends(get_curr_user)):
    check_review = db.query(Rating).filter(Rating.users_id == curr_user.id, Rating.movies_id == movie_id).first()
    if check_review:
        raise HTTPException(status_code=400, detail=f"Already Reviewed Movie")
    new_rating = Rating(**rating.dict(),
        users_id=curr_user.id,
        movies_id=movie_id)
    movie_name = db.query(Movie).filter(Movie.id == movie_id).first()
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return {"id":new_rating.id, "users_id":new_rating.users_id, "movies_id":new_rating.movies_id, "name": movie_name.name,
            "rating":new_rating.rating, "review":new_rating.review}

# READ - Search for certain reviews via its id and the user who made it
@router.get("/{rating_id}",
            response_model=RatingDisplay,
            status_code=200,
            description="Search for certain reviews via its id and the user who made it",
            responses={
                 404: {"description":"Rating not Found"},
                 422: {"description":"Validation Error"}
            })
def read_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not Found")
    movie_name = db.query(Movie).filter(Movie.id == rating.movies_id).first()
    return {"id":rating.id, "users_id":rating.users_id, "movies_id":rating.movies_id, "name": movie_name.name,
            "rating":rating.rating, "review":rating.review}

# UPDATE - User can update their reviews at certain id
@router.put("/{rating_id}",
            response_model=RatingDisplay,
            status_code=200,
            description="User can update their reviews for certain movies",
            responses={
                401: {"description":"Not Authorised"},
                404: {"description":"Rating not Found"},
                422: {"description":"Validation Error"}
            })
def update_rating(rating_id: int, rating_update: RatingUpdate, db: Session = Depends(get_db), 
                    curr_user : User = Depends(get_curr_user)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not Found")
    movie_name = db.query(Movie).filter(Movie.id == rating.movies_id).first()
    for key, value in rating_update.dict(exclude_unset=True).items():
        setattr(rating, key, value)
    db.commit()
    db.refresh(rating)
    return {"id":rating.id, "users_id":rating.users_id, "movies_id":rating.movies_id, "name": movie_name.name,
            "rating":rating.rating, "review":rating.review}

# DELETE - Users can remove their reviews
@router.delete("/{rating_id}",
            response_model=RatingDelete,
            status_code=200,
            description="Users can remove their reviews",
            responses={
                401: {"description":"Not Authorised"},
                404: {"description":"Rating not Found"},
                422: {"description":"Validation Error"}
            })
def delete_rating(rating_id: int, db: Session = Depends(get_db),
                    curr_user : User = Depends(get_curr_user)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    temp_rating=rating
    movie_name = db.query(Movie).filter(Movie.id == rating.movies_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not Found")
    db.delete(rating)
    db.commit()
    return {"id":temp_rating.id, "users_id":temp_rating.users_id, "movies_id":temp_rating.movies_id, "name": movie_name.name,
            "rating":temp_rating.rating, "review":temp_rating.review, "message": "Deleted Rating"}