import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import csv
import re
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

        # Extract movie data
        movies = []
        movie_selectors = response.css("section.movies div.showtime-results div.movie")[:20]

        for sel in movie_selectors:
            title = sel.css("span.resultTitle a::text").get()
            info_text = " ".join(sel.css("span.resultInfo::text").getall()).strip()

            length_match = re.search(r"(\d+\s*min)", info_text)
            length = length_match.group(1) if length_match else ""

            rating_match = re.search(
                r"(PG-13|PG|R|G|NC-17|Not Rated|No Rating|NR|Unrated)", info_text
            )
            rating = rating_match.group(1) if rating_match else ""

            if rating_match:
                category = info_text[: rating_match.start()].strip(" -")
            else:
                category = info_text.replace(length, "").strip(" -")

            movies.append({
                "name": title,
                "category": category,
                "rating": rating,
                "length": length,
            })

        movies = sorted(movies, key=lambda x: x["name"])

        os.makedirs("app/data", exist_ok=True)
        csv_file = f"app/data/movie_output_{timestamp}.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "category", "rating", "length"])
            writer.writeheader()
            writer.writerows(movies)

        print(f"Saved {len(movies)} movies to: {csv_file}")

        # Don't return HTML to avoid console spam
        # HTML is saved to file for inspection


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
