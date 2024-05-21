"""Scrapper."""

from urllib.request import urlopen, Request
import re


def get_movie_names(s: str) -> list[str]:
    """Get movie names from the raw HTML."""
    movie_list_raw = re.findall(r"<h3.*?>(.*?)</h3>", s)
    movies = []
    for movie in movie_list_raw:
        space = movie.find(". ") + 2

        title = movie[space:]
        movies.append(title)

    return movies


def get_imdb_top_250():
    """Get the top 250 movies from IMDb."""
    req = Request(
        "https://www.imdb.com/chart/top/", headers={"User-Agent": "Mozilla/5.0"}
    )
    top_250 = urlopen(req).read().decode("utf-8")

    # Get the raw HTML for the list of movies
    ul_start = top_250.find("""<ul class="ipc-metadata-list""")
    start = top_250.find("""<li""", ul_start)
    end = top_250.find("""</ul>""", start)
    movie_list_raw = top_250[start:end]

    return get_movie_names(movie_list_raw)
