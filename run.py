from app import main

if __name__ == "__main__":
    main.scrape_allmovie()
    main.process_and_save_data()
    main.analyze_movies()
