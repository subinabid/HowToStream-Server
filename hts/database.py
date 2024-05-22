"""Database connection module."""

import sqlite3
from typing import Any


class AppDb:
    """Database connection class."""

    def __init__(self, db_path: str):
        """Initialize the database connection."""
        self.connection = sqlite3.connect(db_path)
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
