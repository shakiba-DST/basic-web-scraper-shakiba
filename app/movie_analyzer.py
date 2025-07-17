import csv
import os
from collections import Counter
from datetime import datetime


def analyze_movies():
    """Analyze movie data from the CSV file and print statistics."""
    # Find the movie CSV file with the date pattern
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    csv_files = [f for f in os.listdir(data_dir) if f.startswith('movie_output_') and f.endswith('.csv')]
    
    if not csv_files:
        print("No movie output CSV file found!")
        return
    
    # Use the first matching file (should be movie_output_2025-07-17.csv)
    csv_file = os.path.join(data_dir, csv_files[0])
    
    # Read the CSV file
    movies = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies.append({
                'title': row['title'],
                'length': int(row['length']),
                'rating': row['rating']
            })
    
    # Calculate average length
    total_length = sum(movie['length'] for movie in movies)
    average_length = total_length / len(movies)
    average_length_int = int(round(average_length))
    
    # Find most common rating(s)
    ratings = [movie['rating'] for movie in movies]
    rating_counts = Counter(ratings)
    max_count = max(rating_counts.values())
    most_common_ratings = [rating for rating, count in rating_counts.items() if count == max_count]
    
    # Count movies with the most common rating
    movie_count = max_count
    
    # Format output based on number of tied ratings
    if len(most_common_ratings) == 1:
        rating_str = most_common_ratings[0]
        count_word = "movie has" if movie_count == 1 else "movies have"
        output = f"The average length of all movies is {average_length_int} minutes. {movie_count} {count_word} the rating of {rating_str} which is the most common rating."
    else:
        # Handle ties
        rating_str = " and ".join(most_common_ratings)
        count_word = "movie has" if movie_count == 1 else "movies have"
        output = f"The average length of all movies is {average_length_int} minutes. {movie_count} {count_word} the rating of {rating_str} which are the most common ratings."
    
    print(output)