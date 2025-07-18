from fastapi import FastAPI, Query
from typing import List, Dict, Optional
import pandas as pd
import os
from datetime import datetime

app = FastAPI(title="Movie API", description="API to fetch movie data from scraped allmovie.com data")

def load_movie_data() -> List[Dict]:
    """Load movie data from the CSV file and return as list of dictionaries."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"app/data/movie_output_{timestamp}.csv"
    
    if not os.path.exists(csv_filename):
        return []
    
    df = pd.read_csv(csv_filename)
    
    movies = []
    for _, row in df.iterrows():
        try:
            length_str = str(row['Length']).replace(' min', '').strip()
            length_int = int(length_str)
        except (ValueError, AttributeError):
            length_int = 0
        
        movie = {
            'name': str(row['Name']).strip(),
            'rating': str(row['Rating']).strip(),
            'length': length_int
        }
        movies.append(movie)
    
    return movies

@app.get("/movies/all", response_model=List[Dict])
async def get_all_movies():
    """Get all movies from the CSV file."""
    return load_movie_data()

@app.get("/movies", response_model=List[Dict])
async def get_movies_by_rating(rating: Optional[str] = Query(None, description="Filter movies by rating (e.g., PG-13, R, Not Rated)")):
    """Get movies filtered by rating."""
    movies = load_movie_data()
    
    if rating:
        filtered_movies = [movie for movie in movies if movie['rating'].lower() == rating.lower()]
        return filtered_movies
    
    return movies

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Movie API - Scraped data from allmovie.com",
        "endpoints": {
            "/movies/all": "Get all movies",
            "/movies?rating=<rating>": "Get movies filtered by rating",
            "/docs": "API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
