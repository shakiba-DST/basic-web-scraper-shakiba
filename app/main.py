import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import csv
from datetime import datetime


class AllMovieSpider(scrapy.Spider):
    name = "allmovie"
    start_urls = ["https://allmovie.com/showtimes/movies"]

    def parse(self, response):
        # Print status code
        print(f"Status Code: {response.status}")

        # Save sample HTML to file
        timestamp = datetime.now().strftime("%Y-%m-%d")
        sample_file = f"app/data/sample_response_{timestamp}.html"

        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"Sample HTML saved to: {sample_file}")
        print(f"HTML length: {len(response.text)} characters")

        movies = []
        movie_divs = response.css('div.movie')
        
        for movie_div in movie_divs:
            title = movie_div.css('a[href*="atomtickets.com"]::attr(title)').get()
            if title and title.strip():
                movie_info = movie_div.css('span.resultInfo::text').get()
                
                if movie_info:
                    movie_info = movie_info.strip()
                    parts = [p.strip() for p in movie_info.split(' - ')]
                    genre = parts[0] if len(parts) > 0 else ""
                    rating = parts[1] if len(parts) > 1 else ""
                    runtime = parts[2] if len(parts) > 2 else ""
                else:
                    genre = rating = runtime = ""
                
                movies.append({
                    'title': title,
                    'genre': genre,
                    'rating': rating,
                    'runtime': runtime
                })

        csv_file = f"app/data/movies_{timestamp}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if movies:
                writer = csv.DictWriter(f, fieldnames=['title', 'genre', 'rating', 'runtime'])
                writer.writeheader()
                writer.writerows(movies)
                print(f"Extracted {len(movies)} movies to: {csv_file}")
            else:
                print("No movies found to extract")


def scrape_allmovie():
    """Scrape allmovie.com and return HTML content"""
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

    # Start crawling and get results
    results = []
    process.start()

    # Return the result (in a real scenario, you'd capture this from the spider)
    return "Scraping completed. Check the sample HTML file in app/data folder."


if __name__ == "__main__":
    result = scrape_allmovie()
    print(result)
