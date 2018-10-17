import os
import sys
from flask import send_from_directory
import configparser

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

config = configparser.ConfigParser()
config.read('config.ini')

# noinspection PyPep8
import logger
# noinspection PyPep8
from app import app

LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, config['LOGGING']['FILENAME']))


@app.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    return send_from_directory('dist', '404.html')

# if __name__ == '__main__':
#     app.run()
