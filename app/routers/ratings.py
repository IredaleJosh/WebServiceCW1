from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_curr_user
from app.movie import Rating, User
from app.schemas.ratings import RatingCreate, RatingUpdate, RatingDelete

router = APIRouter(prefix="/ratings", tags=["Ratings"])


# CRUD
# CREATE

# This uses the movies endpoint
# It gets the current user
# Creates a new review at the movie endpoint + the current user making the review
@router.post("/{movie_id}/ratings")
def create_rating(movie_id : int, rating: RatingCreate, 
    db : Session = Depends(get_db), curr_user : User = Depends(get_curr_user)):
    new_rating = Rating(**rating.dict(),
        users_id=curr_user.id,
        movies_id=movie_id)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

# READ 
@router.get("/{rating_id}", response_model=RatingDelete)
def read_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not Found")
    return rating

# UPDATE
@router.put("/{rating_id}", response_model=RatingDelete)
def update_rating(rating_id: int, rating_update: RatingUpdate, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not Found")
    for key, value in rating_update.dict(exclude_unset=True).items():
        setattr(rating, key, value)
    db.commit()
    db.refresh(rating)
    return rating

# DELETE
@router.delete("/{rating_id}")
def delete_movie(rating_id: int, db: Session = Depends(get_db)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not Found")
    db.delete(rating)
    db.commit()
    return {"Message : Deleted Rating"}