from pydantic import BaseModel, Field
from typing import Optional

# How the ratings are displayed
class RatingRead(BaseModel):
    id: int
    rating: int
    review: str

class RatingBase(BaseModel):
    rating: int = Field(..., ge=0, le=5)
    review: str | None = None

# creates a rating for the movie of movie_id
class RatingCreate(RatingBase):
    pass

# change the rating to either nothing or keep the same
class RatingUpdate(RatingBase):
    rating: int | None = Field(..., ge=0, le=5)
    review: str | None = None

# For Deleting the reviews, we delete the row and the user and movie id linked to it
class RatingDelete(RatingBase):
    pass