import pandas as pd

#taken from phyloseq, tax_glom, could be wrong

def tax_glom(df, taxonomic_level):
    """
    Aggregate taxonomic information at the specified taxonomic level.

    Parameters:
    - df: DataFrame
        The DataFrame containing taxonomic information.
    - taxonomic_level: str
        The taxonomic level to aggregate at (e.g., "Phylum").

    Returns:
    - DataFrame
        A new DataFrame with aggregated taxonomic information.
    """
    # Check if the specified taxonomic level is present in the DataFrame
    if taxonomic_level not in df.columns:
        raise ValueError(f"Taxonomic level '{taxonomic_level}' not found in DataFrame.")

    # Group by the specified taxonomic level and sum the abundances
    grouped_df = df.groupby(taxonomic_level).sum().reset_index()

    return grouped_df
