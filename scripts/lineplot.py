
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

# Melt the dataframe
df_melted = agg_df.melt(id_vars='decade', value_vars=agg_df.columns[1:], 
                       var_name='feature', value_name='mean')

# Multi-selection for features
feature_selection = alt.selection_point(
    fields=['feature'],
    bind='legend',
    toggle=True
)

# Toggle for regression lines
regression_toggle = alt.binding_checkbox(name='Show Regression Lines')
regression_selection = alt.param(value=False, bind=regression_toggle)

# Base line chart
line_chart = alt.Chart(df_melted).mark_line(point=True).encode(
    x=alt.X('decade:O', title='Decade', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('mean:Q', title='Feature Value', scale=alt.Scale(domain=[0, 1])),
    color=alt.Color('feature:N', 
                    legend=alt.Legend(
                        title="Feature", 
                        labelExpr="replace(datum.label, '_mean', '')"
                    )),
    opacity=alt.condition(feature_selection, alt.value(1), alt.value(0.1)),
    tooltip=[
        alt.Tooltip('decade:O', title='Decade'),
        alt.Tooltip('feature:N', title='Feature'),
        alt.Tooltip('mean:Q', title='Mean', format='.3f')
    ]
).add_params(feature_selection)

# Regression lines with toggle visibility
regression_chart = alt.Chart(df_melted).transform_regression(
    'decade', 'mean', groupby=['feature']
).mark_line(strokeDash=[5, 3]).encode(
    x=alt.X('decade:O'),
    y=alt.Y('mean:Q'),
    color=alt.Color('feature:N'),
    opacity=alt.condition(
        feature_selection & regression_selection,
        alt.value(1), 
        alt.value(0)
    )
)

# Combine charts
final_chart = (line_chart + regression_chart).add_params(
    regression_selection
).properties(
    width=700,
    height=450,
    title='Average Song Characteristics Over Decades with Regression Lines'
)

# Save the chart
final_chart.save('chart_with_regression.html')