import logging
import telebot
import time
import json
from base64 import b64decode, b64encode
from flask import Flask, request, abort
from src.common.settings import TG_URL_PATH, WORKER_URL_PATH, MS_ANS_PATH, DEBUG, EXTERNAL_HOST
from src.common.utils import gen_authorize_url, get_ngrok_url
from src.server.bot import ms_ans, deadline_kick

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Server(Flask):
    def __init__(self, name: str, tg_bot: telebot.TeleBot):
        super().__init__(name)
        self._tg_bot = tg_bot
        urls = [
            (TG_URL_PATH, self.handle_tg, {'methods': ['POST']}),
            (WORKER_URL_PATH, self.trigger, {'methods': ['GET']}),
            (MS_ANS_PATH, self.ms_ans, {'methods': ['POST']})
        ]
        for url in urls:
            if len(url) == 3:
                self.add_url_rule(url[0], url[1].__name__, url[1], **url[2])

    def handle_tg(self):
        if request.headers.get('content-type') == 'application/json':
            logger.debug(request.get_json())
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            self._tg_bot.process_new_updates([update])
            return ''
        else:
            abort(403)

    def trigger(self):
        deadline_kick()
        return 'Well done!'

    def ms_ans(self):
        req = json.loads(b64decode(request.get_json()['data']).decode('ascii'))
        if req["status"] == '1':
            ms_ans(req["mail"], req["user_id"], req["chat_id"], 1)
        else:
            ms_ans(req["mail"], req["user_id"], req["chat_id"], 0)
        return 'Well done!'

    def run_server(self):
        # logger.info(f'Debug mode == {DEBUG}')
        # logger.info('Authorize url: %s', gen_authorize_url(state='aosushkov@edu.hse.ru'))
        if DEBUG.find('ngrok') != -1:
            # Comment all lines up to `app.run` in case you ran it at least once
            # for one ngrok server_dir to avoid setting same link as telegram webhook

            ngrok_url = get_ngrok_url() + TG_URL_PATH
            wh_info = self._tg_bot.get_webhook_info()
            logger.debug(wh_info)
            if wh_info.url != ngrok_url:
                assert self._tg_bot.remove_webhook()
                # logger.info('Getting ngrok public url')
                # logger.debug('ngrok public url = %s', ngrok_url)
                time.sleep(1)
                assert self._tg_bot.set_webhook(ngrok_url)
            super().run(host='0.0.0.0', port=8000, debug=True)

        else:
            url = 'https://' + EXTERNAL_HOST + TG_URL_PATH
            wh_info = self._tg_bot.get_webhook_info()
            logger.debug(wh_info)
            if wh_info.url != url:
                assert self._tg_bot.remove_webhook()
                # logger.debug('public url = %s', url)
                time.sleep(1)
                assert self._tg_bot.set_webhook(url)
            if DEBUG:
                super().run(host='0.0.0.0', port=8000, debug=True)
            else:
                super().run(host='0.0.0.0', port=8000)
