import os
import pandas as pd
from qiime2pandas.process_stats_files import process_stats_files

def test_process_stats_files(tmpdir):
    # Set up test files in the temporary directory
    test_data = """58121 reads, max len 458, avg 425.6
Length         MaxEE 0.50         MaxEE 1.00         MaxEE 2.00
------   ----------------   ----------------   ----------------
    50      56620( 97.4%)      57815( 99.5%)      58102(100.0%)
   100      53826( 92.6%)      56417( 97.1%)      57797( 99.4%)
   150      49974( 86.0%)      54244( 93.3%)      56931( 98.0%)
   200      43199( 74.3%)      50789( 87.4%)      55233( 95.0%)
   250      37542( 64.6%)      47467( 81.7%)      53510( 92.1%)
   300      34300( 59.0%)      45133( 77.7%)      51828( 89.2%)
   350      32367( 55.7%)      44005( 75.7%)      50940( 87.6%)
   400      29992( 51.6%)      43200( 74.3%)      50384( 86.7%)
   450          3(  0.0%)          3(  0.0%)          4(  0.0%)
"""
    # Create an example .stats file
    stats_file = tmpdir.join("example.stats")
    stats_file.write(test_data)

    # Run the function and test the output
    maxEE_summary = process_stats_files(tmpdir, 'MaxEE1')
    assert isinstance(maxEE_summary, pd.DataFrame)
    assert 'Length' in maxEE_summary.columns
    assert 'MaxEE1' in maxEE_summary.columns

    # Check some values to ensure correctness
    assert maxEE_summary.iloc[0]['Length'] == 50
    assert maxEE_summary.iloc[0]['MaxEE1'] == 57815

    # Check that the CSV was created
    assert os.path.exists(tmpdir.join("maxEE_summary.csv"))

