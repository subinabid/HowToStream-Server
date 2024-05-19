from fastapi import FastAPI
from scrapper import get_imdb_top_250
from db import AppDb

app = FastAPI()


# Get movies from db
def get_movies():
    """Get the movies from the database."""
    app_db = AppDb()
    query = "SELECT * FROM movies"
    movies = app_db.cursor.execute(query).fetchall()
    app_db.connection.close()
    return movies


@app.get("/")
def index():
    return {"IMDb_250": get_movies()}
