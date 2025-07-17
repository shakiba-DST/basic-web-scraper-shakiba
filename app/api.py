import csv
import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel


# Pydantic model for movie response
class Movie(BaseModel):
    name: str
    rating: str
    length: int


app = FastAPI(title="Movie API", version="1.0.0")


def load_movies_from_csv():
    """Load movies from the most recent CSV file"""
    data_dir = "app/data"
    csv_files = [f for f in os.listdir(data_dir) if f.startswith("movie_output_") and f.endswith(".csv")]
    
    if not csv_files:
        raise FileNotFoundError("No movie CSV files found")
    
    # Get the most recent CSV file
    csv_files.sort(reverse=True)
    latest_csv = os.path.join(data_dir, csv_files[0])
    
    movies = []
    with open(latest_csv, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append(Movie(
                name=row['name'],
                rating=row['rating'],
                length=int(row['length'])
            ))
    
    return movies


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Movie API",
        "endpoints": {
            "/movies/all": "Get all movies",
            "/movies?rating=<rating>": "Get movies filtered by rating (e.g., PG-13, R, Not Rated)",
            "/docs": "API documentation"
        }
    }


@app.get("/movies", response_model=List[Movie])
async def get_movies(rating: Optional[str] = Query(None, description="Filter movies by rating")):
    """
    Get movies with optional rating filter.
    
    - **rating**: Optional rating filter (e.g., PG-13, R, PG, Not Rated, No Rating)
    """
    try:
        movies = load_movies_from_csv()
        
        if rating:
            # Filter movies by rating (case-insensitive)
            filtered_movies = [m for m in movies if m.rating.lower() == rating.lower()]
            return filtered_movies
        
        # If no rating specified, return all movies
        return movies
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No movie data found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/movies/all", response_model=List[Movie])
async def get_all_movies():
    """Get all movies without any filtering"""
    try:
        movies = load_movies_from_csv()
        return movies
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No movie data found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/movies/ratings", response_model=List[str])
async def get_available_ratings():
    """Get list of all available ratings in the dataset"""
    try:
        movies = load_movies_from_csv()
        # Get unique ratings
        ratings = list(set(movie.rating for movie in movies))
        ratings.sort()
        return ratings
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No movie data found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)