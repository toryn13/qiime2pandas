import os
import glob

def rename_fastq_files(directory: str) -> None:
    """
    Renames FASTQ files in the specified directory by removing hyphens from their filenames.

    Parameters:
    - directory (str): The path to the directory containing the FASTQ files.

    Example:
    rename_fastq_files("/content/20240708_HRickard_EMP16S/")
    """

    # Define the pattern to match the FASTQ files
    pattern = os.path.join(directory, "*_S*_L001_R*_001.fastq.gz")

    # Loop through the matched files
    for file in glob.glob(pattern):
        # Get the base name of the file
        base = os.path.basename(file)

        # Remove '-' from the base name
        new_base = base.replace('-', '')

        # Construct the new file path
        new_file = os.path.join(directory, new_base)

        # Rename the file
        os.rename(file, new_file)

        print(f"Renamed {base} to {new_base}")

# Example usage:
# rename_fastq_files("/content/fastq_files/")