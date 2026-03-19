from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.ratings import RatingRead

class UserBase(BaseModel):
    id : int
    username : str
    email : EmailStr

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)
    email: EmailStr

class DisplayUsername(BaseModel):
    username: str
    rate_entries_user: list[RatingRead] = []

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"