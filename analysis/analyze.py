import sys
from datetime import datetime
import time
from collections import Counter
import duckdb
import matplotlib.pyplot as plt


def analyze():
    con = duckdb.connect()

    movieCSV = '../../movieDatasets/movies.csv'
    releaseCSV = '../../movieDatasets/releases.csv'
    genresCSV = '../../movieDatasets/genres.csv'

    query = f"""
        SELECT m.date, g.genre, COUNT(*) AS movie_count
        FROM read_csv_auto('{movieCSV}') AS m
        JOIN read_csv_auto('{genresCSV}') AS g
        ON m.id = g.id
        WHERE m.date IS NOT NULL AND m.date <= 2024
        GROUP BY m.date, g.genre
        ORDER BY m.date, g.genre;
    """
    
    res = con.execute(query).fetchall()

    # Organize data into a nested dictionary {year: {genre: count}}
    genre_data = {}
    total_per_year = {}

    for year, genre, count in res:
        if year not in genre_data:
            genre_data[year] = {}
            total_per_year[year] = 0
        genre_data[year][genre] = count
        total_per_year[year] += count  # Track total movies in each year

    # Get sorted list of unique years and genres
    unique_years = sorted(genre_data.keys())
    unique_genres = sorted(set(genre for year in genre_data for genre in genre_data[year]))

    # Normalize counts to percentages
    normalized_genre_data = {year: {g: (genre_data[year].get(g, 0) / total_per_year[year]) * 100 for g in unique_genres} for year in unique_years}

    # Prepare data for plotting
    stacked_data = {genre: [normalized_genre_data[year].get(genre, 0) for year in unique_years] for genre in unique_genres}
    
    # Plot as a stacked area chart
    plt.figure(figsize=(12, 6))
    bottom_stack = [0] * len(unique_years)

    for genre in unique_genres:
        values = stacked_data[genre]
        plt.fill_between(unique_years, bottom_stack, [sum(x) for x in zip(bottom_stack, values)], label=genre, alpha=0.7)
        bottom_stack = [sum(x) for x in zip(bottom_stack, values)]

    # Formatting the plot
    plt.xlabel("Year")
    plt.ylabel("Percentage of Movies")
    plt.title("Genre Popularity Over Time (Normalized % per Year)")
    plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig("genre_popularity_over_time.png", dpi=300, bbox_inches="tight")
    plt.show()

    
if __name__ == "__main__":
    analyze()