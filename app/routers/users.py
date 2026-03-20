from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_curr_user, create_access_token
from app.database import get_db
from app.model import User
from app.schemas.users import UserBase, UserCreate, UserUpdate, UserDelete, Token

router = APIRouter(tags=["Users"])

# CRUD
# CREATE - Register an email, name and password and display email and username
@router.post("/register", 
            response_model=UserBase,
            status_code=201, 
            description="Register an email, name and password and display email and username",
            responses={
                409: {"description":"Username already exists"},
                422: {"description":"Validation Error"}
            })
def register(user: UserCreate, db : Session = Depends(get_db)):
    new_user = User(
        username=user.username, password=user.password, email=user.email, 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# LOGIN - Login to current account to decide if ADMIN or NORMAL USER
@router.post("/login",
            response_model=Token,
            status_code=201, 
            description="Login to current account to recieve JWT token, to perform actions for your account or admin controls",
            responses={
                 400: {"description":"Invalid Username"},
                 422: {"description":"Validation Error"}
            })
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Username")
    access_token = create_access_token({"sub": user.username})
    return {"access_token" : access_token, "token_type": "bearer"}

# READ - Search for users via ID 
@router.get("/users/{user_id}/overview",
            status_code=200,  
            response_model=UserBase, 
            description="Can view usernames and emails of other users",
            responses={
                 400: {"description":"Invalid Input"},
                 404: {"description":"User not found"},
                 422: {"description":"Validation Error"}
            })
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user

# UPDATE - ONLY the Current User can change their email, name, password
@router.put("/users/{user_id}/update", 
            status_code=200,  
            response_model=UserBase, 
            description="Change username, password or email, but verifies if they are changing their username and email",
            responses={
                401: {"description":"Not Authorised"},
                400: {"description":"Invalid Input"},
                422: {"description":"Validation Error"}
            })
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), curr_user : User = Depends(get_curr_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# DELETE - Current User can delete their account
@router.delete("/users/{user_id}/delete", 
            status_code=200,   
            response_model=UserDelete, 
            description="Current User deletes thier account",
            responses={
                401: {"description":"Not Authorised"},
                404: {"description":"User not found"},
                422: {"description":"Validation Error"}
            })
def delete_user(user_id: int, db: Session = Depends(get_db), curr_user : User = Depends(get_curr_user)):
    user = db.query(User).filter(User.id == user_id).first()
    temp_user=user
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    db.delete(user)
    db.commit()
    return {"id":temp_user.id, "username":temp_user.username, "email": temp_user.email, "Message" : "Deleted User"}