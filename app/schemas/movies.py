from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.ratings import RatingRead

# Genres
class GenreDisplay(BaseModel):
    name: str

# Create a Movie
class MovieCreate(BaseModel):
    name: str
    summary: str
    release: datetime
    runtime: int
    budget: float
    revenue: float
    genres: list[str]

# How Movies are Displayed
class MovieRead(BaseModel):
    id: int
    name: str
    summary: str
    release: datetime
    runtime: int
    budget: float
    revenue: float
    genre: list[GenreDisplay] = []
    rate_entries_movie: list[RatingRead] = []

# Update Movies
class MovieUpdate(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None
    release: Optional[datetime] = None
    runtime: Optional[int] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    genres: list[str]
