"""Helper functions to handle the Log model."""

import hashlib
import os

from werkzeug import secure_filename
from sqlalchemy import desc
from har import app, db
from har.log import LogExtractor, LogReader
from har.model import Log
from .subject import get_subject


def receive_log(device, file):
    """Receive log file from a device.

    Extract log files, and store it's information to database. The log file will be stored in
    a directory based on the file hash.

    Args:
        device: Device identifier.
        file: File received from the device.

    """
    save_path = _save_file(device, file)
    print("Path: " + save_path)
    extracted_files = _extract_file(save_path)
    log_info = _get_log_info(extracted_files)

    return _store_to_database(device, log_info)

def _save_file(device, file):
    filename = secure_filename(os.path.basename(file.filename))
    save_dir = os.path.join(device[:2], device[2:])
    save_dir = os.path.join('/tmp', save_dir)

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, filename)
    file.save(save_path)

    return save_path

def _extract_file(path):
    log_dir = _generate_log_directory(path)
    extract_path = os.path.join(app.config['UPLOAD_FOLDER'], log_dir)
    return LogExtractor(path).extract_all(extract_path)

def _get_log_info(files):
    log_info = []
    for log_file in files:
        reader = LogReader(log_file)
        metadata = reader.metadata()
        log_info.append([metadata, log_file])

    return log_info

def _store_to_database(subject_id, log_info):
    for info in log_info:
        metadata = info[0]
        filepath = info[1]

        log_type, activity, sensor_placement = _parse_type_metadata(metadata)

        log = Log(
            subject_id,
            log_type,
            activity,
            sensor_placement,
            metadata[LogReader.Metadata.NUMBER_OF_SENSOR],
            metadata[LogReader.Metadata.TOTAL_SENSOR_AXIS],
            metadata[LogReader.Metadata.NUMBER_OF_ENTRY],
            filepath
        )

        db.session.add(log)

    db.session.commit()

def _parse_type_metadata(metadata):
    metadata_type = metadata[LogReader.Metadata.TYPE].split('#')

    log_type = None
    activity = None
    sensor_placement = None

    if len(metadata_type) > 0:
        log_type = metadata_type[0].lower()
    if len(metadata_type) > 1:
        activity = metadata_type[1].lower()
    if len(metadata_type) > 2:
        sensor_placement = metadata_type[2].lower()

    return log_type, activity, sensor_placement


def _generate_log_directory(filepath):
    hasher = hashlib.sha1()
    with open(filepath, 'rb') as log_file:
        for chunk in iter(lambda: log_file.read(4096), b''):
            hasher.update(chunk)

    file_hash = hasher.hexdigest()
    return file_hash[:2] + '/' + file_hash[2:]

def get_all_log_from_device(device):
    """Get all Log from a certain device.

    Args:
        device: Device identifier.

    Returns:
        A list of har.model.Log entry from database.

    """
    subject = get_subject(device)

    return subject.logs

def get_latest(limit=1):
    """Get latest Logs.

    Args:
        limit: Number of Logs to retreive

    Returns:
        A list of har.model.Log entry from database.
    """
    return Log.query.order_by(desc(Log.id)).limit(limit).all()
