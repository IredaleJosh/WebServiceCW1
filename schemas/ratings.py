from pydantic import BaseModel, Field

# How the ratings are displayed
class RatingRead(BaseModel):
    id: int
    rating: int
    review: str

# How a new rating is displayed to user
class RatingDisplay(BaseModel):
    id: int
    users_id: int
    movies_id: int
    name: str
    rating: int = Field(..., ge=0, le=5)
    review: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "rating id",
                "users_id": "id of users making rating",
                "movies_id": "id of movie being reviewd",
                "rating": "rating between 1 and 5",
                "review": "100 character review"
            }
        }
    }

class RatingBase(BaseModel):
    rating: int = Field(..., ge=0, le=5)
    review: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "rating": "rating between 1 and 5",
                "review": "100 character review"
            }
        }
    }

# creates a rating for the movie of movie_id
class RatingCreate(RatingBase):
    pass

# change the rating to either nothing or keep the same
class RatingUpdate(RatingBase):
    rating: int | None = Field(..., ge=0, le=5)
    review: str | None = None

# For Deleting the reviews, we delete the row and the user and movie id linked to it
class RatingDelete(RatingDisplay):
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "rating id",
                "users_id": "id of users making rating",
                "movies_id": "id of movie being reviewd",
                "rating": "rating between 1 and 5",
                "review": "100 character review",
                "message": "Deleted Review"
            }
        }
    }