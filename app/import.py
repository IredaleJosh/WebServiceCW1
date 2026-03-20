import csv
from database import session_local
from model import Movie, Genre

db = session_local()

with open("app/imdb_top_1000.csv", encoding="utf-8") as f:
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