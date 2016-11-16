from har import app
from har.controller import LogController


@app.route('/log/upload', methods=['POST'])
def upload_log():
    return LogController().upload()
