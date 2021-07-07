from base64 import b64decode, b64encode
import json
from flask import Flask, request
import requests
from src.server.oauth import get_token, get_ms_me
from src.common.settings import APP_NAME, MS_REDIRECT_URI_PATH, MS_ANS_PATH, DEBUG, SERVER_HOST
from src.common.utils import get_ngrok_url


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
        if DEBUG.find('ngrok') != -1:
            url: str = get_ngrok_url()
        else:
            url: str = SERVER_HOST
        ms_code = request.args.get('code')
        state = request.args.get('state')
        if ms_code is None or state is None:
            return 'Invalid request. Use Microsoft OAuth link.'
        ms_access_token = get_token(ms_code)
        me_resp = get_ms_me(ms_access_token)
        data = b64encode(json.dumps({'mail': me_resp.get('mail'), 'uuid': str(state)}).encode('ascii'))
        requests.post(url + MS_ANS_PATH, json.dumps({'data': str(data, "ascii")}),
                      headers={'content-type': 'application/json'})
        return 'Бот напишет, если что-то пошло не так'

    def run_server(self):
        if not DEBUG:
            super().run(host='0.0.0.0', port=8001)
        else:
            super().run(host='0.0.0.0', port=8001, debug=True, ssl_context='adhoc')


server = Server(APP_NAME)
server.run_server()
