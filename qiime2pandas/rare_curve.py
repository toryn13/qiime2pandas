import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  # For progress bar

def rarefaction_curve(otu_table, max_depth=None, num_iterations=10, seed=None):
    """
    Generate rarefaction curves for each sample in an OTU table.

    Parameters:
    otu_table (pd.DataFrame): The OTU table with OTUs as rows and samples as columns.
    max_depth (int): The maximum depth to rarefy each sample to. If None, use the minimum sample depth.
    num_iterations (int): The number of iterations to perform at each depth.
    seed (int): A random seed for reproducibility (optional).

    Returns:
    None: Displays a rarefaction plot.
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Determine the maximum depth if not specified
    if max_depth is None:
        max_depth = min(otu_table.sum(axis=0))
    
    depths = np.linspace(1, max_depth, 50, dtype=int)  # Generate depths from 1 to max_depth
    rarefaction_results = {depth: [] for depth in depths}

    # Iterate over each sample and generate rarefaction curves
    for sample in otu_table.columns:
        sample_data = otu_table[sample]
        sample_depth = sample_data.sum()
        
        if sample_depth < max_depth:
            print(f"Sample '{sample}' has fewer sequences ({sample_depth}) than the max depth ({max_depth}).")
            continue
        
        sample_rarefaction = []
        for depth in depths:
            otus_observed = []
            for _ in range(num_iterations):
                # Randomly subsample OTUs to the specified depth
                subsampled_otus = np.random.choice(sample_data.index, depth, p=sample_data/sample_depth, replace=True)
                otus_observed.append(len(set(subsampled_otus)))  # Count unique OTUs
            sample_rarefaction.append(np.mean(otus_observed))
        
        plt.plot(depths, sample_rarefaction)  # Removed label to avoid legend

    plt.xlabel('Sequencing Depth')
    plt.ylabel('Observed OTUs')
    plt.title('Rarefaction Curves')
    plt.grid(True)
    plt.show()

# Example usage:
# rarefaction_curve(otu_df, max_depth=1000, num_iterations=10, seed=42)
