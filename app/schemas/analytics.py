from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum
from app.schemas.ratings import RatingRead

# displays the options to filter movies
class SortRatings(str, Enum):
    highest = "Highest"
    lowest = "Lowest"
    recent = "Recent Years"
    latest = "Latest Years"

# Shows either the release data or average rating
class DisplayMovies(BaseModel):
    id: int
    name: str
    rating: Optional[float] | None = None
    release: Optional[date] | None = None

# options to filter by genres - hardcode as genres are fixed
class FindGenre(str, Enum):
    Action = "Action"
    Horror = "Horror"
    Comedy = "Comedy"
    SciFi = "Sci-Fi"

# Show users name, summary, length, reviews
class DisplayMovieGenre(BaseModel):
    id: int
    name: str
    summary: str
    runtime: int

class DisplayUsers(BaseModel):
    rate_entries_user: list[RatingRead] = []