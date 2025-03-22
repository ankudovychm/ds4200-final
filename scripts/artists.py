import pandas as pd
import ast
from sankey import make_sankey

# Read the data
data1 = pd.read_csv('data.csv')
data2 = pd.read_csv('data_w_genres.csv')

# Convert string lists to actual lists
data1['artists'] = data1['artists'].apply(ast.literal_eval)
data2['genres'] = data2['genres'].apply(ast.literal_eval)

# Explode the list of artists so each artist gets its own row
data1_exploded = data1.explode('artists')

# Merge with data2 (matching individual artists)
df = pd.merge(data1_exploded, data2, left_on='artists', right_on='artists', how='inner')

# Convert year to decade
df['decade'] = (df['year'] // 10) * 10

# Compute count and average popularity per artist per decade
artist_stats = df.groupby(['decade', 'artists']).agg(
    count=('artists', 'size'),  
    avg_popularity=('popularity_x', 'mean')  
).reset_index()

# Select the top 5 artists per decade based on count
top_artists_per_decade = artist_stats.sort_values(
    ['decade', 'count'], ascending=[True, False]
).groupby('decade').head(5)

# Merge back to get genres for the top 5 artists only
df_top_artists = pd.merge(
    top_artists_per_decade,
    df[['decade', 'artists', 'genres', 'popularity_x']],
    on=['decade', 'artists'],
    how='inner'
)

# **Pick the first genre only**
df_top_artists['genres'] = df_top_artists['genres'].str[0]

# Compute **average popularity per decade**
decade_popularity = df_top_artists.groupby('decade')['popularity_x'].mean().reset_index()
decade_popularity.rename(columns={'popularity_x': 'avg_popularity'}, inplace=True)

# Compute **average popularity per genre**
genre_popularity = df_top_artists.groupby('genres')['popularity_x'].mean().reset_index()
genre_popularity.rename(columns={'popularity_x': 'avg_popularity'}, inplace=True)

# Merge popularity data into df_top_artists
df_top_artists = pd.merge(df_top_artists, decade_popularity, on='decade', how='left', suffixes=('', '_decade'))
df_top_artists = pd.merge(df_top_artists, genre_popularity, on='genres', how='left', suffixes=('', '_genre'))


# Drop duplicates
df_top_artists_sorted = df_top_artists.drop_duplicates(subset=['decade', 'artists', 'genres']).sort_values(by='decade')
df_top_artists_sorted['avg_popularity_genre'] = df_top_artists_sorted['avg_popularity_genre'].fillna(0)

# Use count for flow, and pass all three popularity metrics
cols = ["decade", "artists", "genres"]

make_sankey(df_top_artists_sorted, cols, 'count', ['avg_popularity', 'avg_popularity_decade', 'avg_popularity_genre'])  