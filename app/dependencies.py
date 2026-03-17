# dependencies/ Security
# annotated --> allows for extra information, in most cases extra validation
from fastapi import Header, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

from app.movie import User
from app.schemas.users import UserBase
from app.database import get_db

# Needed for JWT

# Secrete Keys
# 8393595ca084b5c24e0f6ffcfb5fca9236c64e3c260f7ee306b0413fdf71b6af
# 3c96622bdc9b375f017206ee130c2e84bf7eb4c214bf2e4bc6206852a73e0ebe
# 528404e44b11fe45289ab3f5a5f99e6320e3ab1eddd56334c6a4cc1817c42e1c

SECRET_KEY = "0677cc7030a9744e564f60ecace0b81eca1c4a950344836704a518660ba75a19"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "users/login")

# Get the User and return them if they are in the database
def get_user(username: str, db : Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user


# Security Functions - Generates Signed JWT + Expire Time
def create_access_token(data: dict, expires : int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires)
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Auto runs on protected routes
# extract jwt token, verifies and checks expiry
async def get_curr_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user

# Check if Admin or not
    # Calls current user and checks if the current user is the admin
async def check_admin(curr_user : User = Depends(get_curr_user)):
    if curr_user.admin == False:
        raise HTTPException(status_code=403, detail="Admins Only")
    return curr_user


async def get_token_head(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided") 