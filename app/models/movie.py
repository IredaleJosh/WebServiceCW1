from sqlalchemy import Column, Integer, String, Float, Date, Table
from sqlalchemy import PrimaryKeyConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base, engine

# M:M - Movies and Genres
movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("Movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("Genres.id"), primary_key=True)
)
# M:M - Users and Movies make favourites
users_movies = Table(
    "users_movies",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("movie_id", Integer, ForeignKey("Movies.id"), primary_key=True)
)

# M:M - Movies and Actors
    # Multiple fields like character name and importance
    # this way lets us access the datafields in the API
class Cast(Base):
    __tablename__ = "Casts"
    movies_id = Column(Integer, ForeignKey("Movies.id"), primary_key=True)
    actors_id = Column(Integer, ForeignKey("Actors.id"), primary_key=True)
    character = Column(String(30))
    importance = Column(Integer) # Whether they star or play supporting role
    director = Column(String(50)) # just have field for director here 
    Movie = relationship("Movie", back_populates="Casts")
    Actor = relationship("Actor", back_populates="Movies")

# M:M - Users and Movies
    # Extra fields for ratings and reviews
class Rating(Base):
    __tablename__ = "Ratings"
    users_id = Column(Integer, ForeignKey("Users.id"), primary_key=True)
    movies_id = Column(Integer, ForeignKey("Movies.id"), primary_key=True)
    rating = Column(Integer, CheckConstraint('rating >= 0 and rating <=5'))
    review = Column(String(100))

# Class for the Movie itself, inherits from Base
class Movie(Base):
    __tablename__ = "Movies"
    # Identifier for this model
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    # add validation
    summary = Column(String(200))
    release = Column(Date)
    runtime = Column(Integer) # in minutes, so whole numbers
    budget = Column(Float) # 2dp
    revenue = Column(Float) # 2dp

    # relationships - simple for now
    genres = relationship("Genre", secondary= movie_genre, back_populates="Movies")
    favourites = relationship("User", secondary= users_movies, back_populates="Movies")
    casts = relationship("Cast", back_populates="Movies")

# Class for storing genre
# Movies can have MANY genres
# Genres can have MANY movies
class Genre(Base):
    __tablename__ = "Genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), index=True)
    movies = relationship("Movie", secondary="movie_genre", back_populates="Genres")

# Class for Storing Actors
# Movies can have MANY Actors
# Actors can be in MANY Movies
class Actor(Base):
    __tablename__ = "Actors"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), index=True)
    movies = relationship("Cast", back_populates="Actors")

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), index=True, unique=True)
    password = Column(String(30), index=True)
    email = Column(String(30), index=True)