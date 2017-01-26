"""Log File Processor.

A collection of function to process log file.

"""

import csv
import os
from zipfile import ZipFile, ZIP_DEFLATED
from har.model import log
from har.log.activity import get_activity_id

def create_dataset(log_files, output_path):
    """Create dataset from several log files.

    Args:
        log_files: List of path to log files.
        output_path: Path to create the dataset.

    """
    merged_logs = []

    for log_file in log_files:
        with open(log_file, newline='') as f:
            reader = csv.reader(f)
            metadata = next(reader)
            activity = log.parse_activity_from_metadata(metadata)
            activity_id = get_activity_id(activity)

            for row in reader:
                logs = row
                logs.append(str(activity_id))
                merged_logs.append(logs)

    merged_metadata = [len(merged_logs), metadata[2]]
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(merged_metadata)
        writer.writerows(merged_logs)

def make_archive(files, output_path):
    """Make zip archive from several files.

    Args:
        files: List of path to files.
        output_path: Path to create the archive.

    """
    assert not isinstance(files, str), "files must be list of path"
    with ZipFile(output_path, 'w', compression=ZIP_DEFLATED) as zip:
        for filename in files:
            zip.write(filename, os.path.basename(filename))
