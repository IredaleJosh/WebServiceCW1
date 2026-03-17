from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class SortRatings(str, Enum):
    highest = "Highest"
    lowest = "Lowest"
    recent = "Recent Years"
    latest = "Latest Years"

class DisplayMovies(BaseModel):
    id: int
    name: str
    rating: Optional[float] | None = None
    release: Optional[datetime] | None = None