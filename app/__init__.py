from app.database import Base, engine
from app.movie import users_movies, movie_genre, Movie, Actor, Cast, User, Genre

Base.metadata.create_all(bind=engine)