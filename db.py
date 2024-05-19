"""Database connection module."""

import sqlite3
from typing import Any


class AppDb:
    def __init__(self):
        self.connection = sqlite3.connect("hts.db")
        self.cursor = self.connection.cursor()

    def create_tables(self) -> dict[str, Any]:
        """Create tables."""
        query_create_movies = """
            CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT
            );
        """
        query_create_streams = """
            CREATE TABLE IF NOT EXISTS streams (
            id INTEGER PRIMARY KEY,
            movie INTEGER,
            streamer TEXT,
            streamtype TEXT,
            FOREIGN KEY (movie) REFERENCES movies(id)
            );
        """
        try:
            self.cursor.execute(query_create_movies)
            self.cursor.execute(query_create_streams)
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            self.connection.commit()

            return {"message": "Success", "tables": tables}

        except Exception as e:
            return {"message": "Failed to create tables", "error": e}

    def add_movie(self, movie: str) -> dict[str, Any]:
        """Add a movie to the movies table if it does not exist."""
        query_to_check_movie = "SELECT * FROM movies WHERE title = ?"
        query_insert_movie = "INSERT INTO movies (title) VALUES (?)"
        try:
            self.cursor.execute(query_to_check_movie, (movie,))
            result = self.cursor.fetchone()
            if result:
                return {"message": "Movie already exists", "id": result[0], "flag": 0}

            self.cursor.execute(query_insert_movie, (movie,))
            self.connection.commit()

            return {
                "message": "Movie added successfully",
                "id": self.cursor.lastrowid,
                "flag": 1,
            }

        except Exception as e:
            return {
                "message": "Failed to add movie",
                "error": e,
            }

    def add_movies(self, movies: list) -> dict[str, Any]:
        """Populate the movies table."""

        result: list[int] = list()
        try:
            for movie in movies:
                info = self.add_movie(movie)
                if "error" in info.keys():
                    result.append(2)
                else:
                    result.append(info["flag"])

            return {
                "message": f"{result.count(1)} of {len(movies)} movies added",
            }

        except Exception as e:
            return {
                "message": "Failed to add movies",
                "error": e,
            }

    def add_imdb_top_250(self) -> dict[str, Any]:
        """Add the IMDb top 250 movies to the database."""
        from scrapper import get_imdb_top_250

        movies = get_imdb_top_250()
        return self.add_movies(movies)


def main():
    app_db = AppDb()
    print("Initiating the database...")
    print("Creating tables...")
    print("The following tables were created (or already exists):")
    print(app_db.create_tables())
    print("Adding IMDb top 250 movies to the database...")
    print(app_db.add_imdb_top_250())
    app_db.connection.close()


if __name__ == "__main__":
    main()
