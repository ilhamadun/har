import csv
import numpy as np
import os
import zipfile


class MockLog:
    NUMBER_OF_ITEM = 0
    NUMBER_OF_ROW = 1
    NUMBER_OF_COLUMN = 2

    def __init__(self, shape):
        self.shape = shape
        self.__bast_path = os.getcwd()

    def mock_csv(self, min_value, max_value):
        csv_files = []
        for i in range(self.shape[self.NUMBER_OF_ITEM]):
            filename = self.__bast_path + '/log-' + str(i + 1) + '.csv'
            self.__generate_csv(filename, self.shape[self.NUMBER_OF_ROW],
                                self.shape[self.NUMBER_OF_COLUMN], min_value, max_value)

            csv_files.append(filename)

        return csv_files

    def __generate_csv(self, filename, number_of_rows, number_of_columns, min_value, max_value):
        with open(filename, 'wb') as log:
            writer = csv.writer(log)
            self.log = np.random.uniform(-10, 10, (number_of_rows, number_of_columns))
            writer.writerows(self.log)

    def mock_zip(self, csv_files=None):
        if csv_files is None:
            csv_files = self.mock_csv(-10, 10)

        filename = self.__bast_path + '/log.zip'
        with zipfile.ZipFile(filename, 'w') as log_zip:
            for file in csv_files:
                log_zip.write(os.path.basename(file))

        return filename
