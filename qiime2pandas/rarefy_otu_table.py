import pandas as pd
import numpy as np

def rarefy_otu_table(otu_table, depth, seed=None):
    """
    Perform rarefaction on an OTU table to a specified sequencing depth.

    Parameters:
    otu_table (pd.DataFrame): The OTU table with OTUs as rows and samples as columns.
    depth (int): The depth to rarefy each sample to.
    seed (int): A random seed for reproducibility (optional).

    Returns:
    pd.DataFrame: A rarefied OTU table.
    dict: A dictionary with the number of OTUs lost for each sample.
    """
    if seed is not None:
        np.random.seed(seed)
    
    rarefied_data = []
    otus_lost = {}  # Dictionary to store the number of OTUs lost per sample

    # Iterate over each sample (column)
    for sample in otu_table.columns:
        sample_data = otu_table[sample]

        if sample_data.sum() < depth:
            raise ValueError(f"Sample '{sample}' has less reads ({sample_data.sum()}) than the rarefaction depth ({depth}).")

        # Repeat the OTU IDs according to their counts
        repeated_otus = np.repeat(sample_data.index, sample_data.values)

        # Randomly subsample the repeated OTUs to the desired depth
        subsampled_otus = np.random.choice(repeated_otus, depth, replace=False)

        # Count the occurrences of each OTU in the subsampled data
        subsampled_counts = pd.Series(subsampled_otus).value_counts()

        # Create a new series with the full OTU set and fill missing OTUs with 0
        rarefied_sample = pd.Series(0, index=otu_table.index)
        rarefied_sample[subsampled_counts.index] = subsampled_counts

        # Count how many OTUs were lost (i.e., OTUs that were non-zero before but are zero after rarefaction)
        otus_lost[sample] = (sample_data > 0).sum() - (rarefied_sample > 0).sum()

        rarefied_data.append(rarefied_sample)

    # Combine the rarefied samples into a DataFrame
    rarefied_otu_table = pd.DataFrame(rarefied_data).T
    rarefied_otu_table.columns = otu_table.columns
    print(otus_lost)
    return rarefied_otu_table, otus_lost

# Example usage:
# Assume `otu_df` is a DataFrame where rows are OTUs and columns are samples.
# rarefied_otu_df, otus_lost = rarefy_otu_table(otu_df, depth=1000, seed=42)
# print(rarefied_otu_df)
# print(otus_lost)
