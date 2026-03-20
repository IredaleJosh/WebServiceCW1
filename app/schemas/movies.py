from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from app.schemas.ratings import RatingRead

# Genres
class GenreDisplay(BaseModel):
    name: str

# Create a Movie
class MovieCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=30)
    summary: str = Field()
    release: date
    runtime: int
    budget: float
    revenue: float
    genres: list[str]

    # Validates its not a future date
    @field_validator("release")
    def current(cls, time):
        if time > date.today():
            raise ValueError("Cannot be a future date")
        return time
    
    # Validates its a unique movie name
    

# How Movies are Displayed
class MovieRead(BaseModel):
    id: int
    name: str
    summary: str
    release: date
    runtime: int
    budget: float
    revenue: float
    genre: list[GenreDisplay] = []
    rate_entries_movie: list[RatingRead] = []

# Update Movies
class MovieUpdate(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None
    release: Optional[date] = None
    runtime: Optional[int] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    genres: list[str]
