import logging
import flask
import telebot
import json
from flask import Flask, request
import requests
from src.server.oauth import get_token, get_ms_me
from src.common.settings import MS_REDIRECT_URI_PATH, TG_URL_PATH, MS_ANS_PATH
from src.server.state import decode_state
from src.common.utils import gen_authorize_url, get_ngrok_url
from src.server.bot import ms_ans, deadline_kick
import time
from src.common.settings import (
    APP_NAME, PG_DATABASE,
    PG_HOST, PG_USER, PG_PASSWORD, PG_PORT, DEBUG
)


class Server(Flask):
    def __init__(self, name: str):
        super().__init__(name)
        urls = [
            (MS_REDIRECT_URI_PATH, self.redirect_uri, {})
        ]
        for url in urls:
            if len(url) == 3:
                self.add_url_rule(url[0], url[1].__name__, url[1], **url[2])

    def redirect_uri(self):
        url: str = get_ngrok_url()
        ms_code = request.args.get('code')
        state = request.args.get('state')
        if ms_code is None or state is None:
            return 'Invalid request. Use Microsoft OAuth link.'
        ms_access_token = get_token(ms_code)
        me_resp = get_ms_me(ms_access_token)
        if decode_state(state) == me_resp.get('mail'):
            data = json.dumps({"mail": decode_state(state), "status": "1"})
            requests.post(url + MS_ANS_PATH, data, headers={'content-type': 'application/json'})
            return 'Success!'
        data = json.dumps({"mail": decode_state(state), "status": "0"})
        requests.post(url + MS_ANS_PATH, data, headers={'content-type': 'application/json'})
        return 'Email does not correspond to state argument!'

    def run_server(self):
        print(f"{gen_authorize_url(state='aosushkov@edu.hse.ru')}")
        super().run(host='0.0.0.0', port=8001, ssl_context='adhoc')


server = Server(APP_NAME)
server.run_server()