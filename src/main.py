import logging

from app import app
from settings import HOST, PORT, DEBUG
from utils import gen_authorize_url

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    if DEBUG:
        print('Authorize url without state:', gen_authorize_url())
        app.run(host='0.0.0.0', port=8000, ssl_context='adhoc', debug=DEBUG)
    else:
        app.run(host='0.0.0.0', port=8000)
