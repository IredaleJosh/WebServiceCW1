from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.schemas.ratings import RatingRead

# Genres
class GenreDisplay(BaseModel):
    name: str

# Create a Movie
class MovieCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    summary: str
    release: int
    runtime: int
    director: str
    revenue: int
    genres: list[str]

    # Validates its not a future date
    @field_validator("release")
    def current(cls, time):
        if time > datetime.now().year:
            raise ValueError("Cannot be a future date")
        return time

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Movie name",
                "summary": "350 character descriptor",
                "name": "Year of release",
                "runtime": "runtime in minutes",
                "director": "first and last name of director",
                "revenue": "total revenue to the pound",
                "genres": "list of genres (must be a valid genre)",
            }
        }
    }
    
# How Movies are Displayed
class MovieRead(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=30)
    summary: str
    release: int
    runtime: int
    director: str
    revenue: int
    genre: list[GenreDisplay] = []
    rate_entries_movie: list[RatingRead] = []

# Update Movies
class MovieUpdate(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None
    release: Optional[int] = None
    runtime: Optional[int] = None
    director: Optional[str] = None
    revenue: Optional[float] = None
    genres: list[str]

class MovieDelete(MovieRead):
    message: str
    rate_entries_movie: Optional[list[RatingRead]] = None