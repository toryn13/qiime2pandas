import pandas as pd
import os

def process_stats_files(directory, maxEE_level, output_csv='maxEE_summary.csv'):
    """
    Processes all .stats files in the specified directory and returns a DataFrame
    with 'Length' and the selected MaxEE level for each file. The DataFrame is also
    saved as a CSV file.

    Parameters:
    directory (str): The path to the directory containing .stats files.
    maxEE_level (str): The MaxEE level to select ('MaxEE0.5', 'MaxEE1', 'MaxEE2').
    output_csv (str): The name of the output CSV file (default is 'maxEE_summary.csv').

    Returns:
    pd.DataFrame: A DataFrame with 'Length' and the selected MaxEE level for each file.
    """

    # Mapping of MaxEE levels to column indices in the original data
    maxEE_map = {
        'MaxEE0.5': 1,  # Column 2 in the original file
        'MaxEE1': 3,    # Column 4 in the original file
        'MaxEE2': 5     # Column 6 in the original file
    }

    if maxEE_level not in maxEE_map:
        raise ValueError(f"Invalid MaxEE level: {maxEE_level}. Choose from 'MaxEE0.5', 'MaxEE1', or 'MaxEE2'.")

    # Initialize an empty list to collect DataFrames
    dfs = []

    # Iterate over all files in the directory with a .stats extension
    for filename in os.listdir(directory):
        if filename.endswith('.stats'):
            filepath = os.path.join(directory, filename)

         
            with open(filepath, 'r') as file:
                lines = file.readlines()

            
            data_lines = lines[4:]  # Extract the data lines (skip header and separator)

            # Prepare the data for the DataFrame
            data = []
            for line in data_lines:
                
                parts = line.strip().split()

                
                selected_parts = [
                    parts[0],  # Length
                    parts[maxEE_map[maxEE_level]].split('(')[0]  # Selected MaxEE level
                ]

                data.append(selected_parts)

            
            df = pd.DataFrame(data, columns=['Length', maxEE_level])

            
            df = df.apply(pd.to_numeric, errors='ignore')

            
            df['File'] = filename

           
            dfs.append(df)

   
    maxEE_summary = pd.concat(dfs, ignore_index=True)

    
    output_path = os.path.join(directory, output_csv)
    maxEE_summary.to_csv(output_path, index=False)

    return maxEE_summary

#Example useage
#maxEE_summary = process_stats_files('/content/', 'MaxEE1')