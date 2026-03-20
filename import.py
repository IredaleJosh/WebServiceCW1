import csv
from database import session_local, engine, Base
from model import Movie, Genre, User

Base.metadata.create_all(bind=engine)

db = session_local()

# Add Admin
user = User(
    username="admin", password="admin_password", email="admin@gmail.com", admin=True
)
db.add(user)
if user:
    print("Admin Was Made")
else:
    print("Failed to make admin")

with open("imdb_top_1000.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        runtime = row["Runtime"]
        runtime = (
            int(runtime.replace("min", "").strip())
            if runtime and runtime.strip() != ""
            else None
        )
        movie = Movie(
            name=row["Series_Title"], summary=row["Overview"], release=row["Released_Year"], runtime=runtime,
            director=row["Director"], revenue=int(row["Gross"].replace(",", "")) if row["Gross"] else None
        )
        db.add(movie)
        db.flush()

        raw_genres = row["Genre"]
        if raw_genres:
            genre_names = [g.strip() for g in raw_genres.split(",")]
            for gname in genre_names:
                genre = db.query(Genre).filter_by(name=gname).first()
                if not genre:
                    genre = Genre(name=gname)
                    db.add(genre)
                    db.flush()
                movie.genre.append(genre)
    db.commit()

db.close()
print("Complete")