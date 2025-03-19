import plotly.graph_objects as go
import pandas as pd

def _code_mapping(df, src, targ):
    '''
    Helper function used by make sankey to create labels
    '''
    labels = list(set(df[src]).union(set(df[targ])))
    codes = list(range(len(labels)))
    lc_map = dict(zip(labels, codes))
    df = df.replace({src:lc_map, targ:lc_map})
    return df, labels

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
    :param color: Column to base color intensity on (optional)
    :return: A new dataframe where labels have been encoded + list of labels
    """
    stacked_df = df_stacking(df, cols, vals)
    df_mapped, labels = _code_mapping(stacked_df, 'src', 'targ')

    link = {
        'source': df_mapped['src'], 
        'target': df_mapped['targ'], 
        'value': df_mapped['value'],
    }

    node = {
        'label': labels,
        'pad': 20,
        'thickness': 15,
    }

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.update_layout(
        title="Sankey Diagram of Top Artists by Decade and Genre",
        font=dict(size=12)
    )
    fig.show()