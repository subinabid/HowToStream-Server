"""Create the db and seed data."""

import sys

# import argparse
from typing import Any
from scrapper import get_imdb_top_250

sys.path.append("..")
sys.path.append("../..")
# TODO: replace ".." with os path
from database import AppDb  # noqa: E402
from main import db_path  # noqa: E402


def add_movie(connection, movie: str) -> dict[str, Any]:
    """Add a movie to the movies table if it does not exist."""
    query_to_check_movie = "SELECT * FROM movies WHERE title = ?"
    query_insert_movie = "INSERT INTO movies (title) VALUES (?)"
    cursor = connection.cursor()
    try:
        cursor.execute(query_to_check_movie, (movie,))
        result = cursor.fetchone()
        if result:
            return {"message": "Movie already exists", "id": result[0], "flag": 0}

        cursor.execute(query_insert_movie, (movie,))
        connection.commit()

        return {
            "message": "Movie added successfully",
            "id": cursor.lastrowid,
            "flag": 1,
        }

    except Exception as e:
        return {
            "message": "Failed to add movie",
            "error": e,
            "flag": 2,
        }


def add_movies(connection, movies: list) -> dict[str, Any]:
    """Populate the movies table."""
    result: list[int] = list()
    try:
        for movie in movies:
            info = add_movie(connection, movie)
            result.append(info["flag"])

        return {
            "message": f"{result.count(1)} of {len(movies)} movies added",
        }

    except Exception as e:
        return {
            "message": "Failed to add movie list",
            "error": e,
        }


def add_imdb_top_250(connection) -> dict[str, Any]:
    """Add the IMDb top 250 movies to the database."""
    movies = get_imdb_top_250()
    return add_movies(connection, movies)


def main(db_path) -> None:
    """Initialize and populate the database.

    Args:
        db_path (str): Path to the database.

    """
    app_db = AppDb(db_path)
    print("Initiating the database...")
    print("Creating tables...")
    print("The following tables were created (or already exists):")
    print(app_db.create_tables())
    print("Adding IMDb top 250 movies to the Movie table...")
    print(add_imdb_top_250(app_db.connection))
    app_db.connection.close()


if __name__ == "__main__":
    """Run the main function."""
    main(db_path)
