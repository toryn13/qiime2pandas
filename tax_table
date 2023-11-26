import os
import shutil
import zipfile
import tempfile
import pandas as pd
import subprocess

def import_and_merge(qza_file_paths):
    merged_tables = []  # To store merged tables for each QZA file
    for qza_file_path in qza_file_paths:
        try:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()

            # Unzip the .qza file directly into the temporary directory
            with zipfile.ZipFile(qza_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Create a folder with the same name as the original QZA file
            folder_name = os.path.splitext(os.path.basename(qza_file_path))[0]
            output_folder = os.path.join(os.getcwd(), folder_name)
            os.makedirs(output_folder, exist_ok=True)

            # Create a folder named 'tax_table' in the root directory
            tax_table_folder = os.path.join(os.getcwd(), 'tax_table')
            os.makedirs(tax_table_folder, exist_ok=True)

            # Move taxonomy.tsv and feature-table.biom to the 'tax_table' folder
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    source_file = os.path.join(root, file_name)
                    destination_file = os.path.join(tax_table_folder, file_name)
                    shutil.move(source_file, destination_file)

            # Check if the biom file exists in the 'tax_table' folder
            biom_file_path = os.path.join(tax_table_folder, 'feature-table.biom')
            if not os.path.exists(biom_file_path):
                raise FileNotFoundError(f"The biom file '{biom_file_path}' does not exist.")

            # Convert biom file to text file
            txt_file_path = os.path.join(tax_table_folder, 'rare_table.txt')
            subprocess.run(['biom', 'convert', '-i', biom_file_path, '-o', txt_file_path, '--to-tsv'], check=True)

            print(f"Converted biom file to text file for {os.path.basename(qza_file_path)} into folder: {tax_table_folder}")

            # Import taxonomy information
            taxonomy_path = os.path.join(tax_table_folder, 'taxonomy.tsv')
            taxa = pd.read_table(taxonomy_path, index_col=0)
            taxa[['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']] = taxa['Taxon'].str.split(';', expand=True)

            # Import the rare table
            rare_table_path = os.path.join(tax_table_folder, 'rare_table.txt')
            rare_table = pd.read_table(rare_table_path, skiprows=1, index_col=0)

            # Merge taxonomy and rare table
            merged_table = rare_table.join(taxa[['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']])
            merged_tables.append(merged_table)

            print(f"Imported and merged taxonomy and rare table for {os.path.basename(qza_file_path)} into folder: {tax_table_folder}")

            # Save merged_table as CSV
            csv_file_path = os.path.join(tax_table_folder, 'merged_table.csv')
            merged_table.to_csv(csv_file_path, index=True)

            print(f"Saved merged_table as CSV for {os.path.basename(qza_file_path)} into folder: {tax_table_folder}")

            # Clean up the temporary directory
            shutil.rmtree(temp_dir)

        except Exception as e:
            print(f"An error occurred while processing {qza_file_path}: {e}")

    return merged_tables

# Example usage:
# qza_file_paths = ['/content/taxonomy.qza', '/content/core-metrics-results/rarefied_table.qza']
# merged_tables = import_and_merge(qza_file_paths)
