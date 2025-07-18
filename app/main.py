import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
from datetime import datetime


class AllMovieSpider(scrapy.Spider):
    name = "allmovie"
    start_urls = ["https://allmovie.com/showtimes/movies"]

    def parse(self, response):
        print(f"Status Code: {response.status}")

        movies = response.css('div.movie')[:20]
        movie_data = []
        
        for movie in movies:
            title_element = movie.css('span.resultTitle a::text').get()
            if not title_element:
                continue
                
            info_text = movie.css('span.resultInfo::text').get()
            if not info_text:
                continue
                
            info_parts = [part.strip() for part in info_text.split(' - ')]
            if len(info_parts) >= 3:
                categories = info_parts[0]
                rating = info_parts[1] 
                length = info_parts[2]
            else:
                categories = info_parts[0] if len(info_parts) > 0 else "Unknown"
                rating = info_parts[1] if len(info_parts) > 1 else "Unknown"
                length = info_parts[2] if len(info_parts) > 2 else "Unknown"
            
            movie_data.append({
                'Name': title_element.strip(),
                'Category': categories,
                'Rating': rating,
                'Length': length
            })
        
        movie_data.sort(key=lambda x: x['Name'].lower())
        
        df = pd.DataFrame(movie_data)
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"app/data/movie_output_{timestamp}.csv"
        
        df.to_csv(csv_filename, index=False)
        
        print(f"Successfully extracted {len(movie_data)} movies")
        print(f"CSV saved to: {csv_filename}")
        
        return movie_data


def scrape_allmovie():
    """Scrape allmovie.com and return HTML content"""
    settings = get_project_settings()
    settings.set(
        "USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    settings.set("ROBOTSTXT_OBEY", False)
    settings.set("DOWNLOAD_DELAY", 1)

    process = CrawlerProcess(settings)

    process.crawl(AllMovieSpider)

    results = []
    process.start()

    return "Scraping completed. Check the movie_output CSV file in app/data folder."


if __name__ == "__main__":
    result = scrape_allmovie()
    print(result)
