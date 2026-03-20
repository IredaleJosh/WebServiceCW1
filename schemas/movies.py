from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from schemas.ratings import RatingRead

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