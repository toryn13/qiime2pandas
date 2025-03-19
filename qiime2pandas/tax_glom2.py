import pandas as pd

def tax_glom_table(df, taxonomic_level, sample_indices=None):
    """
    Aggregate taxonomic information at the specified taxonomic level, summing only sample columns selected by index.

    Parameters:
    - df: DataFrame
        The DataFrame containing taxonomic and sample abundance information.
    - taxonomic_level: str
        The taxonomic level to aggregate at (e.g., "Phylum").
    - sample_indices: list of int, optional (default=None)
        The indices of the columns corresponding to the samples to aggregate.

    Returns:
    - DataFrame
        A new DataFrame with aggregated taxonomic information.
    """
    # Check if the specified taxonomic level is present in the DataFrame
    if taxonomic_level not in df.columns:
        raise ValueError(f"Taxonomic level '{taxonomic_level}' not found in DataFrame.")
    
    # Select sample columns by index if specified
    if sample_indices is not None:
        sample_cols = df.columns[sample_indices].tolist()
    else:
        raise ValueError("Please provide sample indices for column selection.")
    
    # Ensure there are sample columns to aggregate
    if not sample_cols:
        raise ValueError("No sample columns found with the provided indices.")

    # Keep only the taxonomic level and the selected sample columns
    df_filtered = df[[taxonomic_level] + sample_cols]

    # Group by the specified taxonomic level and sum the sample abundances
    grouped_df = df_filtered.groupby(taxonomic_level, as_index=False).sum()

    return grouped_df

# Example usage:
# Use tax_glom to aggregate at the 'Phylum' level, summing columns with indices 1 to 10
# result = tax_glom_table(df, "Phylum", sample_indices=range(1, 11))

