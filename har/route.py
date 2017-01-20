from har import app
from har.controller import LogController, SubjectController


@app.route('/subject/register', methods=['POST'])
def register():
    return SubjectController().register()


@app.route('/log/upload', methods=['POST'])
def upload_log():
    return LogController().upload()
