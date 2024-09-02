import pandas as pd
import os

def extract_summary_stats(directory, output_csv='summary_stats.csv'):
    """
    Extracts the summary statistics (reads, max length, avg length) from the first line of each .stats file.

    Parameters:
    directory (str): The path to the directory containing .stats files.
    output_csv (str): The name of the output CSV file (default is 'summary_stats.csv').

    Returns:
    pd.DataFrame: A DataFrame with 'File', 'Reads', 'Max Length', and 'Avg Length' columns.
    """

    # Initialize an empty list to collect the summary data
    summaries = []

    # Iterate over all files in the directory with a .stats extension
    for filename in os.listdir(directory):
        if filename.endswith('.stats'):
            filepath = os.path.join(directory, filename)

            with open(filepath, 'r') as file:
                first_line = file.readline().strip()

            
            parts = first_line.split(',')
            reads = int(parts[0].split()[0])
            max_len = int(parts[1].split()[-1])
            avg_len = float(parts[2].split()[-1])

            # Append the data to the list
            summaries.append({
                'File': filename,
                'Reads': reads,
                'Max Length': max_len,
                'Average Length': avg_len
            })

    summary_df = pd.DataFrame(summaries)

    # Save the DataFrame as a CSV file
    output_path = os.path.join(directory, output_csv)
    summary_df.to_csv(output_path, index=False)

    return summary_df
#extract_summary_stats('/content')