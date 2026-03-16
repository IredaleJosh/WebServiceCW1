from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

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