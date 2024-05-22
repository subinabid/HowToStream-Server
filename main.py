"""FastAPI app."""

from fastapi import FastAPI
from hts.database import AppDb
from settings import db_path

# Initialize the app
app = FastAPI()


# Get all movies from db
def get_movies():
    """Get the movies from the database."""
    app_db = AppDb(db_path)
    query = "SELECT * FROM movies"
    movies = app_db.cursor.execute(query).fetchall()
    app_db.connection.close()
    return movies


# Routers
@app.get("/")
def root():
    """Root."""
    return {"IMDb_250": get_movies()}
