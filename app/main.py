import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from datetime import datetime
import pandas as pd
import re


class AllMovieSpider(scrapy.Spider):
    name = "allmovie"
    start_urls = ["https://www.allmovie.com/showtimes/movies"]

    def parse(self, response):
        movies = []
        for movie in response.css("div.movie"):
            if len(movies) >= 20:
                break

            title = movie.css("span.resultTitle a::text").get()
            details = movie.css("span.resultInfo::text").get()

            if details:
                # Use regex to find rating and length
                rating_match = re.search(r"-\s*(PG-13|PG|R|G|Not Rated|No Rating)\s*-", details)
                length_match = re.search(r"(\d+)\s*min", details)

                rating = rating_match.group(1) if rating_match else "Not Rated"
                length = f"{length_match.group(1)} min" if length_match else ""

                # Assume everything before the rating is the category
                category = details.split(f"- {rating}")[0].strip() if rating_match else details.strip()

            else:
                category, rating, length = "N/A", "N/A", "N/A"

            movies.append(
                {
                    "Name": title,
                    "Category": category,
                    "Rating": rating,
                    "Length": length,
                }
            )
        return movies


def scrape_allmovie():
    """Scrape allmovie.com and return a list of movies."""
    # Configure settings
    settings = get_project_settings()
    settings.set(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    )
    settings.set("ROBOTSTXT_OBEY", False)
    settings.set("DOWNLOAD_DELAY", 1)
    settings.set("FEEDS", {"movies.json": {"format": "json", "overwrite": True}})

    # Create crawler process
    process = CrawlerProcess(settings)

    # Add spider to process
    process.crawl(AllMovieSpider)

    # Start crawling
    process.start()


def process_and_save_data():
    """Processes and saves the scraped movie data."""
    try:
        with open("movies.json", "r") as f:
            data = pd.read_json(f)

        if not data.empty:
            # Sort data alphabetically by movie name
            data_sorted = data.sort_values(by="Name").reset_index(drop=True)

            # Save to CSV
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_dir = "app/data"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, f"movie_output_{timestamp}.csv")
            data_sorted.to_csv(output_file, index=False)
            print(f"Data saved to: {output_file}")
        else:
            print("No data was scraped.")

    except FileNotFoundError:
        print("Scraping did not produce a file.")


if __name__ == "__main__":
    scrape_allmovie()
    process_and_save_data()
