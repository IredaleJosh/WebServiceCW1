from app.database import Base, engine
from app.model import movie_genre, Movie, User, Genre, Rating

Base.metadata.create_all(bind=engine)