# inside directory with __init__.py, so a module of the package: app.main
from fastapi import FastAPI
from routers.movies import router as movies_routers
from routers.users import router as users_routers
from routers.ratings import router as rating_routers
from routers.analytics import router as analytics_routers

# Overview
app = FastAPI(
    title="MovieAPI",
    description="API for Movies, Ratings and Users",
    version="1.0"
)

# Routers that are used
app.include_router(users_routers)
app.include_router(movies_routers)
app.include_router(rating_routers)
app.include_router(analytics_routers)

# main path
@app.get("/")
def root():
    return {"status" : "Ok, Welcome to Website"}


