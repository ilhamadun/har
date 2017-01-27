import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/har/')

from har import app as application

application.config.from_object('config')
application.config.from_pyfile('config.py')

if __name__ == '__main__':
    application.run(host=application.config['HOST'])
