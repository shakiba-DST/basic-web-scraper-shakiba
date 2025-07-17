from fastapi import FastAPI, HTTPException
from pathlib import Path
import csv
import re
from glob import glob

app = FastAPI(title="Movie API")

def get_latest_csv_path() -> Path:
    data_dir = Path(__file__).resolve().parent / "data"
    csv_files = sorted(data_dir.glob("movie_output_*.csv"))
    if not csv_files:
        raise FileNotFoundError("No movie_output CSV files found in 'app/data'.")
    return csv_files[-1]

def read_movies() -> list:
    path = get_latest_csv_path()
    movies = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            rating = row.get("rating", "").strip()
            length_raw = row.get("length", "")
            match = re.search(r"\d+", length_raw)
            length = int(match.group()) if match else None
            movies.append({"name": name, "rating": rating, "length": length})
    return movies

@app.get("/movies/all")
def get_all_movies():
    try:
        return read_movies()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/movies")
def get_movies_by_rating(rating: str):
    try:
        movies = read_movies()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    filtered = [m for m in movies if m.get("rating") == rating]
    return filtered
