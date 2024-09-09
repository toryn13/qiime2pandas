import pandas as pd

def parse_sintax(sintax_file, otu_table_file, output_file=None):
    """
    Parses a SINTAX output file to extract the OTU ID and the final assigned taxonomy levels.
    The function removes prefixes (e.g., d:, p:, etc.) and organizes the taxonomy
    into separate columns (kingdom, phylum, class, order, family, genus). It then merges the
    parsed taxonomy data with an OTU table. Optionally, it saves the result to a text file.

    Parameters:
    sintax_file (str): Path to the SINTAX output file (in .txt format).
    otu_table_file (str): Path to the OTU table file (in .txt or .csv format).
    output_file (str): Path to save the merged data (optional).

    Returns:
    pd.DataFrame: A DataFrame with merged OTU table and taxonomy data.
    """
    # Import the SINTAX file with the relevant columns
    taxa_df = pd.read_csv(sintax_file, sep='\t', header=None, names=['OTU', 'TaxonomyDetails'], usecols=[0, 3])

    # Split the TaxonomyDetails column into separate columns for each taxonomic level
    taxa_split = (
        taxa_df['TaxonomyDetails']
        .str.split(',', expand=True)
        .apply(lambda col: col.str.split(':').str[1] if col.str.contains(':').any() else col)
    )

    # Ensure there are exactly 6 columns by filling missing values with empty strings
    taxa_split = taxa_split.reindex(columns=range(6)).fillna('')

    # Rename the columns to match the taxonomic levels
    taxa_split.columns = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']

    # Combine OTU with the split taxonomy data
    taxa_df = pd.concat([taxa_df['OTU'], taxa_split], axis=1)

    # Load the OTU table
    otu_df = pd.read_csv(otu_table_file, sep='\t')

    # Identify the OTU ID column in the OTU table
    possible_otu_columns = ['#OTU ID', 'OTU', 'OTU_ID']
    otu_column = next((col for col in possible_otu_columns if col in otu_df.columns), None)

    if otu_column is None:
        raise ValueError("No recognized OTU ID column found in OTU table.")

    # Rename the OTU column to 'OTU' to match the SINTAX DataFrame
    otu_df = otu_df.rename(columns={otu_column: 'OTU'})

    # Merge the OTU table with the parsed taxonomy data
    merged_df = pd.merge(otu_df, taxa_df, on='OTU', how='left')

    # Calculate relative abundances only for numeric columns
    numeric_columns = merged_df.select_dtypes(include=['number']).columns
    rel_table = merged_df[['OTU']].copy()  # Start with the OTU column
    rel_table[numeric_columns] = merged_df[numeric_columns].div(merged_df[numeric_columns].sum()) * 100

    # Combine the relative abundance table back with the taxonomy data
    merged_rel_df = pd.merge(taxa_df, rel_table, on='OTU', how='left')

    # Optionally save the final DataFrame to a text file
    if output_file:
        merged_rel_df.to_csv(output_file, sep='\t', index=False)

    return merged_rel_df

# Example usage:
# merged_rel_df = parse_sintax('sintax2.txt', 'otutab.sorted.txt', 'merged_output.txt')
# print(merged_rel_df.head())