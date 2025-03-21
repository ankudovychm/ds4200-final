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

def make_sankey(df, cols, vals=None):
    """
    A wrapper function to create a Sankey diagram from a dataframe and an arbitrary list of columns.

    :param df: Input dataframe with aggregated columns
    :param cols: List of column names which define the layers of the plot
    :param vals: column name for values used in plot (optional)
    :return: A new dataframe where labels have been encoded + list of labels
    """

    stacked_df = df_stacking(df, cols, vals)
    df_mapped, labels, lc_map = _code_mapping(stacked_df, 'src', 'targ')

    # Compute the total node value
    node_values = pd.concat([df_mapped[['src', 'value']], df_mapped[['targ', 'value']].rename(columns={'targ': 'src'})])
    node_counts = node_values.groupby('src')['value'].sum()

    # Ensure all nodes are accounted for
    all_nodes = range(len(labels))
    node_counts = node_counts.reindex(all_nodes, fill_value=0)

    # Normalize values with contrast control
    min_count, max_count = node_counts.min(), node_counts.max()
    if max_count > min_count:  # Avoid division by zero
        contrast_factor = 0.5  # Adjust this between 0.3 - 0.7 for best results
        normalized_counts = ((node_counts - min_count) / (max_count - min_count)) ** contrast_factor
    else:
        normalized_counts = np.zeros(len(node_counts))  # Handle edge case

    # Generate grayscale colors (darker for higher values)
    colors = [plt.cm.Greys(norm_val) for norm_val in normalized_counts]
    rgba_colors = [f'rgba({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)}, 1)' for c in colors]

    link = {
        'source': df_mapped['src'], 
        'target': df_mapped['targ'], 
        'value': df_mapped['value'],
    }

    node = {
        'label': labels,
        'pad': 20,
        'thickness': 15,
        'color': rgba_colors  # Ensures all nodes get a valid color
    }

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.update_layout(
        title="Sankey Diagram of Top Artists by Decade and Genre",
        font=dict(size=12)
    )
    fig.write_html("sankey.html")