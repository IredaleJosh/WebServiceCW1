from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum
from schemas.ratings import RatingRead

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
    release: Optional[int] | None = None

# options to filter by genres - hardcode as genres are fixed
class FindGenre(str, Enum):
    Drama = "Drama"
    Crime = "Crime"
    Action = "Action"
    Adventure = "Adventure"
    Biography = "Biography"
    History = "History"
    SciFi = "Sci-Fi"
    Romance = "Romance"
    Western = "Western"
    Fantasy = "Fantasy"
    Comedy = "Comedy"
    Thriller = "Thriller"
    Animation = "Animation"
    Family = "Family"
    War = "War"
    Mystery = "Mystery"
    Music = "Music"
    Horror = "Horror"
    Musical = "Musical"
    FilmNoir = "Film-Noir"
    Sport = "Sport"

# Show users name, summary, length, reviews
class DisplayMovieShort(BaseModel):
    id: int
    name: str
    summary: str
    runtime: int

# Show users name, summary, length, reviews
class DisplayMovieAvg(DisplayMovieShort):
    average: int

class DisplayReviewNumber(BaseModel):
    id: int
    username: str
    review_count: int

class DisplayUsers(BaseModel):
    rate_entries_user: list[RatingRead] = []