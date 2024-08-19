import os
import shutil
import zipfile
import tempfile
import pandas as pd
import subprocess
import logging

def import_and_merge(qza_file_paths):
    logging.basicConfig(level=logging.INFO)
    merged_tables = []

    for qza_file_path in qza_file_paths:
        try:
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(qza_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            folder_name = os.path.splitext(os.path.basename(qza_file_path))[0]
            output_folder = os.path.join(os.getcwd(), folder_name)
            os.makedirs(output_folder, exist_ok=True)

            tax_table_folder = os.path.join(os.getcwd(), 'tax_table')
            os.makedirs(tax_table_folder, exist_ok=True)

            # Move files only if they exist
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    source_file = os.path.join(root, file_name)
                    if os.path.exists(source_file):
                        destination_file = os.path.join(tax_table_folder, file_name)
                        shutil.move(source_file, destination_file)

            biom_file_path = os.path.join(tax_table_folder, 'feature-table.biom')
            if os.path.exists(biom_file_path):
                txt_file_path = os.path.join(tax_table_folder, 'rare_table.txt')
                subprocess.run(['biom', 'convert', '-i', biom_file_path, '-o', txt_file_path, '--to-tsv'], check=True)
                logging.info(f"Converted biom file to text file for {os.path.basename(qza_file_path)} into folder: {tax_table_folder}")
            else:
                logging.warning(f"The biom file '{biom_file_path}' does not exist. Skipping conversion for {qza_file_path}.")
                continue  # Skip this iteration if the biom file is missing

            taxonomy_path = os.path.join(tax_table_folder, 'taxonomy.tsv')
            taxa = pd.read_table(taxonomy_path, index_col=0)
            taxa[['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']] = taxa['Taxon'].str.split(';', expand=True)

            rare_table_path = os.path.join(tax_table_folder, 'rare_table.txt')
            rare_table = pd.read_table(rare_table_path, skiprows=1, index_col=0)

            merged_table = rare_table.join(taxa[['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']])
            merged_tables.append(merged_table)

            logging.info(f"Imported and merged taxonomy and rare table for {os.path.basename(qza_file_path)} into folder: {tax_table_folder}")

            csv_file_path = os.path.join(tax_table_folder, 'merged_table.csv')
            merged_table.to_csv(csv_file_path, index=True)

            logging.info(f"Saved merged_table as CSV for {os.path.basename(qza_file_path)} into folder: {tax_table_folder}")

            shutil.rmtree(temp_dir)

        except Exception as e:
            logging.error(f"An error occurred while processing {qza_file_path}: {e}")

    return merged_tables

# Example usage:
# qza_file_paths = ['/content/taxonomy.qza', '/content/core-metrics-results/rarefied_table.qza']
# merged_tables = import_and_merge(qza_file_paths)

