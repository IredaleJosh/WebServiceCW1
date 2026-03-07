from app.db.database import Base, engine
from app.models.movie import users_movies, movie_genre, Movie, Actor, Cast, Rating, User, Genre

Base.metadata.create_all(bind=engine)