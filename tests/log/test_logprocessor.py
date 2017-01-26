"""Test cases for log processor"""

import csv
import os
import pytest
from .mocklog import MockLog
from har.log.processor import create_dataset


@pytest.fixture
def log_files():
    """Create a dummy log files"""
    mocklog = MockLog((2, 10, 6))

    stand_log_info = ['TRAINING#STAND#HANDHELD', '2', '6', '10']
    stand_log_files = mocklog.mock_csv(stand_log_info, -10, 10)

    run_log_info = ['TRAINING#RUN#HANDHELD', '2', '6', '10']
    run_log_files = mocklog.mock_csv(run_log_info, -10, 10)

    files = stand_log_files + run_log_files

    yield files

    for log in files:
        os.remove(log)

def test_create_dataset(log_files):
    """Test dataset creation from dummy log file."""
    base_path = os.getcwd()
    output_path = os.path.join(base_path, 'dataset.csv')
    create_dataset(log_files, output_path)

    metadata = None
    data = None

    with open(output_path, newline='') as f:
        reader = csv.reader(f)
        metadata = next(reader)
        data = next(reader)

    assert metadata[0] == '40'
    assert int(metadata[1]) == 6
    assert len(data) == 7

    os.remove(output_path)
