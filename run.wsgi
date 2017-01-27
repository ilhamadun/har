import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/har/')

from har import app

app.config.from_object('config')
app.config.from_pyfile('config.py')

if __name__ == '__main__':
    app.run(host=app.config['HOST'])
