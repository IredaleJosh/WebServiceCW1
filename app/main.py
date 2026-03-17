# inside directory with __init__.py, so a module of the package: app.main
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from app.routers.movies import router as movies_routers
from app.routers.users import router as users_routers
from app.routers.ratings import router as rating_routers
from app.routers.analytics import router as analytics_routers

app = FastAPI()
app.include_router(movies_routers)
app.include_router(users_routers)
app.include_router(rating_routers)
app.include_router(analytics_routers)

# main path
@app.get("/")
def root():
    return {"status" : "Ok, Welcome to Website"}


