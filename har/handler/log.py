import hashlib
import os

from werkzeug import secure_filename
from har import app, db
from har.log import LogExtractor, LogReader
from har.model import Log
from .subject import SubjectHandler



class LogHandler:
    def receive_log(self, device, file):
        save_path = self.__save_file(device, file)
        extracted_files = self.__extract_file(save_path)
        log_infos = self.__log_info(extracted_files)

        return self.__store_to_database(device, log_infos)

    def __save_file(self, device, file):
        filename = secure_filename(os.path.basename(file.filename))
        save_dir = os.path.join(device[:2], device[2:])
        save_dir = os.path.join('/tmp', save_dir)

        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        save_path = os.path.join(save_dir, filename)
        file.save(save_path)

        return save_path

    def __extract_file(self, path):
        log_dir = self.generate_log_directory(path)
        extract_path = os.path.join(app.config['UPLOAD_FOLDER'], log_dir)
        return LogExtractor(path).extract_all(extract_path)

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

    def generate_log_directory(self, filepath):
        hasher = hashlib.sha1()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)

        file_hash = hasher.hexdigest()
        return file_hash[:2] + '/' + file_hash[2:]

    def get_all_log_from_device(self, device):
        subject = SubjectHandler().get_device(device)

        return subject.logs
