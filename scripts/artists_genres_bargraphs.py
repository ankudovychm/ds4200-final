import pandas as pd
import altair as alt
import ast

# Read the data
data1 = pd.read_csv('data.csv')
data2 = pd.read_csv('data_w_genres.csv')

# Convert string lists to actual lists
data1['artists'] = data1['artists'].apply(ast.literal_eval)
data2['genres'] = data2['genres'].apply(ast.literal_eval)

# Explode artist lists and merge data
data1_exploded = data1.explode('artists')
data2_exploded = data2.explode('genres')
data2_exploded = data2_exploded.dropna(subset=['genres'])
df = pd.merge(data1_exploded, data2_exploded, left_on='artists', right_on='artists', how='inner')

def map_genre(genre):
    genre = str(genre).lower()  # Force genre to be a string and convert to lowercase
    # Check for specific keywords and map to the standardized genre name
    if 'pop' in genre:
        return 'pop'
    elif 'rap' in genre:
        return 'rap'
    elif 'hip-hop' in genre or 'hip hop' in genre or 'hiphop' in genre:
        return 'hip-hop'
    elif 'rock' in genre:
        return 'rock'
    elif 'country' in genre:
        return 'country'
    elif 'electronic' in genre:
        return 'electronic'
    elif 'r&b' in genre or 'rnb' in genre:
        return 'r&b'
    elif 'jazz' in genre:
        return 'jazz'
    elif 'classical' in genre:
        return 'classical'
    elif 'reggae' in genre:
        return 'reggae'
    elif 'metal' in genre:
        return 'metal'
    elif 'tango' in genre:
        return 'tango'
    else:
        return genre  # If none of the above, return the genre as is

# Apply genre mapping with the updated function
df['genres_mapped'] = df['genres'].apply(map_genre)

# Convert year to decade
df['decade'] = (df['year'] // 10) * 10

# Group data for artists and genres
artist_stats = df.groupby(['decade', 'artists']).agg(
    count=('artists', 'size'),  
    avg_popularity=('popularity_x', 'mean')  
).reset_index()

# Group data for genres (using genres_mapped)
genre_stats = df.explode('genres_mapped').groupby(['decade', 'genres_mapped']).agg(
    count=('genres_mapped', 'size'),
    avg_popularity=('popularity_x', 'mean')
).reset_index()

# Define sliders
slider_decade = alt.binding_range(min=df['decade'].min(), max=df['decade'].max(), step=10, name='Decade Filter')
slider_count = alt.binding_range(min=1, max=15, step=1, name="Number of Artists and Genres to Show")

selection_decade = alt.selection_point(fields=['decade'], bind=slider_decade, name="decade_filter", value=[{'decade': 2000}])
selection_count = alt.param(name="top_n", value=5, bind=slider_count)

# Artist bar chart
artist_chart = alt.Chart(artist_stats).mark_bar().encode(
    x=alt.X('count:Q', title='Number of Songs'),
    y=alt.Y('artists:N', sort='-x', title='Top Artists'),
    color=alt.Color('avg_popularity:Q', scale=alt.Scale(domain=[0, 100], scheme='redyellowgreen'), title='Popularity'),
    tooltip=['artists', 'count', 'avg_popularity']
).transform_filter(selection_decade).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('count', order='descending')]
).transform_filter(alt.datum.rank <= selection_count
                   ).properties(width=400, height=300, title="Top Artists by Number of Songs")

# Genre bar chart
genre_chart = alt.Chart(genre_stats).mark_bar().encode(
    x=alt.X('count:Q', title='Number of Songs'),
    y=alt.Y('genres_mapped:N', sort='-x', title='Top Genres'),
    color=alt.Color('avg_popularity:Q', scale=alt.Scale(domain=[0, 100], scheme='magma'), title='Popularity'),
    tooltip=['genres_mapped', 'count', 'avg_popularity']
).transform_filter(selection_decade).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('count', order='descending')]
).transform_filter(alt.datum.rank <= selection_count
                   ).properties(width=400, height=300, title="Top Genres by Number of Songs")
# Combine charts with sliders below
final_chart = alt.vconcat(
    artist_chart,
    genre_chart
).add_params(
    selection_decade,
    selection_count)

# Display the chart
final_chart.save('artist_genre_bargraphs.html')
