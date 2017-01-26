"""Helper functions to handle the Dataset model."""

import os
from har import app, db
from har.model import Dataset
from har.handler.log import _generate_log_directory
from har.log.processor import create_dataset, make_archive

def create_dataset_archive(logs):
    """Create dataset archive from log files.

    Args:
        logs: List of Log

    Returns:
        Entry of the newly created Dataset entry.

    """
    assert len(logs) > 0

    dataset_path = os.path.join(app.config['UPLOAD_FOLDER'], 'dataset.csv')
    archive_path = os.path.join(app.config['UPLOAD_FOLDER'], 'dataset.zip')

    log_files = _get_log_path_list(logs)
    create_dataset(log_files, dataset_path)
    make_archive([dataset_path], archive_path)
    os.remove(dataset_path)

    final_path = _move_to_unique_path(archive_path, 'dataset.zip')
    dataset = _store_to_database(logs[-1].id, logs[0].id, final_path)

    return dataset

def _get_log_path_list(logs):
    log_files = []
    for log in logs:
        log_files.append(log.path)

    return log_files

def _move_to_unique_path(archive_path, file_name):
    final_directory = _generate_log_directory(archive_path)
    final_directory = os.path.join(app.config['UPLOAD_FOLDER'], final_directory)
    final_path = os.path.join(final_directory, file_name)
    os.makedirs(final_directory)
    os.rename(archive_path, os.path.join(final_directory, final_path))

    return final_path

def _store_to_database(log_start, log_end, archive_path):
    dataset = Dataset(log_start, log_end, archive_path)

    db.session.add(dataset)
    db.session.commit()

    return dataset

def get_dataset_from_logs(logs):
    """Retreive dataset that matched with the logs argument"""
    return Dataset.query.filter_by(log_start=logs[-1].id, log_end=logs[0].id).first()
