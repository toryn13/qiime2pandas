import os
import pandas as pd
from qiime2pandas.process_stats_files import process_stats_files

def test_process_stats_files(tmpdir):
    # Get the path to the example.stats file
    test_file_path = os.path.join(os.path.dirname(__file__), 'test_files', 'example.stats')

    # Copy the example .stats file to the temporary directory (tmpdir)
    tmpdir_path = tmpdir.mkdir("testdata")
    test_file_copy = tmpdir_path.join("data.stats")
    test_file_copy.write(open(test_file_path).read())

        maxEE_summary = process_stats_files(tmpdir_path, 'MaxEE1')


    print(maxEE_summary)

    assert isinstance(maxEE_summary, pd.DataFrame)
    assert 'Length' in maxEE_summary.columns
    assert 'MaxEE1' in maxEE_summary.columns

    # Check some values to ensure correctness
    assert maxEE_summary.iloc[0]['Length'] == 50
    assert maxEE_summary.iloc[0]['MaxEE1'] == 57815

    # Check that the CSV was created
    assert os.path.exists(tmpdir_path.join("maxEE_summary.csv"))
