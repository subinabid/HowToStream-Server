"""FastAPI app."""

from fastapi import FastAPI
from hts.database import AppDb
import os

# Configurations
prod_db_path = os.path.join(os.path.dirname(__file__), "hts.db")
test_db_path = os.path.join(os.path.dirname(__file__), "hts-test.db")

# test or prod mode
MODE = "test"  # or prod
db_path = prod_db_path if MODE == "prod" else test_db_path

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
