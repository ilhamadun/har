from har import app
from har.controller import LogController, SubjectController, StatusController


@app.route('/subject/register', methods=['POST'])
def register():
    return SubjectController().register()


@app.route('/log/upload', methods=['POST'])
def upload_log():
    return LogController().upload()

@app.route('/status', methods=['GET'])
def status():
    return StatusController().status()
