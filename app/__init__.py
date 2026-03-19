from app.database import Base, engine
from app.model import users_movies, Movie, User

Base.metadata.create_all(bind=engine)