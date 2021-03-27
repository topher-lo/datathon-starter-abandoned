"""Unit tests for running and querying Prefect flow runs from the Streamlit app.
"""

import shutil
import pandas as pd
import numpy as np

from client.app import create_prefect_flow_run
from server.utils import make_path

from pandas.testing import assert_frame_equal


def test_create_prefect_flow_run(tmp_data_directory):
    flow_name = 'wrangle_na_pipeline'
    project_name = 'streamlit-e2e-boilerplate'
    task_refs = ['wrangle_na']
    # Create fake CSV in tmp ir
    tmpdir = tmp_data_directory
    make_path(tmpdir)
    data = pd.DataFrame({
        'x1': [1, 0, 1, 1],
        'x2': [3, np.nan, 1, 2],
        'x3': ['A', 'B', 'C', 'A']
    })
    file_path = f'{tmpdir}/test.csv'
    data.to_csv(file_path)
    # Test function
    params = {'url': file_path,
              'sep': ',',
              'strategy': 'cc'}
    result, state = create_prefect_flow_run(flow_name,
                                            project_name,
                                            task_refs,
                                            params)
    expected = pd.DataFrame({
        'x1': [1, 0, 1, 1],
        'x2': [3, np.nan, 1, 2],
        'x3': ['A', 'B', 'C', 'A']
    }).dropna()
    # Delete tmpdir if smoke test succeeds
    shutil.rmtree(str(tmpdir))
    # Assertions
    assert state.is_successful()
    assert_frame_equal(result['wrangle_na'], expected)
