import pandas as pd
import altair as alt
import ast

data1 = pd.read_csv('../Data/data.csv')
data2 = pd.read_csv('../Data/data_w_genres.csv')

# Convert string lists to actual lists
data1['artists'] = data1['artists'].apply(ast.literal_eval)
data2['genres'] = data2['genres'].apply(ast.literal_eval)

# Explode artist lists and merge data
data1_exploded = data1.explode('artists')
data2_exploded = data2.explode('genres')
data2_exploded = data2_exploded.dropna(subset=['genres'])
df = pd.merge(data1_exploded, data2_exploded, left_on='artists', right_on='artists', how='inner')

def map_genre(genre):
    genre = str(genre).lower()  
    genre_mapping = {
        "pop": "pop",
        "rap": "rap",
        "hip-hop": "hip-hop",
        "hip hop": "hip-hop",
        "hiphop": "hip-hop",
        "rock": "rock",
        "country": "country",
        "electronic": "electronic",
        "r&b": "r&b",
        "rnb": "r&b",
        "jazz": "jazz",
        "classical": "classical",
        "reggae": "reggae",
        "metal": "metal",
        "tango": "tango",
        "contemporary": "contemporary",
        "tropical": "tropical"
    }

    for key in genre_mapping:
        if key in genre:
            return genre_mapping[key]

    # Return the original genre if no match
    return genre

df['genres_mapped'] = df['genres'].apply(map_genre)

df['decade'] = (df['year'] // 10) * 10

# Group data for artists
artist_stats = df.groupby(['decade', 'artists']).agg(
    count=('artists', 'size'),  
    avg_popularity=('popularity_x', 'mean')  
).reset_index()

# Group data for genres 
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
    color=alt.Color(
        'avg_popularity:Q',
        scale=alt.Scale(domain=[0, 100], scheme='redyellowgreen'),
        title='Popularity',
        legend=alt.Legend(labelLimit=200)
    ),
    tooltip=['artists', 'count', 'avg_popularity']
).transform_filter(selection_decade).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('count', order='descending')]
).transform_filter(alt.datum.rank <= selection_count
                   ).properties(width=300, height=250, title="Top Artists by Number of Songs")

# Genre bar chart
genre_chart = alt.Chart(genre_stats).mark_bar().encode(
    x=alt.X('count:Q', title='Number of Songs'),
    y=alt.Y('genres_mapped:N', sort='-x', title='Top Genres'),
    color=alt.Color(
        'avg_popularity:Q',
        scale=alt.Scale(domain=[0, 100], scheme='magma'),
        title='Popularity',
        legend=alt.Legend(labelLimit=200)
    ),
    tooltip=['genres_mapped', 'count', 'avg_popularity']
).transform_filter(selection_decade).transform_window(
    rank='rank(count)',
    sort=[alt.SortField('count', order='descending')]
).transform_filter(alt.datum.rank <= selection_count
                   ).properties(width=300, height=250, title="Top Genres by Number of Songs")

combined_chart = alt.hconcat(
    artist_chart,
    genre_chart
)

sliders = alt.Chart().mark_text().encode().add_params(
    selection_decade,
    selection_count
).properties(height=50)

final_chart = alt.vconcat(
    combined_chart,
    sliders
)

final_chart = final_chart.configure_concat(
    spacing=30
).configure_view(
    continuousWidth=350,
    continuousHeight=250,
    stroke=None
).configure_axis(
    labelFontSize=12,
    titleFontSize=14,
    labelPadding=30
).configure_legend(
    labelLimit=200,
    titleLimit=100
).configure(
    padding={"left": 100, "right": 100}
)

final_chart.save('../docs/ChartFiles/artist_genre_bargraphs.html')
