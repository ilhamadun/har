import os
import pytest

from .mocklog import MockLog
from har.log import LogReader


class TestLogReader:

    @pytest.fixture
    def setup(self):
        self.log_shape = (10, 6)
        mocklog = MockLog((1,) + self.log_shape)
        self.log_info = ['TRAINING', '2']
        self.log_csv = mocklog.mock_csv(self.log_info, -10, 10)

        yield

        os.remove(self.log_csv)

    def test_invalid_file_format(self, setup):
        with pytest.raises(IOError):
            LogReader('log.cvs')

    def test_read_log_from_csv(self, setup):
        log = LogReader(self.log_csv)
        self.assert_shape(log)

    def test_read_log_from_list_of_csv(self, setup):
        with pytest.raises(AttributeError):
            LogReader(['log.cvs'])

    def assert_shape(self, log):
        assert log.shape()[0] == self.log_shape[0]
        assert log.shape()[1] == self.log_shape[1]

    def test_read(self, setup):
        logs = LogReader(self.log_csv)
        metadata, log = logs.read()

        assert metadata[logs.Metadata.TYPE] == self.log_info[0]
        assert metadata[logs.Metadata.NUMBER_OF_SENSOR] == self.log_info[1]
        assert log.shape == self.log_shape

    def test_log_type(self, setup):
        log = LogReader(self.log_csv)

        assert log.log_type() == self.log_info[0]
