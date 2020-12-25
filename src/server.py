import logging
import time

import flask
import telebot
from flask import Flask, request

from oauth import get_token, get_ms_me
from settings import MS_REDIRECT_URI_PATH, TG_URL_PATH
from state import decode_state
from utils import gen_authorize_url, get_ngrok_url

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Server(Flask):
    def __init__(self, name: str, tg_bot: telebot.TeleBot, debug_mode=None):
        super().__init__(name)
        self._debug_mode = debug_mode
        self._tg_bot = tg_bot
        urls = [
            (MS_REDIRECT_URI_PATH, self.redirect_uri, {}),
            (TG_URL_PATH, self.handle_tg, {'methods': ['POST']})
        ]
        for url in urls:
            if len(url) == 3:
                self.add_url_rule(url[0], url[1].__name__, url[1], **url[2])

    def redirect_uri(self):
        ms_code = request.args.get('code')
        state = request.args.get('state')
        if ms_code is None or state is None:
            return 'Invalid request. Use Microsoft OAuth link.'
        ms_access_token = get_token(ms_code)
        me_resp = get_ms_me(ms_access_token)
        if decode_state(state) == me_resp.get('mail'):
            return 'Success!'
        return 'Email does not correspond to state argument!'

    def handle_tg(self):
        if request.headers.get('content-type') == 'application/json':
            logger.debug(request.get_json())
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            self._tg_bot.process_new_updates([update])
            return ''
        else:
            flask.abort(403)

    def run_server(self):
        logger.info(f'Debug more == {self._debug_mode}')
        if self._debug_mode == 'local':
            #logger.info('Authorize url: %s', gen_authorize_url(state='ganovikov@edu.hse.ru'))
            super().run(host='0.0.0.0', port=8000, ssl_context='adhoc', debug=True)
        elif self._debug_mode == 'local-ngrok':
            # Comment all lines up to `app.run` in case you ran it at least once
            # for one ngrok server to avoid setting same link as telegram webhook
            logger.info('Authorize url without state: %s', gen_authorize_url("testtest"))

            # ngrok_url = get_ngrok_url() + TG_URL_PATH
            # wh_info = self._tg_bot.get_webhook_info()
            # logger.debug(wh_info)
            # if wh_info.url != ngrok_url:
            #     assert self._tg_bot.remove_webhook()
            #     logger.info('Getting ngrok public url')
            #     logger.debug('ngrok public url = %s', ngrok_url)
            #     time.sleep(1)
            #     assert self._tg_bot.set_webhook(ngrok_url)

            super().run(host='0.0.0.0', port=8000, debug=True)
        else:
            super().run(host='0.0.0.0', port=8000, ssl_context='adhoc')
