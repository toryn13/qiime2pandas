import pandas as pd

def parse_sintax(sintax_file, output_file=None):
    """
    Parses a SINTAX output file and extracts the classification levels from kingdom to genus.
    The function removes confidence scores and prefixes (d:, p:, c:, etc.) and returns
    a Pandas DataFrame. Optionally, it saves the result to a text file.

    Parameters:
    sintax_file (str): Path to the SINTAX output file (in .txt format).
    output_file (str): Path to save the parsed taxonomy data (optional).

    Returns:
    pd.DataFrame: A DataFrame with columns for OTU ID and taxonomy levels from kingdom to genus.
    """
    classification_levels = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']

    taxonomy_data = []

    with open(sintax_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            otu_id = parts[0]
            taxonomy_string = parts[1]
            
            # Split the taxonomy string by commas and process each level
            taxonomy_levels = taxonomy_string.split(',')
            parsed_levels = {}
            
            for level in taxonomy_levels:
                # Split by ':' to separate the prefix (d:, p:, etc.) and the actual classification
                prefix, classification = level.split(':', 1)
                # Remove any confidence scores in parentheses
                classification = classification.split('(')[0]
                
                # Map the prefix to the corresponding classification level
                if prefix == 'd':
                    parsed_levels['kingdom'] = classification
                elif prefix == 'p':
                    parsed_levels['phylum'] = classification
                elif prefix == 'c':
                    parsed_levels['class'] = classification
                elif prefix == 'o':
                    parsed_levels['order'] = classification
                elif prefix == 'f':
                    parsed_levels['family'] = classification
                elif prefix == 'g':
                    parsed_levels['genus'] = classification

            # Ensure all levels are present, filling with empty strings if necessary
            parsed_taxonomy = {level: parsed_levels.get(level, '') for level in classification_levels}
            parsed_taxonomy['OTU ID'] = otu_id
            
            taxonomy_data.append(parsed_taxonomy)

    # Convert the list of dictionaries into a DataFrame
    taxonomy_df = pd.DataFrame(taxonomy_data, columns=['OTU ID'] + classification_levels)

    # Optionally save the DataFrame to a text file
    if output_file:
        taxonomy_df.to_csv(output_file, sep='\t', index=False)

    return taxonomy_df

# Example usage:
# parsed_df = parse_sintax('sintax_output.txt', 'parsed_taxonomy.txt')
# print(parsed_df.head())
