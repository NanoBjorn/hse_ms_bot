import logging
import time

from app import app
from bot import bot
from settings import DEBUG, logger, TG_URL_PATH
from utils import gen_authorize_url, get_ngrok_url

logging.basicConfig()

if __name__ == '__main__':
    logging.info(f'Debug more == {DEBUG}')
    if DEBUG == 'local':
        logger.info('Authorize url without state:', gen_authorize_url())
        app.run(host='0.0.0.0', port=8000, ssl_context='adhoc', debug=True)
    elif DEBUG == 'local-ngrok':
        # Comment all lines up to `app.run` in case you ran it at least once
        # for one ngrok server to avoid setting same link as telegram webhook
        ngrok_url = get_ngrok_url() + TG_URL_PATH
        wh_info = bot.get_webhook_info()
        logger.debug(wh_info)
        if wh_info.url != ngrok_url:
            assert (bot.remove_webhook())
            logger.info('Getting ngrok public url')
            logger.debug('ngrok public url = %s', ngrok_url)
            time.sleep(1)
            assert (bot.set_webhook(ngrok_url + TG_URL_PATH))
        app.run(host='0.0.0.0', port=8000, debug=True)
    else:
        app.run(host='0.0.0.0', port=8000)
