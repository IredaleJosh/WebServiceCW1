from sqlalchemy import Column, Integer, String, Float, Date, Table
from sqlalchemy import PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

# M:M - Movies and Genres
movie_genre = Table(
    "movie_genre",
    Column("movie_id", Integer, ForeignKey("Movie.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("Genre.id"), primary_key=True)
)
# M:M - Movies and Users


# Class for the Movie itself, inherits from Base
class Movie(Base):
    __tablename__ = "Movies"
    # Identifier for this model
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    # add validation
    summary = Column(String(200))
    release = Column(Date)
    runtime = Column(Integer) # in minutes
    budget = Column(Float) # 2dp
    revenue = Column(Float) # 2dp

    # relationships - simple for now
    genres = relationship("Genre", secondary= movie_genre, back_populates="Movies")
    actors = relationship("Actors", back_populates="Movies")

# Class for storing genre
# Movies can have MANY genres
# Genres can have MANY movies
class Genre(Base):
    __tablename__ = "Genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), index=True)
