import pandas as pd
import os
from datetime import datetime
from collections import Counter


def analyze_movie_data():
    """Analyze movie data from the CSV file and print statistics."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    csv_filename = f"app/data/movie_output_{timestamp}.csv"
    
    if not os.path.exists(csv_filename):
        print(f"CSV file {csv_filename} not found.")
        return
    
    df = pd.read_csv(csv_filename)
    
    lengths = []
    for length_str in df['Length']:
        try:
            length_num = int(length_str.replace(' min', '').strip())
            lengths.append(length_num)
        except (ValueError, AttributeError):
            continue
    
    if lengths:
        avg_length = int(sum(lengths) / len(lengths))
    else:
        avg_length = 0
    
    rating_counts = Counter(df['Rating'])
    max_count = max(rating_counts.values())
    most_common_ratings = [rating for rating, count in rating_counts.items() if count == max_count]
    
    rating_text = most_common_ratings[0]
    count_text = "movies have" if max_count != 1 else "movie has"
    print(f"The average length of all movies is {avg_length} minutes. {max_count} {count_text} the rating of {rating_text} which is the most common rating.")
