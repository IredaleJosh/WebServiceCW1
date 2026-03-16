from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    id : int
    username : str
    email : str

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=6)
    email: EmailStr

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"