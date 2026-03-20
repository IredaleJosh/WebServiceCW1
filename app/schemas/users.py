from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.ratings import RatingRead

# Display all but password
class UserBase(BaseModel):
    id : int
    username : str
    email : EmailStr

# Required Fields when making usernames
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6, max_length=20)
    email: EmailStr

# Shows thier username and all reviews
class DisplayUsername(BaseModel):
    username: str
    rate_entries_user: list[RatingRead] = []

# Update username, mus be 
class UserUpdate(BaseModel):
    username: Optional[str] = Field(min_length=3, max_length=20)
    password: Optional[str] = Field(min_length=6, max_length=20)
    email: Optional[EmailStr] = None

# Delete User
class UserDelete(UserBase):
    Message: str

# Shows users access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"