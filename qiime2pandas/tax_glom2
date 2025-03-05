import pandas as pd

def tax_glom_table(df, taxonomic_level, sample_prefix="s"):
    """
    Aggregate taxonomic information at the specified taxonomic level, summing only sample columns.

    Parameters:
    - df: DataFrame
        The DataFrame containing taxonomic and sample abundance information.
    - taxonomic_level: str
        The taxonomic level to aggregate at (e.g., "Phylum").
    - sample_prefix: str, optional (default="s")
        The prefix that identifies sample columns.

    Returns:
    - DataFrame
        A new DataFrame with aggregated taxonomic information.
    """
    # Check if the specified taxonomic level is present in the DataFrame
    if taxonomic_level not in df.columns:
        raise ValueError(f"Taxonomic level '{taxonomic_level}' not found in DataFrame.")

    # Select only the taxonomic column and sample columns (starting with sample_prefix)
    sample_cols = [col for col in df.columns if col.startswith(sample_prefix)]
    
    # Ensure there are sample columns to aggregate
    if not sample_cols:
        raise ValueError(f"No sample columns found with prefix '{sample_prefix}'.")

    # Keep only the taxonomic level and the sample columns
    df_filtered = df[[taxonomic_level] + sample_cols]

    # Group by the specified taxonomic level and sum the sample abundances
    grouped_df = df_filtered.groupby(taxonomic_level, as_index=False).sum()

    return grouped_df
#example use
#Use tax_glom to aggregate at the 'phylum' level, summing columns starting with 's'
#result = tax_glom(df, "phylum", sample_prefix="s")
