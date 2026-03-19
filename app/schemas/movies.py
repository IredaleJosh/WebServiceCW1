from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.ratings import RatingRead

# How Movies are Displayed
class MovieRead(BaseModel):
    id: int
    name: str
    summary: str
    release: datetime
    runtime: int
    budget: float
    revenue: float
    rate_entries_movie: list[RatingRead] = []

class MovieCreate(BaseModel):
    name: str
    summary: str
    release: datetime
    runtime: int
    budget: float
    revenue: float

class MovieUpdate(BaseModel):
    name: Optional[str] = None
    summary: Optional[str] = None
    release: Optional[datetime] = None
    runtime: Optional[int] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None