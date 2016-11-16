import os

from har import app, db
from har.model import Log
from har.log import LogExtractor, LogReader
from werkzeug import secure_filename


class LogHandler:
    def receive_log(self, subject_id, file):
        save_path = self.__save_file(file)
        extracted_files = self.__extract_file(save_path)
        log_infos = self.__log_info(extracted_files)

        return self.__store_to_database(subject_id, log_infos)

    def __save_file(self, file):
        filename = secure_filename(os.path.basename(file.filename))
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        return save_path

    def __extract_file(self, path):
        return LogExtractor(path).extract_all()

    def __log_info(self, files):
        log_info = []
        for f in files:
            reader = LogReader(f)
            metadata = reader.metadata()
            log_info.append([metadata, f])

        return log_info

    def __store_to_database(self, subject_id, log_infos):
        for info in log_infos:
            metadata = info[0]
            filepath = info[1]

            log = Log(
                subject_id,
                metadata[LogReader.Metadata.TYPE],
                metadata[LogReader.Metadata.NUMBER_OF_SENSOR],
                metadata[LogReader.Metadata.TOTAL_SENSOR_AXIS],
                metadata[LogReader.Metadata.NUMBER_OF_ENTRY],
                filepath
            )

            db.session.add(log)

        db.session.commit()
