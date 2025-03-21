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

# Count total occurrences of each artist per decade
artist_counts = df.groupby(['decade', 'artists']).size().reset_index(name='count')

# Select the top 5 artists per decade
top_artists_per_decade = artist_counts.sort_values(
    ['decade', 'count'], ascending=[True, False]
).groupby('decade').head(5)

# Merge back to get genres for the top 5 artists only
df_top_artists = pd.merge(
    top_artists_per_decade,
    df[['decade', 'artists', 'genres']],
    on=['decade', 'artists'],
    how='inner'
)

# **Pick the first genre only** (instead of exploding genres)
df_top_artists['genres'] = df_top_artists['genres'].str[0]

# Drop duplicates
df_top_artists = df_top_artists.drop_duplicates(subset=['decade', 'artists', 'genres'])
df_top_artists_sorted = df_top_artists.sort_values(by='decade', ascending=True)

cols = ["decade", "artists", "genres"]
make_sankey(df_top_artists_sorted, cols, 'count')
