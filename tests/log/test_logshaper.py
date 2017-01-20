import os
import pytest

from .mocklog import MockLog
from har.log import LogShaper, LogReader


class TestLogShaper:

    @pytest.fixture
    def setup(self):
        mock = MockLog((1, 100, 6))
        log_info = ['TRAINING', '2']
        csv_file = mock.mock_csv(log_info, -10, 10)
        reader = LogReader(csv_file)
        data = reader.read()[1]
        self.shaper = LogShaper(data)

        os.remove(csv_file)

    def test_sliding_window(self, setup):
        data = self.shaper.sliding_window(10, 5)

        assert data.shape[0] == 19
        assert data.shape[1] == 60

    def test_split(self, setup):
        data = self.shaper.split(2)

        assert len(data) == 2
        assert data[0].shape[0] == 100
        assert data[0].shape[1] == 3
        assert data[1].shape[0] == 100
        assert data[1].shape[1] == 3
