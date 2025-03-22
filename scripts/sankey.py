import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def _code_mapping(df, src, targ):
    '''
    Helper function used by make_sankey to create labels
    '''
    # Ensure decades are ordered explicitly
    labels = list(set(df[src]).union(set(df[targ])))
    codes = list(range(len(labels)))
    lc_map = dict(zip(labels, codes))
    df = df.replace({src: lc_map, targ: lc_map})
    return df, labels, lc_map

def df_stacking(df, cols, vals=None):
    '''
    Helper function used by make sankey to stack dataframes for a multi-layered chart
    '''
    df_pairs = []
    for i in range(len(cols) - 1):
        if vals:
            df_pair = df.groupby([cols[i], cols[i + 1]])[vals].sum().reset_index()
        else:
            df_pair = df.groupby([cols[i], cols[i + 1]]).apply(lambda x: pd.Series({'value': 1})).reset_index()

        df_pair.columns = ['src', 'targ', 'value']
        df_pairs.append(df_pair)

    stacked = pd.concat(df_pairs, axis=0)
    return stacked

import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def make_sankey(df, cols, vals=None, popularity_cols=None):
    """
    Create a Sankey diagram with multiple average popularity features.

    :param df: Input dataframe with aggregated columns
    :param cols: List of column names defining the layers of the plot
    :param vals: Column name for values used in the plot (e.g., count)
    :param popularity_cols: List of columns for popularity (artists, decades, genres)
    """
    stacked_df = df_stacking(df, cols, vals)
    df_mapped, labels, lc_map = _code_mapping(stacked_df, 'src', 'targ')

    # Compute node values
    node_values = pd.concat([df_mapped[['src', 'value']], df_mapped[['targ', 'value']].rename(columns={'targ': 'src'})])
    node_counts = node_values.groupby('src')['value'].sum()

    # Handle missing nodes
    all_nodes = range(len(labels))
    node_counts = node_counts.reindex(all_nodes, fill_value=0)

    # Get popularity for each type of node
    pop_maps = {
    'avg_popularity': df.groupby("artists")["avg_popularity"].mean().to_dict(),
    'avg_popularity_decade': df.groupby("decade")["avg_popularity_decade"].mean().to_dict(),
    'avg_popularity_genre': df.groupby("genres")["avg_popularity_genre"].mean().to_dict()
    }

    # Assign popularity values to nodes
    node_popularity = []
    for label in labels:
        if label in pop_maps['avg_popularity']:  # Artists
            node_popularity.append(pop_maps['avg_popularity'].get(label, 0))
        elif label in pop_maps['avg_popularity_decade']:  # Decades
            node_popularity.append(pop_maps['avg_popularity_decade'].get(label, 0))
        elif label in pop_maps['avg_popularity_genre']:  # Genres
            node_popularity.append(pop_maps['avg_popularity_genre'].get(label, 0))
        else:
            node_popularity.append(0)  # Default to 0 if not found

    # Normalize popularity values for coloring
    min_pop, max_pop = min(node_popularity), max(node_popularity)
    if max_pop > min_pop:
        norm_popularity = [(p - min_pop) / (max_pop - min_pop) for p in node_popularity]
    else:
        norm_popularity = [0] * len(node_popularity)

    # Define colormaps for different node types
    artist_cmap = plt.cm.Blues
    decade_cmap = plt.cm.Oranges
    genre_cmap = plt.cm.Greens

    # Assign appropriate color based on label type
    rgba_colors = []
    for label, norm in zip(labels, norm_popularity):
        if label in pop_maps['avg_popularity']:  # Artists
            c = artist_cmap(norm)
        elif label in pop_maps['avg_popularity_decade']:  # Decades
            c = decade_cmap(norm)
        elif label in pop_maps['avg_popularity_genre']:  # Genres
            c = genre_cmap(norm)

        rgba_colors.append(f'rgba({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)}, 1)')

    link = {
        'source': df_mapped['src'], 
        'target': df_mapped['targ'], 
        'value': df_mapped['value'],
    }

    node = {
        'label': labels,
        'pad': 20,
        'thickness': 15,
        'color': rgba_colors  # Nodes colored by popularity type
    }

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.update_layout(
        title="Sankey Diagram of Artists, Genres, and Decades (Colored by Popularity)",
        font=dict(size=12)
    )
    fig.write_html("sankey.html")