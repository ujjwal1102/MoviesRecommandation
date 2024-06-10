import pandas as pd
import sqlite3
import random
from datetime import datetime

# Load the CSV file
csv_file_path = 'D://Let\'s Code//python files//raw files//tmdb_movies3.csv'
df = pd.read_csv(csv_file_path)

# Connect to the SQLite database
db_path = 'D://Let\'s Code//python files//raw files//db_old.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define the insert statements
insert_movie_query = '''
INSERT INTO reviews_movie (title, description, release_date, genre)
VALUES (?, ?, ?, ?)
ON CONFLICT(title) DO UPDATE SET description=excluded.description, release_date=excluded.release_date, genre=excluded.genre;
'''

insert_review_query = '''
INSERT INTO reviews_review (movie_id, user_id, rating, comment)
VALUES (?, ?, ?, ?)
'''

# Iterate through the DataFrame and insert data
for index, row in df.iterrows():
    release_date = row['release_date']
    if pd.isnull(release_date):
        release_date = '1970-01-01'  # Use a default date or skip this row

    # Insert movie
    cursor.execute(insert_movie_query, (
        row['title'],
        row['overview'],
        release_date,  # Use the handled release_date variable
        row['genre_ids']
    ))

    # Get the movie_id of the inserted or updated movie
    cursor.execute('SELECT id FROM reviews_movie WHERE title = ?', (row['title'],))
    movie_id = cursor.fetchone()[0]

    # Generate a random user_id between 1 and 10
    user_id = random.randint(1, 10)

    # Insert review
    cursor.execute(insert_review_query, (
        movie_id,
        user_id,  # Random user_id
        row['vote_average'],  # Use vote_average for ratings
        "No comment"  # Static comment
    ))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data imported successfully")
