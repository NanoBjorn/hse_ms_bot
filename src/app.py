import flask
import telebot
from flask import Flask, request

from bot import bot
from oauth import get_token, get_ms_me
from settings import APP_NAME, MS_REDIRECT_URI_PATH, TG_URL_PATH, logger
from state import decode_state

app = Flask(APP_NAME)


@app.route(MS_REDIRECT_URI_PATH)
def redirect_uri():
    ms_code = request.args.get('code')
    state = request.args.get('state')
    if ms_code is None or state is None:
        return 'Invalid request. Use Microsoft OAuth link.'
    ms_access_token = get_token(ms_code)
    me_resp = get_ms_me(ms_access_token)
    if decode_state(state) == me_resp.get('mail'):
        return 'Success!'
    return 'Email does not correspond to state argument!'


@app.route(TG_URL_PATH, methods=['POST'])
def handle_tg():
    if request.headers.get('content-type') == 'application/json':
        logger.debug(request.get_json())
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
