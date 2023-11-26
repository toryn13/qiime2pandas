import os
import shutil
import zipfile
import tempfile

def unzip_qza_files(qza_file_paths):
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

            # Iterate through the extracted directories and copy all suitable files
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    if file_name.lower().endswith(('.csv', '.tsv', '.txt', 'biom', 'nwk', 'fasta')) and not file_name.startswith('.'):
                        source_file = os.path.join(root, file_name)
                        destination_file = os.path.join(output_folder, file_name)
                        shutil.copy(source_file, destination_file)

            # Clean up the temporary directory and its contents
            shutil.rmtree(temp_dir)

            print(f"Unzipped and copied files from {os.path.basename(qza_file_path)} into folder: {folder_name}")
        except Exception as e:
            print(f"An error occurred while processing {qza_file_path}: {e}")

# Example usage:
# qza_file_paths = ['file1.qza', 'file2.qza']
# unzip_qza_files(qza_file_paths)

