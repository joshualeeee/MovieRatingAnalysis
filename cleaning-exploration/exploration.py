import sys
from datetime import datetime
import time
from collections import Counter
import duckdb
import matplotlib.pyplot as plt


def explore():
    con = duckdb.connect()

    movieCSV = '../../movieDatasets/movies.csv'
    releaseCSV = '../../movieDatasets/releases.csv'

    print("\n ** Examples of Movie Entry **")
    query = f"SELECT * FROM read_csv_auto('{movieCSV}') LIMIT 1;"
    res = con.execute(query).fetchone()
    print(res)
    
    query = f"""
            SELECT 
                (COUNT(*) FILTER (WHERE rating IS NULL) * 100.0 / COUNT(*)) AS missing_rating_percentage
            FROM read_csv_auto('{movieCSV}');
    """

    res = con.execute(query).fetchone()[0]

    print(f"\n Rating Missing From {res:.2f}% of Entries")

    query = f"""
                SELECT date, COUNT(*) AS movie_count
                FROM read_csv_auto('{movieCSV}')
                WHERE date IS NOT NULL
                GROUP BY date
                ORDER BY date;
            """
    res = con.execute(query).fetchall()

    years, movie_counts = zip(*res)

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.bar(years, movie_counts, width=1.5, edgecolor="black")
    plt.xlabel("Year")
    plt.ylabel("Number of Movies Produced")
    plt.title("Number of Movies Produced Per Year")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    
    # plt.savefig("movies_per_year.png", dpi=300, bbox_inches="tight")

    query = f"""
                SELECT DISTINCT genre
                FROM read_csv_auto('../../movieDatasets/genres.csv')
                ORDER BY RANDOM()
                LIMIT 3;
            """
    res = con.execute(query).fetchall()
    print("\n ** Examples of Genres **")
    for genre in res:
        print(genre)


    query = f"""
                SELECT DISTINCT theme
                FROM read_csv_auto('../../movieDatasets/themes.csv')
                ORDER BY RANDOM()
                LIMIT 3;
            """
    res = con.execute(query).fetchall()
    print("\n ** Examples of Themes **")
    for genre in res:
        print(genre)

    query = f"""
            SELECT 
                (COUNT(*) FILTER (WHERE date IS NULL) * 100.0 / COUNT(*)) AS missing_date_percentage,
                (COUNT(*) FILTER (WHERE country IS NULL) * 100.0 / COUNT(*)) AS missing_country_percentage,
                (COUNT(*) FILTER (WHERE type IS NULL) * 100.0 / COUNT(*)) AS missing_type_percentage,
                (COUNT(*) FILTER (WHERE rating IS NULL) * 100.0 / COUNT(*)) AS missing_rating_percentage
            FROM read_csv_auto('{releaseCSV}');
    """

    res = con.execute(query).fetchall()[0]
    

    print(f"** Date Missing From {res[0]:.2f}% of Entries **")
    print(f"** Country Missing From {res[1]:.2f}% of Entries **")
    print(f"** Type Missing From {res[0]:.2f}% of Entries **")
    print(f"** Rating Missing From {res[1]:.2f}% of Entries **")



    
    

if __name__ == "__main__":
    explore()