import os
import unittest

from mocklog import MockLog
from har.log import LogShaper, LogReader


class LogShaperTestCase(unittest.TestCase):

    def setUp(self):
        mock = MockLog((1, 100, 6))
        log_info = ['TRAINING', '2']
        csv_file = mock.mock_csv(log_info, -10, 10)
        reader = LogReader(csv_file)
        data = reader.read()[1]
        self.shaper = LogShaper(data)

        os.remove(csv_file)

    def test_sliding_window(self):
        data = self.shaper.sliding_window(10, 5)

        self.assertEqual(data.shape[0], 19)
        self.assertEqual(data.shape[1], 60)

    def test_split(self):
        data = self.shaper.split(2)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].shape[0], 100)
        self.assertEqual(data[0].shape[1], 3)
        self.assertEqual(data[1].shape[0], 100)
        self.assertEqual(data[1].shape[1], 3)
