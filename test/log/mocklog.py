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

    def mock_csv(self, log_info, min_value, max_value):
        csv_files = []
        for i in range(self.shape[self.NUMBER_OF_ITEM]):
            filename = self.__bast_path + '/log-' + str(i + 1) + '.csv'
            self.__generate_csv(filename, log_info, self.shape[self.NUMBER_OF_ROW],
                                self.shape[self.NUMBER_OF_COLUMN], min_value, max_value)

            csv_files.append(filename)

        if self.shape[self.NUMBER_OF_ITEM] is 1:
            return csv_files[0]
        else:
            return csv_files

    def __generate_csv(self, filename, log_info, number_of_rows, number_of_columns, min_value, max_value):
        with open(filename, 'wb') as log:
            writer = csv.writer(log)

            log_info.append(str(number_of_columns))
            log_info.append(str(number_of_rows))
            writer.writerow(log_info)

            data = np.random.uniform(-10, 10, (number_of_rows, number_of_columns))
            writer.writerows(data)

    def mock_zip(self, csv_files=None):
        if csv_files is None:
            log_info = ['TRAINING', '2']
            csv_files = self.mock_csv(log_info, -10, 10)
            if self.shape[self.NUMBER_OF_ITEM] is 1:
                csv_files = [csv_files]

        filename = self.__bast_path + '/log.zip'
        with zipfile.ZipFile(filename, 'w') as log_zip:
            for file in csv_files:
                log_zip.write(os.path.basename(file))

        return filename
