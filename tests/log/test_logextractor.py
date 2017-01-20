import os
import pytest

from .mocklog import MockLog
from har.log import LogExtractor


class TestLogExtractor():

    @pytest.fixture
    def setup(self):
        mocklog = MockLog((5, 10, 6))
        log_info = ['TRAINING', '2']
        self.log = mocklog.mock_csv(log_info, -10, 10)
        self.log_archive = mocklog.mock_zip(self.log)

        yield

        for log in self.log:
            os.remove(log)

        os.remove(self.log_archive)

    def test_open_bad_file(self, setup):
        with pytest.raises(IOError):
            LogExtractor(os.getcwd() + "/badfile.zip")

    def test_extract_good_file(self, setup):
        extractor = LogExtractor(self.log_archive)
        files = extractor.name_list()

        for i, file in enumerate(files):
            log = extractor.extract(files[i])
            assert log == self.log[i]

    def test_extract_all(self, setup):
        extractor = LogExtractor(self.log_archive)
        files = extractor.extract_all()

        for i, file in enumerate(files):
            assert file == self.log[i]
