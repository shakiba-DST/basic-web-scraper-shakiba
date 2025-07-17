import re
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import os


def parse_movies_from_html(html_file_path):
    """Parse movie data from HTML file and return list of movies"""
    with open(html_file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    movies = []
    movie_divs = soup.find_all('div', class_='movie')
    
    for movie_div in movie_divs:
        # Extract movie title
        title_elem = movie_div.find('span', class_='resultTitle')
        if not title_elem:
            continue
        title = title_elem.find('a').text.strip()
        
        # Extract movie info (genres, rating, length)
        info_elem = movie_div.find('span', class_='resultInfo')
        if not info_elem:
            continue
        
        info_text = info_elem.text.strip()
        # Split by ' - ' to get genres, rating, and length
        parts = [p.strip() for p in info_text.split(' - ')]
        
        if len(parts) >= 3:
            genres = parts[0]
            rating = parts[1]
            length_str = parts[2]
            
            # Extract numeric length (remove "min" and whitespace)
            length_match = re.search(r'(\d+)\s*min', length_str)
            length = int(length_match.group(1)) if length_match else 0
            
            movies.append({
                'name': title,
                'rating': rating,
                'length': length
            })
    
    return movies


def save_movies_to_csv(movies, output_dir='app/data'):
    """Save movie data to CSV file with today's date"""
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with today's date
    today = datetime.now().strftime('%Y-%m-%d')
    csv_filename = f'movie_output_{today}.csv'
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Write to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'rating', 'length']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(movies)
    
    print(f"Saved {len(movies)} movies to {csv_path}")
    return csv_path


if __name__ == "__main__":
    # Parse HTML and save to CSV
    html_file = "app/data/sample_response_2025-07-17.html"
    movies = parse_movies_from_html(html_file)
    csv_path = save_movies_to_csv(movies)
    
    # Display sample data
    print(f"\nSample movies (first 5):")
    for movie in movies[:5]:
        print(f"  {movie}")