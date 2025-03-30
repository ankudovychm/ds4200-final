import pandas as pd
import os


def check_full(df_path):
    # Load DataFrame
    df = pd.read_csv(df_path)

    # Count missing (NaN) values per column
    nan_counts = df.isna().sum()

    # Count empty string values per column
    empty_counts = (df == "").sum()

    # Combine results into a single DataFrame and print
    missing_summary = pd.DataFrame({
        "NaN Count": nan_counts,
        "Empty String Count": empty_counts,
        "Total Missing": nan_counts + empty_counts
    })

    print(missing_summary)

def find_near_duplicates(df):
    """
    Identify rows where all columns except 'id' are identical.
    """
    # Exclude 'id' column from comparison
    comparison_cols = [col for col in df.columns if col != 'id']

    # Count unique IDs for each group
    grouped = df.groupby(comparison_cols)['id'].nunique()

    # Find cases where multiple unique IDs exist
    duplicates = grouped[grouped > 1].reset_index()

    # Merge back to get the full row details
    result = df.merge(duplicates, on=comparison_cols, how='inner')

    return result

def find_year_differences(df):

    # Exclude 'id', 'year', 'popularity', and 'release_date' columns from comparison
    comparison_cols = [col for col in df.columns if col not in ['id', 'year', 'popularity', 'release_date']]

    # Group by the relevant columns and count unique 'year' and 'id'
    grouped = df.groupby(comparison_cols).agg(
        unique_years=('year', 'nunique'),
        unique_ids=('id', 'nunique')
    )

    # Find cases where multiple unique years exist
    duplicates = grouped[grouped['unique_years'] > 1].reset_index()

    # Merge back to get the full row details
    result = df.merge(duplicates, on=comparison_cols, how='inner')

    return result


data_folder = os.path.join(os.path.dirname(__file__))
# List all CSV files in the Data folder
files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

"""
for i in files:
    print(i)
    check_full(i)
    print("")
    print("")


# Duplicate Songs where everythign is the same but track ID 
df = pd.read_csv("data.csv")  # Load your dataset
near_duplicates_df = find_near_duplicates(df)
# Print
print(near_duplicates_df)


print("")
print("Songs Released in different years")
print(find_year_differences(df))
"""

df = pd.read_csv("data.csv")
print(len(df["name"]), "songs")

print(len(df["name"]), "songs")
