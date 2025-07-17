import csv
import os
import re
from collections import Counter
from glob import glob


def print_movie_statistics():
    """Read the latest movie_output_<YYYY-MM-DD>.csv and print statistics."""
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.isdir(data_dir):
        print("No data directory found.")
        return

    csv_files = sorted(glob(os.path.join(data_dir, "movie_output_*.csv")))
    if not csv_files:
        print("No movie_output CSV files found.")
        return

    latest_csv = csv_files[-1]

    lengths = []
    ratings = []
    with open(latest_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            length_str = row.get("length", "")
            match = re.search(r"\d+", length_str)
            if match:
                lengths.append(int(match.group()))
            rating = row.get("rating", "").strip()
            if rating:
                ratings.append(rating)

    avg_length = round(sum(lengths) / len(lengths)) if lengths else 0
    rating_counts = Counter(ratings)
    if not rating_counts:
        print(f"The average length of all movies is {avg_length} minutes. No ratings available.")
        return

    max_count = max(rating_counts.values())
    most_common = sorted([r for r, c in rating_counts.items() if c == max_count])
    rating_text = " and ".join(most_common)

    plural = "ratings" if len(most_common) > 1 else "rating"
    print(
        f"The average length of all movies is {avg_length} minutes. {max_count} movies have the {plural} of {rating_text} which is the most common rating."
    )

