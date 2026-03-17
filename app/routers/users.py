from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.dependencies import get_user, create_access_token
from app.database import get_db
from app.movie import User
from app.schemas.users import UserCreate, UserUpdate, Token

router = APIRouter(prefix="/users", tags=["Users"])

# CRUD

# CREATE - Register an email, name and password
@router.post("/register")
def register(user: UserCreate, db : Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# LOGIN - Login to current accoun to perform UPDATE and DELETE
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Username")
    access_token = create_access_token({"sub": user.username})
    return {"access_token" : access_token, "token_type": "bearer"}

# READ - Search for users
@router.get("/{user_id}/overview")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user

# UPDATE - Current User can change their email, name, password
@router.put("/{user_id}/update")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# DELETE - Current User can delete their username
@router.delete("/{user_id}/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    db.delete(user)
    db.commit()
    return {"Message : Deleted User"}