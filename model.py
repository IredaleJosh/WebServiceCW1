from sqlalchemy import Column, Integer, String, Table, Boolean
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

# M:M - Movies and Genres
movie_genre = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("Movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("Genres.id", ondelete="CASCADE"), primary_key=True)
)

# M:M - Users and Movies
    # Extra fields for ratings and reviews
class Rating(Base):
    __tablename__ = "Ratings"
    id = Column(Integer, primary_key=True, index=True)

    users_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    movies_id = Column(Integer, ForeignKey("Movies.id", ondelete="CASCADE"))
    rating = Column(Integer, CheckConstraint('rating >= 0 and rating <=5'))
    review = Column(String(100))

    movie = relationship("Movie", back_populates="rate_entries_movie")
    user = relationship("User", back_populates="rate_entries_user")

# Class for the Movie itself, inherits from Base
class Movie(Base):
    __tablename__ = "Movies"
    # Identifier for this model
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # add validation
    summary = Column(String(350))
    release = Column(Integer)
    runtime = Column(Integer) # in minutes, so whole numbers
    director = Column(String)
    revenue = Column(Integer) # as it has commas
    genre = Column(String)

    # relationships
    genre = relationship("Genre", secondary=movie_genre, back_populates="movie")
    rate_entries_movie = relationship("Rating", back_populates="movie", passive_deletes=True)

# Class for storing genre
# Movies can have MANY genres
# Genres can have MANY movies
class Genre(Base):
    __tablename__ = "Genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), index=True)

    # relationship
    movie = relationship("Movie", secondary=movie_genre, back_populates="genre")

# Stores User details
class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True)
    password = Column(String(30))
    email = Column(String(30), unique=True)
    admin = Column(Boolean, default=False)

    rate_entries_user = relationship("Rating", back_populates="user", passive_deletes=True)