import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
from datetime import datetime
import re


class AllMovieSpider(scrapy.Spider):
    name = "allmovie"
    start_urls = ["https://allmovie.com/showtimes/movies"]

    def __init__(self):
        self.movie_data = []

    def parse(self, response):
        # Print status code
        print(f"Status Code: {response.status}")
        print(f"HTML length: {len(response.text)} characters")

        # Extract movie data
        movies = response.css('div.movie')
        print(f"Found {len(movies)} movie elements")
        
        for movie in movies:
            # Extract movie name
            name_element = movie.css('span.resultTitle a::text')
            name = name_element.get().strip() if name_element else "Unknown"
            
            # Extract the result info (contains category, rating, and duration)
            result_info = movie.css('span.resultInfo::text').get()
            
            if result_info:
                result_info = result_info.strip()
                print(f"Processing: {name} - {result_info}")
                
                # Parse the result info to extract category, rating, and duration
                category, rating, duration = self.parse_result_info(result_info)
                
                self.movie_data.append({
                    'name': name,
                    'category': category,
                    'rating': rating,
                    'length': duration
                })
            else:
                print(f"No result info found for: {name}")
        
        print(f"Extracted {len(self.movie_data)} movies")
        
        # Limit to first 20 movies as requested
        if len(self.movie_data) > 20:
            self.movie_data = self.movie_data[:20]
            print(f"Limited to first 20 movies")
        
        # Sort alphabetically by name
        self.movie_data.sort(key=lambda x: x['name'].lower())
        print("Movies sorted alphabetically")
        
        # Save to CSV
        self.save_to_csv()

    def parse_result_info(self, result_info):
        """
        Parse result info string like "Comedy - PG-13 - 89 min"
        or "Adventure, Drama, Fantasy - PG-13 - 201 min"
        """
        # Split by " - " to separate the parts
        parts = [part.strip() for part in result_info.split(' - ')]
        
        category = "Unknown"
        rating = "Not Rated"
        duration = "Unknown"
        
        if len(parts) >= 3:
            category = parts[0]
            rating = parts[1]
            duration = parts[2]
        elif len(parts) == 2:
            # Handle cases where rating might be missing
            category = parts[0]
            # Check if the second part looks like duration (contains 'min')
            if 'min' in parts[1]:
                duration = parts[1]
            else:
                rating = parts[1]
        elif len(parts) == 1:
            # Only category provided
            category = parts[0]
        
        return category, rating, duration

    def save_to_csv(self):
        """Save the movie data to a CSV file"""
        # Create data directory if it doesn't exist
        os.makedirs('app/data', exist_ok=True)
        
        # Generate filename with current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"app/data/movie_output_{current_date}.csv"
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(self.movie_data)
        df.to_csv(filename, index=False)
        
        print(f"\nMovie data saved to: {filename}")
        print(f"Total movies saved: {len(self.movie_data)}")
        
        # Display the first few movies for verification
        print("\nFirst 5 movies (alphabetically sorted):")
        for i, movie in enumerate(self.movie_data[:5]):
            print(f"{i+1}. {movie['name']} | {movie['category']} | {movie['rating']} | {movie['length']}")


def scrape_allmovie():
    """Scrape allmovie.com and extract movie data"""
    # Configure settings
    settings = get_project_settings()
    settings.set(
        "USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    settings.set("ROBOTSTXT_OBEY", False)
    settings.set("DOWNLOAD_DELAY", 1)

    # Create crawler process
    process = CrawlerProcess(settings)

    # Add spider to process
    process.crawl(AllMovieSpider)

    # Start crawling
    process.start()

    return "Scraping completed. Check the CSV file in app/data folder."


if __name__ == "__main__":
    result = scrape_allmovie()
    print(result)
