import pandas as pd
import altair as alt

# Load data
df = pd.read_csv('data.csv')

# Create 'decade' column
df['decade'] = (df['year'] // 10) * 10

# Group by decade and compute the mean for each feature
agg_df = df.groupby('decade').agg({
    'danceability': 'mean',
    'energy': 'mean',
    'instrumentalness': 'mean',
    'liveness': 'mean',
    'speechiness': 'mean',
    'acousticness': 'mean',
    'valence': 'mean'
}).reset_index()

# Rename columns for clarity
agg_df.rename(columns={
    'danceability': 'danceability_mean',
    'energy': 'energy_mean',
    'instrumentalness': 'instrumentalness_mean',
    'liveness': 'liveness_mean',
    'speechiness': 'speechiness_mean',
    'acousticness': 'acousticness_mean',
    'valence': 'valence_mean'
}, inplace=True)

# Filter for the desired features
selected_features = ['danceability_mean', 'energy_mean', 'instrumentalness_mean', 
                     'liveness_mean', 'speechiness_mean', 'acousticness_mean', 'valence_mean']

# Melt the dataframe
df_melted = agg_df.melt(id_vars='decade', value_vars=selected_features, 
                         var_name='feature', value_name='mean')

# Create multi-selection
selection = alt.selection_point(
    fields=['feature'],
    bind='legend',
    toggle=True  # Allow multi-selection
)

# Create the Altair chart
chart = alt.Chart(df_melted).mark_line(point=True).encode(
    x=alt.X('decade:O', title='Decade', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('mean:Q', title='Feature Value', scale=alt.Scale(domain=[0, 1])),
    color=alt.Color('feature:N', 
                    legend=alt.Legend(
                        title="Feature", 
                        labelExpr="replace(datum.label, '_mean', '')"
                    )),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1)),
    tooltip=[
        alt.Tooltip('decade:O', title='Decade'),
        alt.Tooltip('feature:N', title='Feature'),
        alt.Tooltip('mean:Q', title='Mean', format='.3f')
    ]
).properties(
    width=700,
    height=450,
    title='Average Song Characteristics Over Decades'
).add_params(
    selection)

# Save the chart to an HTML file
chart.save('chart.html')
