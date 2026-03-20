# setup sqlalchemy hgere
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = "postgresql://josh:movie-secret@localhost/moviedb"
# creates database engine and connects to postgresql
engine = create_engine(database_url)
# creates session factory, temp connection to database 
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# parent class for all models
    # Base registers model, stores metadata and allows sqlalchemy to auto create tables
Base = declarative_base()
# Run once
# Base.metadata.create_all(bind=engine)

# To use the database in the routers
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# basic query to test its connected to engine
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT 1;"))
#     print(result.fetchone())

