from sqlalchemy import Column, Integer, String, Float, Date, Table, Boolean
from sqlalchemy import PrimaryKeyConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

# M:M - Users and Movies make favourites
users_movies = Table(
    "users_movies",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("Users.id"), primary_key=True),
    Column("movie_id", Integer, ForeignKey("Movies.id"), primary_key=True)
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
    summary = Column(String(200))
    release = Column(Date)
    runtime = Column(Integer) # in minutes, so whole numbers
    budget = Column(Float) # 2dp
    revenue = Column(Float) # 2dp
    genre = Column(String)

    # relationships - simple for now
    favourites = relationship("User", secondary=users_movies, back_populates="movie")
    cast_entries_movie = relationship("Cast", back_populates="movie", passive_deletes=True)
    rate_entries_movie = relationship("Rating", back_populates="movie", passive_deletes=True)

# Stores the Users 
class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True)
    password = Column(String(30))
    email = Column(String(30))
    admin = Column(Boolean, default=False)

    rate_entries_user = relationship("Rating", back_populates="user", passive_deletes=True)
    movie = relationship("Movie", secondary=users_movies, back_populates="favourites")